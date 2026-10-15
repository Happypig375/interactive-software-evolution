"""Build every prepared R04 arm without launching Gaia."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time


ARMS = {
    "baseline-explicit": "baseline",
    "baseline-wildcard": "baseline",
    "pause-explicit": "pause",
    "pause-wildcard": "pause",
    "fault-missing-toggle": "pause",
    "fault-hidden-content": "pause",
    "fault-advancing-time": "pause",
    "fault-reset-resume": "pause",
    "fault-stale-quit": "pause",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("prepared", type=Path)
    args = parser.parse_args()
    root = args.prepared.resolve(strict=True)
    receipt = json.loads((root / "prepare-receipt.json").read_text(encoding="utf-8"))
    logs = root / "build-logs"
    logs.mkdir(exist_ok=False)
    env = os.environ.copy()
    env.update({"DOTNET_CLI_HOME": str(root / ".dotnet-home"), "NUGET_PACKAGES": str(root / ".nuget-packages"), "DOTNET_NOLOGO": "1", "DOTNET_CLI_TELEMETRY_OPTOUT": "1"})
    version = subprocess.run(["dotnet", "--version"], cwd=Path(__file__).parent, env=env, capture_output=True, text=True)
    if version.returncode or version.stdout.strip() != "10.0.302":
        parser.error(f"SDK differs: {version.stdout}{version.stderr}")
    results = {}
    for arm, kind in ARMS.items():
        arm_root = root / "arms" / arm
        source = arm_root / "source"
        project = arm_root / "probe" / "Probe.fsproj"
        command = ["dotnet", "build", str(project), "--configuration", "Release", "--nologo", "--verbosity", "normal", f"-p:NuSource={source}", f"-p:ProbeKind={kind}"]
        started = time.monotonic()
        process = subprocess.run(command, cwd=Path(__file__).parent, env=env, capture_output=True, text=True)
        elapsed = time.monotonic() - started
        (logs / f"{arm}.stdout.log").write_text(process.stdout, encoding="utf-8")
        (logs / f"{arm}.stderr.log").write_text(process.stderr, encoding="utf-8")
        probe_dll = arm_root / "probe/bin/Release/net10.0/Probe.dll"
        app_dll = source / "Projects/Breakout Mmcc/bin/Release/net10.0/Breakout Mmcc.dll"
        nu_dll = source / "Nu/Nu/bin/Release/net10.0/Nu.dll"
        gaia_dll = source / "Nu/Nu.Gaia/bin/Release/net10.0/Nu.Gaia.dll"
        outputs = {}
        for label, path in {"probe": probe_dll, "application": app_dll, "nu": nu_dll, "gaia": gaia_dll}.items():
            if path.exists():
                outputs[label] = {"path": str(path.relative_to(root)).replace("\\", "/"), "sha256": digest(path), "bytes": path.stat().st_size}
        results[arm] = {"command": command, "exit_code": process.returncode, "elapsed_seconds": elapsed, "outputs": outputs}
        print(f"{arm}: exit={process.returncode} seconds={elapsed:.3f}")
    final = {"sdk": version.stdout.strip(), "prepare_receipt_sha256": digest(root / "prepare-receipt.json"), "arms": results}
    (root / "build-receipt.json").write_text(json.dumps(final, indent=2) + "\n", encoding="utf-8")
    return 0 if all(value["exit_code"] == 0 and len(value["outputs"]) == 4 for value in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
