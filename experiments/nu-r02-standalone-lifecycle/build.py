"""Build the MMCC then ImSim lifecycle probes against one unchanged source graph."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time


ARMS = {
    "mmcc": "Projects/Breakout Mmcc/bin/Release/net10.0",
    "imsim": "Projects/Breakout ImSim/bin/Release/net10.0",
}
PROBE_FILES = ("global.json", "Probe.fsproj", "Common.fs", "Probe.fs", "pre-execution-contract.md", "initializer-diagnostic-addendum.md")
PROBE_HOST_FILES = (
    "StandaloneLifecycleProbe.dll",
    "StandaloneLifecycleProbe.pdb",
    "StandaloneLifecycleProbe.deps.json",
    "StandaloneLifecycleProbe.runtimeconfig.json",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_record(path: Path, root: Path) -> dict[str, object]:
    return {"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)}


def tree_manifest(root: Path) -> list[dict[str, object]]:
    return [file_record(path, root) for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.relative_to(root).as_posix())]


def assembly_name(path: Path) -> str:
    env = os.environ.copy()
    env["NU_R02_ASSEMBLY_PATH"] = str(path)
    command = [
        "powershell", "-NoProfile", "-Command",
        "[Reflection.AssemblyName]::GetAssemblyName([Environment]::GetEnvironmentVariable('NU_R02_ASSEMBLY_PATH')).FullName",
    ]
    result = subprocess.run(command, env=env, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else f"unavailable: {result.stderr.strip()}"


def summary_count(text: str, label: str) -> int | None:
    matches = re.findall(rf"^\s*(\d+) {label}\(s\)\s*$", text, flags=re.MULTILINE)
    return int(matches[-1]) if matches else None


def main() -> int:
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("prepared", type=Path)
    args = parser.parse_args()
    root = args.prepared.resolve(strict=True)
    source = root / "source"
    prepare_receipt = root / "prepare-receipt.json"
    prepare = json.loads(prepare_receipt.read_text(encoding="utf-8"))
    if prepare.get("pin") != "064f7ae92a8506689cd91aff5e6804a375d6ef3d":
        parser.error("prepared pin differs")
    source_manifest_record = prepare.get("source_manifest", {})
    source_manifest_path = root / str(source_manifest_record.get("path", ""))
    if (not source_manifest_path.is_file() or
            digest(source_manifest_path) != source_manifest_record.get("sha256")):
        parser.error("prepared full-source manifest identity differs")
    original_rows = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    if len(original_rows) != source_manifest_record.get("files"):
        parser.error("prepared full-source manifest count differs")

    package = Path(__file__).resolve().parent
    public_checks = {}
    for name, expected in prepare.get("public_inputs", {}).items():
        path = package / name
        actual = {"bytes": path.stat().st_size, "sha256": digest(path)} if path.is_file() else None
        if actual != expected:
            parser.error(f"prepared public input differs: {name}")
        public_checks[name] = actual
    arm_probe_checks = {}
    for arm in ARMS:
        checks = {}
        for name in PROBE_FILES:
            expected = prepare.get("public_inputs", {}).get(name)
            path = root / "arms" / arm / "probe" / name
            actual = {"bytes": path.stat().st_size, "sha256": digest(path)} if path.is_file() else None
            if expected is None or actual != expected:
                parser.error(f"{arm}: prepared probe input differs: {name}")
            checks[name] = actual
        arm_probe_checks[arm] = checks
    attempt = root / "build-attempt-01"
    if attempt.exists():
        parser.error("build-attempt-01 already exists; use a new preparation root for another attempt")
    attempt.mkdir()

    env = os.environ.copy()
    env.update({
        "DOTNET_CLI_HOME": str(root / ".dotnet-home"),
        "NUGET_PACKAGES": str(root / ".nuget-packages"),
        "DOTNET_NOLOGO": "1",
        "DOTNET_CLI_TELEMETRY_OPTOUT": "1",
    })
    version = subprocess.run(["dotnet", "--version"], cwd=Path(__file__).parent, env=env, capture_output=True, text=True)
    (attempt / "dotnet-version.stdout.log").write_text(version.stdout, encoding="utf-8")
    (attempt / "dotnet-version.stderr.log").write_text(version.stderr, encoding="utf-8")
    if version.returncode or version.stdout.strip() != "10.0.302":
        parser.error(f"SDK differs: {version.stdout}{version.stderr}")

    results = {}
    for arm, host_relative in ARMS.items():
        probe_project = root / "arms" / arm / "probe" / "Probe.fsproj"
        command = [
            "dotnet", "build", str(probe_project), "--configuration", "Release", "--nologo", "--verbosity", "normal",
            f"-p:NuSource={source}", f"-p:Arm={arm}",
        ]
        started = time.monotonic()
        process = subprocess.run(command, cwd=Path(__file__).parent, env=env, capture_output=True, text=True)
        elapsed = time.monotonic() - started
        stdout_path = attempt / f"{arm}.stdout.log"
        stderr_path = attempt / f"{arm}.stderr.log"
        stdout_path.write_text(process.stdout, encoding="utf-8")
        stderr_path.write_text(process.stderr, encoding="utf-8")
        combined = process.stdout + "\n" + process.stderr
        diagnostics = [line for line in combined.splitlines() if re.search(r": (warning|error) [A-Z]{2}\d{4}:", line)]
        codes = sorted(set(re.findall(r"\b(?:FS|NU|MSB|CS)\d{4}\b", "\n".join(diagnostics))))
        result = {
            "command": command,
            "exit_code": process.returncode,
            "elapsed_seconds": elapsed,
            "summary_warnings": summary_count(combined, "Warning"),
            "summary_errors": summary_count(combined, "Error"),
            "diagnostic_lines": len(diagnostics),
            "diagnostic_codes": codes,
            "stdout": file_record(stdout_path, root),
            "stderr": file_record(stderr_path, root),
        }
        if process.returncode == 0:
            probe_output = probe_project.parent / "bin" / "Release" / "net10.0"
            host = source / host_relative
            copied = []
            for name in PROBE_HOST_FILES:
                source_file = probe_output / name
                destination = host / name
                if destination.exists():
                    raise SystemExit(f"{arm}: probe host file already exists: {destination}")
                shutil.copy2(source_file, destination)
                copied.append(file_record(destination, root))
            application_name = "Breakout Mmcc.dll" if arm == "mmcc" else "Breakout ImSim.dll"
            identities = {}
            for label, path in {
                "probe": host / "StandaloneLifecycleProbe.dll",
                "application": host / application_name,
                "nu": host / "Nu.dll",
            }.items():
                identities[label] = file_record(path, root) | {"assembly_name": assembly_name(path)}
            result["assembly_identity_complete"] = all(
                value["assembly_name"] and not value["assembly_name"].startswith("unavailable:")
                for value in identities.values()
            )
            result["host"] = host.relative_to(root).as_posix()
            result["probe_host_files"] = copied
            result["assemblies"] = identities
            result["host_manifest"] = tree_manifest(host)
        results[arm] = result
        print(f"{arm}: exit={process.returncode} warnings={result['summary_warnings']} errors={result['summary_errors']} seconds={elapsed:.3f}")

    changed = []
    for row in original_rows:
        path = source / row["path"]
        if not path.is_file() or path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
            changed.append(row["path"])
    receipt = {
        "sdk": version.stdout.strip(),
        "prepare_receipt": file_record(prepare_receipt, root),
        "source_manifest_validation": file_record(source_manifest_path, root) | {"files": len(original_rows)},
        "public_input_validations": public_checks,
        "arm_probe_copy_validations": arm_probe_checks,
        "original_source_inputs_checked": len(original_rows),
        "original_source_input_mismatches": changed,
        "arms": results,
    }
    receipt_path = attempt / "build-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"receipt={receipt_path} sha256={digest(receipt_path)}")
    return 0 if not changed and all(
        result["exit_code"] == 0 and "assemblies" in result and result.get("assembly_identity_complete") is True
        for result in results.values()
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
