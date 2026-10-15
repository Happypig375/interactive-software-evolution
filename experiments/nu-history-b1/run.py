"""Run one seeded B1 arm with fixed input hashes and a bounded process lifetime."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time


TARGET_HASHES = {
    "gameplay.symbol": "ffee72d91c6e4a32b650d45e9addd9e02e179163d0c8bbaaa8cddb9c92bc783a",
    "projection.json": "f62c9f3a906905f844e8b5dc58593bb99392f62293cee0899cc54bcfc8dd3cbd",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("mode", choices=("history", "fresh"))
    parser.add_argument("project_dll", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--checkpoint", type=Path, default=here / "checkpoint")
    parser.add_argument("--probe", type=Path, default=here / "bin/Release/net10.0/B1.dll")
    parser.add_argument("--timeout", type=float, default=600)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("timeout must be positive")
    checkpoint = args.checkpoint.resolve(strict=True)
    for name, expected in TARGET_HASHES.items():
        if digest(checkpoint / name) != expected:
            parser.error(f"fixed checkpoint differs: {name}")
    probe, project = args.probe.resolve(strict=True), args.project_dll.resolve(strict=True)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    command = ["dotnet", str(probe), args.mode, str(project), str(checkpoint), str(output / "probe")]
    receipt = {
        "command": command,
        "timeout_seconds": args.timeout,
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "timed_out": False,
        "fixed_inputs": TARGET_HASHES,
        "probe_sha256": digest(probe),
        "application_sha256": digest(project),
        "assemblies": {name: digest(probe.parent / name) for name in
                       ("Nu.dll", "Nu.Gaia.dll", "Probe.dll", "FSharp.Core.dll")},
        "source_files": {name: digest(here / name) for name in
                         ("B1.fs", "B1.fsproj", "run.py", "README.md")},
    }
    # Preserve launch identity even if this driver itself is interrupted.
    receipt_path = output / "process.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    start = time.monotonic()
    with (output / "stdout.log").open("wb") as stdout, (output / "stderr.log").open("wb") as stderr:
        try:
            process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                       creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
            receipt["pid"] = process.pid
            try:
                receipt["exit_code"] = process.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                receipt["timed_out"] = True
                if os.name == "nt":
                    cleanup = subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                                             capture_output=True, text=True, timeout=15)
                    receipt["deadline_cleanup_exit"] = cleanup.returncode
                else:
                    process.kill()
                receipt["exit_code"] = process.wait(timeout=15)
        except Exception as error:
            receipt["driver_error"] = repr(error)
    receipt["elapsed_seconds"] = time.monotonic() - start
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0 if receipt.get("exit_code") == 0 and not receipt["timed_out"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
