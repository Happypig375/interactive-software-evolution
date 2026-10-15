"""Launch one built standalone lifecycle arm into a new receipt directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("prepared", type=Path)
    parser.add_argument("arm", choices=("mmcc", "imsim"))
    parser.add_argument("output", type=Path)
    parser.add_argument("--timeout", type=float, default=600.0)
    parser.add_argument("--accept-build-sha256", required=True)
    args = parser.parse_args()
    if args.timeout != 600.0:
        parser.error("timeout must be exactly 600 seconds")
    root = args.prepared.resolve(strict=True)
    output = args.output.resolve()
    if output.exists():
        parser.error("output must not exist")
    receipt_path = root / "build-attempt-01" / "build-receipt.json"
    receipt_sha256 = digest(receipt_path)
    if receipt_sha256.lower() != args.accept_build_sha256.lower():
        parser.error("build receipt hash differs from the explicitly accepted identity")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    prepare_path = root / "prepare-receipt.json"
    prepare = json.loads(prepare_path.read_text(encoding="utf-8"))
    run_expected = prepare.get("public_inputs", {}).get("run.py")
    run_path = Path(__file__).resolve()
    run_actual = {"bytes": run_path.stat().st_size, "sha256": digest(run_path)}
    if run_expected != run_actual:
        parser.error("executed run.py differs from the prepared identity")
    prepare_bound = receipt.get("prepare_receipt", {})
    if (prepare_bound.get("path") != "prepare-receipt.json" or
            prepare_bound.get("bytes") != prepare_path.stat().st_size or
            prepare_bound.get("sha256") != digest(prepare_path)):
        parser.error("build receipt does not bind the current preparation receipt")
    arms = receipt.get("arms", {})
    required_arms = ("mmcc", "imsim")
    build_complete = (
        receipt.get("sdk") == "10.0.302" and
        receipt.get("original_source_input_mismatches") == [] and
        set(arms) == set(required_arms) and
        all(
            arms.get(name, {}).get("exit_code") == 0 and
            arms.get(name, {}).get("assembly_identity_complete") is True and
            set(arms.get(name, {}).get("assemblies", {})) == {"probe", "application", "nu"} and
            all(
                value.get("assembly_name") and not value["assembly_name"].startswith("unavailable:")
                for value in arms.get(name, {}).get("assemblies", {}).values()
            )
            for name in required_arms
        )
    )
    if not build_complete:
        parser.error("receipt is not a complete two-arm SDK 10.0.302 build with unchanged source inputs")
    arm = arms[args.arm]
    host = root / arm["host"]
    expected_host_paths = {record["path"] for record in arm["host_manifest"]}
    actual_host_paths = {
        path.relative_to(host).as_posix()
        for path in host.rglob("*") if path.is_file()
    }
    if actual_host_paths != expected_host_paths:
        parser.error("host file-name set differs from the reviewed build manifest")
    for record in arm["host_manifest"]:
        path = host / record["path"]
        if not path.is_file() or path.stat().st_size != record["bytes"] or digest(path) != record["sha256"]:
            parser.error(f"host identity differs: {record['path']}")
    probe = host / "StandaloneLifecycleProbe.dll"
    output.mkdir(parents=True)
    probe_output = output / "probe"
    stdout_path = output / "stdout.log"
    stderr_path = output / "stderr.log"
    stdout_path.touch()
    stderr_path.touch()
    command = ["dotnet", str(probe), str(probe_output)]
    process_receipt = {
        "arm": args.arm,
        "command": command,
        "cwd": str(host),
        "timeout_seconds": args.timeout,
        "build_receipt_sha256": receipt_sha256,
        "accepted_build_receipt_sha256": args.accept_build_sha256.lower(),
        "executed_run_py": run_actual,
        "host_files_verified": len(arm["host_manifest"]),
        "probe_sha256": digest(probe),
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "timed_out": False,
    }
    started = time.monotonic()
    process = None
    cleanup_errors = []
    try:
        with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
            try:
                process = subprocess.Popen(command, cwd=host, stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
                process_receipt["pid"] = process.pid
                process_receipt["exit_code"] = process.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                process_receipt["timed_out"] = True
                if os.name == "nt" and process is not None:
                    try:
                        cleanup = subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True, text=True, timeout=15)
                        process_receipt["deadline_cleanup_exit"] = cleanup.returncode
                        (output / "deadline-cleanup.stdout.log").write_text(cleanup.stdout, encoding="utf-8")
                        (output / "deadline-cleanup.stderr.log").write_text(cleanup.stderr, encoding="utf-8")
                    except Exception as error:
                        cleanup_errors.append({"operation": "taskkill", "type": type(error).__name__, "message": str(error)})
                if process is not None and process.poll() is None:
                    try:
                        process.kill()
                    except Exception as error:
                        cleanup_errors.append({"operation": "owned-process-kill", "type": type(error).__name__, "message": str(error)})
                if process is not None:
                    try:
                        process_receipt["exit_code"] = process.wait(timeout=15)
                    except Exception as error:
                        cleanup_errors.append({"operation": "owned-process-wait", "type": type(error).__name__, "message": str(error)})
            except Exception as error:
                process_receipt["launch_error"] = {"type": type(error).__name__, "message": str(error)}
    finally:
        process_receipt["elapsed_seconds"] = time.monotonic() - started
        process_receipt["cleanup_errors"] = cleanup_errors
        process_receipt["terminal_poll"] = process.poll() if process is not None else None
        process_receipt["owned_process_terminal"] = process is not None and process.poll() is not None
        for name in ("stdout.log", "stderr.log"):
            path = output / name
            process_receipt[name] = {"bytes": path.stat().st_size, "sha256": digest(path)} if path.is_file() else {"missing": True}
        if probe_output.exists():
            process_receipt["probe_outputs"] = {
                path.relative_to(probe_output).as_posix(): {"bytes": path.stat().st_size, "sha256": digest(path)}
                for path in sorted(item for item in probe_output.rglob("*") if item.is_file())
            }
        (output / "process.json").write_text(json.dumps(process_receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(process_receipt, indent=2))
    return 0 if process_receipt.get("exit_code") == 0 and not process_receipt["timed_out"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
