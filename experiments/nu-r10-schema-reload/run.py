"""Run one sealed live or fresh initializer-only schema observation."""

import argparse
import json
import os
import subprocess
import time
from pathlib import Path

from schema_edit import GAMEPLAY_V0_SHA256, derive_v1, require_arm
from seal_build import ORACLE_SHA256, atomic_json, file_identity, verify_receipt


SEED_SHA256 = "ffee72d91c6e4a32b650d45e9addd9e02e179163d0c8bbaaa8cddb9c92bc783a"
CHECKPOINT_FILES = ("gameplay.symbol", "model-seven.json", "projection.json")


class RunnerFailure(RuntimeError):
    pass


def atomic_bytes(path: Path, body: bytes) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("xb") as target:
        target.write(body)
        target.flush()
        os.fsync(target.fileno())
    os.replace(temporary, path)


def terminate_process_tree(
    process: subprocess.Popen | None,
    reason: str,
    timeout: float = 20.0,
    primary_runner=subprocess.run,
) -> dict:
    result = {
        "required": process is not None and process.poll() is None,
        "reason": reason,
        "timeoutSeconds": timeout,
        "attempted": False,
        "completed": process is None or process.poll() is not None,
        "exitCode": None if process is None else process.poll(),
        "errors": [],
        "primary": {"attempted": False, "confirmedTreeCleanup": False},
        "fallback": {"required": False, "attempted": False, "rootCompleted": process is None or process.poll() is not None},
        "treeCleanupConfirmed": process is None or process.poll() is not None,
    }
    if process is None or process.poll() is not None:
        result["pass"] = True
        result["furtherNativeWorkAllowed"] = True
        return result
    result["attempted"] = True
    if os.name == "nt":
        result["primary"]["attempted"] = True
        try:
            killed = primary_runner(
                ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            result["primary"].update(
                {
                    "exitCode": killed.returncode,
                    "stdout": killed.stdout,
                    "stderr": killed.stderr,
                    "confirmedTreeCleanup": killed.returncode == 0,
                }
            )
            if killed.returncode != 0:
                result["errors"].append(f"primary taskkill exited {killed.returncode}")
        except BaseException as error:
            result["primary"]["exception"] = {"type": type(error).__name__, "message": str(error)}
            result["errors"].append(f"primary taskkill {type(error).__name__}: {error}")
    else:
        result["primary"]["attempted"] = True
        try:
            process.terminate()
            result["primary"]["confirmedTreeCleanup"] = True
        except BaseException as error:
            result["primary"]["exception"] = {"type": type(error).__name__, "message": str(error)}
            result["errors"].append(f"primary terminate {type(error).__name__}: {error}")
    primary_failed = not result["primary"].get("confirmedTreeCleanup", False)
    if not primary_failed:
        try:
            result["exitCode"] = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired as error:
            result["primary"]["waitException"] = {"type": type(error).__name__, "message": str(error)}
            result["errors"].append("bounded primary cleanup wait expired")
        except BaseException as error:
            result["primary"]["waitException"] = {"type": type(error).__name__, "message": str(error)}
            result["errors"].append(f"primary wait {type(error).__name__}: {error}")
    root_alive = process.poll() is None
    result["fallback"]["required"] = root_alive and (primary_failed or "waitException" in result["primary"])
    if root_alive and (primary_failed or "waitException" in result["primary"]):
        result["fallback"]["attempted"] = True
        try:
            process.kill()
            result["exitCode"] = process.wait(timeout=timeout)
        except BaseException as error:
            result["fallback"]["exception"] = {"type": type(error).__name__, "message": str(error)}
            result["errors"].append(f"fallback direct kill/wait {type(error).__name__}: {error}")
    result["fallback"]["rootCompleted"] = process.poll() is not None
    result["completed"] = process.poll() is not None
    result["treeCleanupConfirmed"] = bool(result["primary"].get("confirmedTreeCleanup"))
    result["pass"] = result["completed"] and result["treeCleanupConfirmed"]
    result["furtherNativeWorkAllowed"] = result["pass"]
    return result


def checkpoint_identities(checkpoint: Path) -> dict:
    result = {}
    for name in CHECKPOINT_FILES:
        path = (checkpoint / name).resolve(strict=True)
        result[name] = {"path": str(path), **file_identity(path)}
    return result


def validate_checkpoint_against_oracle(checkpoint: Path, oracle: dict) -> dict:
    identities = checkpoint_identities(checkpoint)
    model = json.loads((checkpoint / "model-seven.json").read_text(encoding="utf-8"))
    if model != oracle["checkpoint"]:
        raise RunnerFailure("live checkpoint model differs from the independent frozen oracle")
    return identities


def create_live_binding(
    checkpoint: Path,
    ready: Path,
    oracle_path: Path,
    seed_identity: dict,
    arm_receipt_identity: dict,
) -> dict:
    ready_value = json.loads(ready.read_text(encoding="utf-8"))
    checkpoint_files = checkpoint_identities(checkpoint)
    expected_ready = {
        "gameplay.symbol": "symbolSha256",
        "model-seven.json": "modelSevenSha256",
        "projection.json": "projectionSha256",
    }
    for name, field in expected_ready.items():
        if checkpoint_files[name]["sha256"] != ready_value.get(field):
            raise RunnerFailure(f"ready handshake hash differs for {name}")
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    validate_checkpoint_against_oracle(checkpoint, oracle)
    binding_path = checkpoint / "checkpoint-binding.json"
    if binding_path.exists():
        raise RunnerFailure("live checkpoint binding already exists")
    binding = {
        "schemaVersion": 1,
        "createdUtc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mode": "live",
        "nativeLaunch": True,
        "checkpointPath": str(checkpoint.resolve()),
        "ready": {"path": str(ready.resolve()), **file_identity(ready)},
        "oracle": {"path": str(oracle_path.resolve()), **file_identity(oracle_path)},
        "seed": seed_identity,
        "armReceipt": arm_receipt_identity,
        "checkpointFiles": checkpoint_files,
        "checkpointEqualsIndependentOracle": True,
    }
    atomic_json(binding_path, binding)
    return {"path": str(binding_path.resolve()), **file_identity(binding_path)}


def verify_live_binding(
    checkpoint: Path,
    binding_path: Path,
    accepted_hash: str,
    oracle_path: Path,
    seed_identity: dict,
) -> dict:
    expected_path = (checkpoint / "checkpoint-binding.json").resolve(strict=True)
    binding_path = binding_path.resolve(strict=True)
    if binding_path != expected_path:
        raise RunnerFailure("fresh binding must be the exact receipt inside the live checkpoint")
    identity = {"path": str(binding_path), **file_identity(binding_path)}
    if identity["sha256"] != accepted_hash.lower():
        raise RunnerFailure("live checkpoint binding SHA-256 differs from the accepted value")
    binding = json.loads(binding_path.read_text(encoding="utf-8"))
    if binding.get("schemaVersion") != 1 or binding.get("mode") != "live":
        raise RunnerFailure("live checkpoint binding schema differs")
    if binding.get("checkpointPath") != str(checkpoint.resolve()):
        raise RunnerFailure("live checkpoint binding points at another checkpoint")
    if binding.get("oracle", {}).get("sha256") != ORACLE_SHA256:
        raise RunnerFailure("live checkpoint binding oracle differs")
    if binding.get("seed", {}).get("sha256") != seed_identity["sha256"]:
        raise RunnerFailure("live checkpoint binding seed differs")
    current = checkpoint_identities(checkpoint)
    if current != binding.get("checkpointFiles"):
        raise RunnerFailure("live checkpoint files changed after binding")
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    validate_checkpoint_against_oracle(checkpoint, oracle)
    return identity


def artifact_identities(output: Path) -> dict:
    names = (
        "stdout.log",
        "stderr.log",
        "Gameplay.before.fs",
        "Gameplay.after.fs",
        "edit.json",
        "probe/trace.jsonl",
        "probe/generated-reload.fsx",
        "probe/ready.json",
        "probe/go.signal",
    )
    result = {}
    for name in names:
        path = output / Path(name)
        if path.is_file():
            result[name] = {"path": str(path.resolve()), **file_identity(path)}
    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("live", "fresh"))
    parser.add_argument("probe", type=Path)
    parser.add_argument("project_dll", type=Path)
    parser.add_argument("seed", type=Path)
    parser.add_argument("checkpoint", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--gameplay-source", type=Path, required=True)
    parser.add_argument("--arm-receipt", type=Path, required=True)
    parser.add_argument("--arm-receipt-sha256", required=True)
    parser.add_argument("--live-binding-receipt", type=Path)
    parser.add_argument("--live-binding-sha256")
    parser.add_argument("--timeout", type=float, default=900.0)
    parser.add_argument("--checkpoint-timeout", type=float, default=420.0)
    args = parser.parse_args(argv)
    if args.timeout != 900.0:
        parser.error("the frozen process deadline is exactly 900 seconds")
    if args.checkpoint_timeout != 420.0:
        parser.error("the frozen checkpoint deadline is exactly 420 seconds")
    if args.mode == "live" and (args.live_binding_receipt or args.live_binding_sha256):
        parser.error("live mode creates rather than consumes a checkpoint binding")
    if args.mode == "fresh" and not (args.live_binding_receipt and args.live_binding_sha256):
        parser.error("fresh mode requires the exact accepted live checkpoint binding")
    return args


def execute(args: argparse.Namespace) -> int:
    started_wall = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    started = time.monotonic()
    output = args.output.resolve()
    if output.exists():
        raise RunnerFailure("output must be new")
    output.mkdir(parents=True)
    receipt_path = output / "process.json"
    receipt = {
        "schemaVersion": 2,
        "mode": args.mode,
        "startedUtc": started_wall,
        "timeoutSeconds": args.timeout,
        "checkpointTimeoutSeconds": args.checkpoint_timeout,
        "nativeLaunch": False,
        "timedOut": False,
        "checkpointTimedOut": False,
    }
    process: subprocess.Popen | None = None
    caught: BaseException | None = None
    process_completed = False
    cleanup = {"required": False, "attempted": False, "completed": True, "reason": "not-started"}
    stdout_path, stderr_path = output / "stdout.log", output / "stderr.log"
    stdout = stdout_path.open("xb")
    stderr = stderr_path.open("xb")
    try:
        arm = "v0" if args.mode == "live" else "v1"
        probe = args.probe.resolve(strict=True)
        application = args.project_dll.resolve(strict=True)
        seed = args.seed.resolve(strict=True)
        checkpoint = args.checkpoint.resolve()
        gameplay = args.gameplay_source.resolve(strict=True)
        oracle_path = Path(__file__).with_name("oracle.json").resolve(strict=True)
        if file_identity(oracle_path)["sha256"] != ORACLE_SHA256:
            raise RunnerFailure("public independent oracle identity differs")
        seed_identity = {"path": str(seed), **file_identity(seed)}
        if seed_identity["sha256"] != SEED_SHA256:
            raise RunnerFailure("seed identity differs from the exact frozen B0 symbol")
        require_arm(gameplay.read_bytes(), arm)
        sealed = verify_receipt(
            args.arm_receipt,
            args.arm_receipt_sha256,
            arm,
            probe,
            application,
            gameplay,
        )
        receipt["armReceipt"] = sealed["identity"]
        receipt["sourceManifestVerification"] = sealed["sourceManifestVerification"]
        receipt["toolchainVerification"] = sealed["toolchainVerification"]
        receipt["seed"] = seed_identity
        receipt["oracle"] = {"path": str(oracle_path), **file_identity(oracle_path)}
        receipt["gameplaySource"] = {"path": str(gameplay), **file_identity(gameplay)}
        if args.mode == "live":
            if checkpoint.exists() and any(checkpoint.iterdir()):
                raise RunnerFailure("live checkpoint directory must be new or empty")
            checkpoint.mkdir(parents=True, exist_ok=True)
        else:
            binding = verify_live_binding(
                checkpoint,
                args.live_binding_receipt,
                args.live_binding_sha256,
                oracle_path,
                seed_identity,
            )
            receipt["liveCheckpointBinding"] = binding
        probe_output = output / "probe"
        command = [
            "dotnet",
            "--fx-version",
            "10.0.10",
            str(probe),
            args.mode,
            str(application),
            str(seed),
            str(checkpoint),
            str(probe_output),
        ]
        receipt["command"] = command
        receipt["probe"] = {"path": str(probe), **file_identity(probe)}
        receipt["application"] = {"path": str(application), **file_identity(application)}
        process = subprocess.Popen(
            command,
            stdout=stdout,
            stderr=stderr,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        receipt["nativeLaunch"] = True
        receipt["pid"] = process.pid
        if args.mode == "live":
            ready = probe_output / "ready.json"
            deadline = started + args.checkpoint_timeout
            while not ready.exists() and process.poll() is None and time.monotonic() < deadline:
                time.sleep(0.1)
            if not ready.exists():
                if process.poll() is None:
                    receipt["checkpointTimedOut"] = True
                    raise RunnerFailure("checkpoint-ready timeout")
                raise RunnerFailure("process exited before checkpoint-ready handshake")
            if process.poll() is not None:
                raise RunnerFailure("process exited at checkpoint-ready handshake")
            binding = create_live_binding(
                checkpoint,
                ready,
                oracle_path,
                seed_identity,
                sealed["identity"],
            )
            receipt["liveCheckpointBinding"] = binding
            before_body = gameplay.read_bytes()
            if file_identity(gameplay)["sha256"] != GAMEPLAY_V0_SHA256:
                raise RunnerFailure("Gameplay V0 identity changed before edit")
            after_body = derive_v1(before_body)
            before_copy = output / "Gameplay.before.fs"
            after_copy = output / "Gameplay.after.fs"
            atomic_bytes(before_copy, before_body)
            atomic_bytes(after_copy, after_body)
            atomic_bytes(gameplay, after_body)
            edit = {
                "before": {"path": str(before_copy.resolve()), **file_identity(before_copy)},
                "after": {"path": str(after_copy.resolve()), **file_identity(after_copy)},
                "installedSource": {"path": str(gameplay), **file_identity(gameplay)},
                "bytePreservation": {"utf8Bom": True, "lineEndings": "CRLF"},
                "changedAnchors": ["record", "empty", "score"],
                "changedAnchorCount": 3,
                "ready": {"path": str(ready.resolve()), **file_identity(ready)},
                "checkpointBinding": binding,
            }
            atomic_json(output / "edit.json", edit)
            atomic_json(probe_output / "go.signal", edit)
        remaining = max(1.0, args.timeout - (time.monotonic() - started))
        try:
            receipt["exitCode"] = process.wait(timeout=remaining)
            process_completed = True
        except subprocess.TimeoutExpired as error:
            receipt["timedOut"] = True
            raise RunnerFailure("overall process timeout") from error
        if receipt["exitCode"] != 0:
            raise RunnerFailure(f"observation process exited {receipt['exitCode']}")
    except BaseException as error:
        caught = error
        receipt["exception"] = {
            "type": type(error).__name__,
            "message": str(error),
            "interrupted": isinstance(error, KeyboardInterrupt),
        }
    finally:
        if process is not None and process.poll() is not None:
            process_completed = True
            receipt.setdefault("exitCode", process.poll())
        if process is not None and not process_completed:
            cleanup = terminate_process_tree(process, "handled-exception-or-incomplete-lifecycle")
        else:
            cleanup = terminate_process_tree(process, "process-already-completed")
        receipt["cleanup"] = cleanup
        stdout.close()
        stderr.close()
        receipt["elapsedSeconds"] = time.monotonic() - started
        receipt["artifacts"] = artifact_identities(output)
        receipt["runnerPass"] = bool(
            caught is None
            and receipt.get("exitCode") == 0
            and not receipt["timedOut"]
            and not receipt["checkpointTimedOut"]
            and cleanup.get("pass") is True
        )
        try:
            atomic_json(receipt_path, receipt)
        except BaseException as write_error:
            fallback = output / "process-receipt-write-failure.json"
            atomic_json(
                fallback,
                {
                    "schemaVersion": 1,
                    "originalReceiptPath": str(receipt_path),
                    "writeError": {"type": type(write_error).__name__, "message": str(write_error)},
                    "receipt": receipt,
                },
            )
            raise
    print(json.dumps(receipt, indent=2))
    if isinstance(caught, KeyboardInterrupt):
        return 130
    return 0 if receipt["runnerPass"] else 1


def main(argv: list[str] | None = None) -> int:
    return execute(parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
