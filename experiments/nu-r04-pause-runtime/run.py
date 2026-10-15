"""Launch one prepared R04 arm into a new immutable receipt directory."""

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
    parser.add_argument("arm", choices=("baseline-explicit", "baseline-wildcard", "pause-explicit", "pause-wildcard", "fault-missing-toggle", "fault-hidden-content", "fault-advancing-time", "fault-reset-resume", "fault-stale-quit"))
    parser.add_argument("checkpoint", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--timeout", type=float, default=600.0)
    args = parser.parse_args()
    root = args.prepared.resolve(strict=True)
    checkpoint = args.checkpoint.resolve(strict=True)
    output = args.output.resolve()
    if output.exists():
        parser.error("output must not exist")
    if args.timeout != 600.0:
        parser.error("timeout must be exactly 600 seconds")
    arm_root = root / "arms" / args.arm
    build_receipt = root / "build-receipt.json"
    build_data = json.loads(build_receipt.read_text(encoding="utf-8"))
    if build_data.get("sdk") != "10.0.302" or build_data.get("arms", {}).get(args.arm, {}).get("exit_code") != 0:
        parser.error("selected arm lacks a successful SDK 10.0.302 build receipt")
    probe = arm_root / "probe/bin/Release/net10.0/Probe.dll"
    application = arm_root / "source/Projects/Breakout Mmcc/bin/Release/net10.0/Breakout Mmcc.dll"
    nu = arm_root / "source/Nu/Nu/bin/Release/net10.0/Nu.dll"
    gaia = arm_root / "source/Nu/Nu.Gaia/bin/Release/net10.0/Nu.Gaia.dll"
    probe.resolve(strict=True)
    application.resolve(strict=True)
    nu.resolve(strict=True)
    gaia.resolve(strict=True)
    output.mkdir(parents=True)
    command = ["dotnet", str(probe), str(application), str(checkpoint), str(output / "probe")]
    receipt = {"arm": args.arm, "command": command, "timeout_seconds": args.timeout, "build_receipt_sha256": digest(build_receipt), "probe_sha256": digest(probe), "application_sha256": digest(application), "nu_sha256": digest(nu), "gaia_sha256": digest(gaia), "checkpoint_sha256": digest(checkpoint), "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "timed_out": False}
    start = time.monotonic()
    with (output / "stdout.log").open("wb") as stdout, (output / "stderr.log").open("wb") as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        receipt["pid"] = process.pid
        try:
            receipt["exit_code"] = process.wait(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            receipt["timed_out"] = True
            if os.name == "nt":
                cleanup = subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True, text=True, timeout=15)
                receipt["deadline_cleanup_exit"] = cleanup.returncode
            else:
                process.kill()
            receipt["exit_code"] = process.wait(timeout=15)
    receipt["elapsed_seconds"] = time.monotonic() - start
    (output / "process.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["exit_code"] == 0 and not receipt["timed_out"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
