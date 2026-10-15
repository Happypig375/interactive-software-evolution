"""Run one preassigned R06 process from an explicitly accepted build receipt."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time


PIN = "064f7ae92a8506689cd91aff5e6804a375d6ef3d"
SDK = "10.0.302"
TARGET_HASHES = {
    "gameplay.symbol": "ffee72d91c6e4a32b650d45e9addd9e02e179163d0c8bbaaa8cddb9c92bc783a",
    "projection.json": "f62c9f3a906905f844e8b5dc58593bb99392f62293cee0899cc54bcfc8dd3cbd",
}
REQUIRED_BINARIES = {
    "RecoveryCost.dll",
    "RecoveryCost.runtimeconfig.json",
    "RecoveryCost.deps.json",
    "Probe.dll",
    "Breakout Mmcc.dll",
    "Nu.dll",
    "Nu.Gaia.dll",
}


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def verify_identity(label, entry):
    path = Path(entry["path"]).resolve(strict=True)
    if digest(path) != entry["sha256"] or path.stat().st_size != entry["bytes"]:
        raise ValueError(f"{label} differs from the accepted build receipt")
    return path


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("attempt_id")
    parser.add_argument("build_receipt", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--accept-build-sha256", required=True)
    parser.add_argument("--checkpoint", type=Path, default=here.parent / "nu-history-b1" / "checkpoint")
    parser.add_argument("--timeout", type=float, default=600)
    args = parser.parse_args()
    if args.timeout != 600:
        parser.error("the frozen process deadline is exactly 600 seconds")

    plan = json.loads((here / "attempt-plan.json").read_text(encoding="utf-8"))
    attempts = plan["feasibility"] + plan["measuredOrder"]
    by_id = {entry["attemptId"]: entry for entry in attempts}
    if args.attempt_id not in by_id:
        parser.error("attempt id is not in the frozen attempt plan")
    assigned = by_id[args.attempt_id]

    build_path = args.build_receipt.resolve(strict=True)
    build_hash = digest(build_path)
    if build_hash != args.accept_build_sha256.lower():
        parser.error("build receipt hash is not the explicitly accepted hash")
    build = json.loads(build_path.read_text(encoding="utf-8"))
    if build.get("schemaVersion") != 2 or build.get("status") != "passed" or build.get("exitCode") != 0:
        parser.error("build receipt is not a successful R06 build")
    if build.get("pin") != PIN or build.get("sdk") != SDK:
        parser.error("build receipt pin or SDK differs")

    try:
        prepare_path = verify_identity("prepare receipt", build["prepareReceipt"])
        prepare = json.loads(prepare_path.read_text(encoding="utf-8"))
        if prepare.get("status") != "passed" or not prepare["finalFullArchiveComparison"]["passes"]:
            raise ValueError("prepare receipt no longer establishes the full archive comparison")
        source_paths = {
            name: verify_identity(f"source {name}", entry)
            for name, entry in build["sourceIdentities"].items()
        }
        binaries = build["commonBinaries"]
        if set(binaries) != REQUIRED_BINARIES:
            raise ValueError("build receipt common binary set differs")
        binary_paths = {
            name: verify_identity(f"binary {name}", entry)
            for name, entry in binaries.items()
        }
    except (KeyError, OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))

    checkpoint = args.checkpoint.resolve(strict=True)
    for name, expected in TARGET_HASHES.items():
        if digest(checkpoint / name) != expected:
            parser.error(f"fixed checkpoint differs: {name}")
        fixed_entry = build["fixedInputs"][f"fixed/{name}"]
        if expected != fixed_entry["sha256"]:
            parser.error(f"build receipt fixed input differs: {name}")
    if source_paths["r06/run.py"] != Path(__file__).resolve():
        parser.error("accepted build used a different run.py")

    probe = binary_paths["RecoveryCost.dll"]
    project = binary_paths["Breakout Mmcc.dll"]
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    command = [
        "dotnet", str(probe), assigned["route"], assigned["kind"], assigned["attemptId"],
        str(project), str(checkpoint), str(output / "probe"),
    ]
    receipt = {
        "schemaVersion": 2,
        "attempt": assigned,
        "command": command,
        "timeoutSeconds": 600,
        "startedUtc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "timedOut": False,
        "acceptedBuildReceipt": {"path": str(build_path), "sha256": build_hash},
        "verifiedSourceIdentities": build["sourceIdentities"],
        "verifiedCommonBinaries": build["commonBinaries"],
        "fixedInputs": TARGET_HASHES,
    }
    receipt_path = output / "process.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    start = time.monotonic()
    with (output / "stdout.log").open("wb") as stdout, (output / "stderr.log").open("wb") as stderr:
        try:
            process = subprocess.Popen(
                command,
                stdout=stdout,
                stderr=stderr,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
            receipt["pid"] = process.pid
            receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
            try:
                receipt["exitCode"] = process.wait(timeout=600)
            except subprocess.TimeoutExpired:
                receipt["timedOut"] = True
                if os.name == "nt":
                    cleanup = subprocess.run(
                        ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                        capture_output=True,
                        text=True,
                        timeout=15,
                    )
                    receipt["deadlineCleanupExit"] = cleanup.returncode
                else:
                    process.kill()
                receipt["exitCode"] = process.wait(timeout=15)
        except Exception as error:
            receipt["driverError"] = repr(error)
    receipt["processElapsedSecondsNotComponentCost"] = time.monotonic() - start
    probe_output = output / "probe"
    receipt["probeOutputs"] = {
        path.name: {"bytes": path.stat().st_size, "sha256": digest(path)}
        for path in sorted(probe_output.iterdir()) if path.is_file()
    } if probe_output.is_dir() else {}
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0 if receipt.get("exitCode") == 0 and not receipt["timedOut"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
