"""Create and verify immutable R10 arm build snapshots."""

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import time
from pathlib import Path

from schema_edit import GAMEPLAY_V0_SHA256, GAMEPLAY_V1_SHA256, require_arm
from source_manifest import (
    ARCHIVE_BYTES,
    ARCHIVE_FILE_COUNT,
    ARCHIVE_SHA256,
    build_source_manifest,
    verify_source_manifest,
)


PIN = "064f7ae92a8506689cd91aff5e6804a375d6ef3d"
ORACLE_SHA256 = "327d804d8d780f70894476267f0995554764798309b6a5fa1b88c1fe69b1cb2c"
RUNTIME_VERSION = "10.0.10"
PACKAGE_FILES = (
    "SchemaReload.fs",
    "SchemaReload.fsproj",
    "prepare.py",
    "schema_edit.py",
    "source_manifest.py",
    "seal_build.py",
    "run.py",
    "compare.py",
    "objective_checks.py",
    "README.md",
    "oracle.json",
)


def file_identity(path: Path) -> dict:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return {"sha256": digest.hexdigest(), "bytes": size}


def atomic_json(path: Path, value: dict) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("x", encoding="utf-8", newline="\n") as target:
        json.dump(value, target, indent=2)
        target.write("\n")
        target.flush()
        os.fsync(target.fileno())
    os.replace(temporary, path)


def selected_output_files(directory: Path) -> list[Path]:
    directory = directory.resolve(strict=True)
    files = []
    for item in directory.rglob("*"):
        if item.is_file():
            resolved = item.resolve(strict=True)
            try:
                resolved.relative_to(directory)
            except ValueError as error:
                raise ValueError(f"output file resolves outside its root: {item}") from error
            files.append(item)
    return sorted(files, key=lambda item: item.relative_to(directory).as_posix())


def run_probe(command: list[str]) -> str:
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout.strip()


def probe_toolchain() -> dict:
    sdk = run_probe(["dotnet", "--version"])
    runtimes = run_probe(["dotnet", "--list-runtimes"]).splitlines()
    info = run_probe(["dotnet", "--info"])
    runtime_pattern = re.compile(r"^Microsoft\.NETCore\.App\s+(\S+)\s+\[(.+)\]$")
    selected = None
    for line in runtimes:
        match = runtime_pattern.match(line.strip())
        if match and match.group(1) == RUNTIME_VERSION:
            selected = {"framework": "Microsoft.NETCore.App", "version": match.group(1), "path": match.group(2)}
            break
    rid_match = re.search(r"^\s*RID:\s*(\S+)\s*$", info, re.MULTILINE)
    os_name_match = re.search(r"^\s*OS Name:\s*(.+?)\s*$", info, re.MULTILINE)
    os_version_match = re.search(r"^\s*OS Version:\s*(.+?)\s*$", info, re.MULTILINE)
    result = {
        "sdk": sdk,
        "selectedRuntime": selected,
        "installedRuntimes": runtimes,
        "os": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "dotnetName": os_name_match.group(1) if os_name_match else None,
            "dotnetVersion": os_version_match.group(1) if os_version_match else None,
        },
        "architecture": {"machine": platform.machine(), "rid": rid_match.group(1) if rid_match else None},
    }
    if sdk != "10.0.302":
        raise ValueError(f"unexpected SDK {sdk}")
    if selected is None:
        raise ValueError(f"Microsoft.NETCore.App {RUNTIME_VERSION} is not installed")
    if result["os"]["system"] != "Windows" or result["os"]["dotnetName"] != "Windows":
        raise ValueError("frozen probe requires Windows")
    if result["architecture"]["machine"].upper() not in ("AMD64", "X86_64") or result["architecture"]["rid"] != "win-x64":
        raise ValueError("frozen probe requires Windows x64")
    return result


def verify_output_roots(receipt: dict, entries: list[dict], snapshot_root: Path) -> None:
    for label, root in receipt.get("outputRoots", {}).items():
        current_root = Path(root["currentRoot"]).resolve(strict=True)
        snapshot_output_root = (snapshot_root / root["snapshotRoot"]).resolve(strict=True)
        expected = sorted(
            entry["currentPath"]
            for entry in entries
            if entry.get("role", "").startswith(f"output:{label}:")
        )
        actual = sorted(str(item.resolve(strict=True)) for item in selected_output_files(current_root))
        if actual != expected or len(expected) != root.get("fileCount"):
            raise ValueError(f"current output-root file set differs: {label}")
        expected_snapshot = sorted(
            str((snapshot_root / entry["snapshotPath"]).resolve(strict=True))
            for entry in entries
            if entry.get("role", "").startswith(f"output:{label}:")
        )
        actual_snapshot = sorted(str(item.resolve(strict=True)) for item in selected_output_files(snapshot_output_root))
        if actual_snapshot != expected_snapshot:
            raise ValueError(f"snapshot output-root file set differs: {label}")


def copy_entry(current: Path, snapshot: Path, role: str, root: Path) -> dict:
    current = current.resolve(strict=True)
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    if snapshot.exists():
        raise FileExistsError(f"refusing snapshot reuse: {snapshot}")
    shutil.copy2(current, snapshot)
    snapshot = snapshot.resolve(strict=True)
    if os.path.samefile(current, snapshot):
        raise RuntimeError(f"snapshot is a hardlink or same file: {snapshot}")
    current_identity = file_identity(current)
    snapshot_identity = file_identity(snapshot)
    if current_identity != snapshot_identity:
        raise RuntimeError(f"snapshot copy differs: {current}")
    return {
        "role": role,
        "currentPath": str(current),
        "snapshotPath": str(snapshot.relative_to(root)),
        **current_identity,
    }


def verify_receipt(
    receipt_path: Path,
    receipt_sha256: str,
    arm: str,
    probe: Path,
    application: Path,
    gameplay: Path,
) -> dict:
    receipt_path = receipt_path.resolve(strict=True)
    receipt_identity = file_identity(receipt_path)
    if receipt_identity["sha256"] != receipt_sha256.lower():
        raise ValueError("arm receipt SHA-256 differs from the accepted value")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("schemaVersion") != 3 or receipt.get("arm") != arm:
        raise ValueError("arm receipt schema or arm differs")
    if receipt.get("pin") != PIN or receipt.get("nativeLaunch") is not False:
        raise ValueError("arm receipt pin or execution boundary differs")
    snapshot_root = Path(receipt["snapshotRoot"]).resolve(strict=True)
    if receipt_path.parent != snapshot_root:
        raise ValueError("arm receipt is not located at its immutable snapshot root")
    entries = receipt.get("files", [])
    for entry in entries:
        current = Path(entry["currentPath"]).resolve(strict=True)
        snapshot = (snapshot_root / entry["snapshotPath"]).resolve(strict=True)
        expected = {"sha256": entry["sha256"], "bytes": entry["bytes"]}
        if file_identity(current) != expected or file_identity(snapshot) != expected:
            raise ValueError(f"current or snapshot identity differs for {entry['role']}")
        if os.path.samefile(current, snapshot):
            raise ValueError(f"snapshot is not an independent copy for {entry['role']}")
    manifest_binding = receipt.get("sourceManifest", {})
    manifest_path = (snapshot_root / manifest_binding.get("snapshotPath", "")).resolve(strict=True)
    expected_manifest_path = (snapshot_root / "source-manifest.json").resolve(strict=True)
    if manifest_path != expected_manifest_path or file_identity(manifest_path) != {
        "sha256": manifest_binding.get("sha256"),
        "bytes": manifest_binding.get("bytes"),
    }:
        raise ValueError("source manifest path or identity differs")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_root = Path(manifest["sourceRoot"]).resolve(strict=True)
    manifest_result = verify_source_manifest(manifest, source_root, arm)
    if manifest_result["fileCount"] != ARCHIVE_FILE_COUNT:
        raise ValueError("source manifest verification count differs")
    verify_output_roots(receipt, entries, snapshot_root)
    current_toolchain = probe_toolchain()
    accepted_toolchain = receipt.get("toolchain")
    for field in ("sdk", "selectedRuntime", "os", "architecture"):
        if current_toolchain[field] != accepted_toolchain.get(field):
            raise ValueError(f"current probed toolchain differs: {field}")
    bindings = receipt.get("launchBindings", {})
    expected_paths = {
        "probe": probe.resolve(strict=True),
        "application": application.resolve(strict=True),
        "gameplay": gameplay.resolve(strict=True),
    }
    for name, expected_path in expected_paths.items():
        binding = bindings.get(name)
        if not binding or Path(binding["currentPath"]).resolve(strict=True) != expected_path:
            raise ValueError(f"{name} launch path differs from the arm receipt")
        if file_identity(expected_path) != {"sha256": binding["sha256"], "bytes": binding["bytes"]}:
            raise ValueError(f"{name} launch identity differs from the arm receipt")
    require_arm(gameplay.read_bytes(), arm)
    expected_gameplay = GAMEPLAY_V0_SHA256 if arm == "v0" else GAMEPLAY_V1_SHA256
    if bindings["gameplay"]["sha256"] != expected_gameplay:
        raise ValueError("receipt Gameplay identity differs from the frozen arm")
    return {
        "receipt": receipt,
        "identity": {"path": str(receipt_path), **receipt_identity},
        "sourceManifestVerification": manifest_result,
        "toolchainVerification": current_toolchain,
    }


def seal(args: argparse.Namespace) -> dict:
    root = Path(__file__).resolve().parents[2]
    package = Path(__file__).resolve().parent
    snapshot_root = args.snapshot.resolve()
    if snapshot_root.exists():
        raise FileExistsError(f"snapshot output must be new: {snapshot_root}")
    snapshot_root.mkdir(parents=True)
    source_root = args.source_root.resolve(strict=True)
    archive = args.archive.resolve(strict=True)
    probe = args.probe.resolve(strict=True)
    application = args.application.resolve(strict=True)
    gameplay = args.gameplay_source.resolve(strict=True)
    build_log = args.build_log.resolve(strict=True)
    require_arm(gameplay.read_bytes(), args.arm)
    oracle = package / "oracle.json"
    if file_identity(oracle)["sha256"] != ORACLE_SHA256:
        raise ValueError("public independent oracle identity differs")
    archive_identity = file_identity(archive)
    if archive_identity != {"sha256": ARCHIVE_SHA256, "bytes": ARCHIVE_BYTES}:
        raise ValueError("pinned archive identity differs")
    toolchain = probe_toolchain()
    manifest = build_source_manifest(archive, source_root, args.arm, archive_identity)
    manifest_path = snapshot_root / "source-manifest.json"
    atomic_json(manifest_path, manifest)
    manifest_identity = file_identity(manifest_path)

    entries: list[dict] = []

    def add(current: Path, relative: Path, role: str) -> None:
        entries.append(copy_entry(current, snapshot_root / relative, role, snapshot_root))

    for name in PACKAGE_FILES:
        add(package / name, Path("package") / name, f"package:{name}")
    add(gameplay, Path("source") / "Gameplay.fs", "source:Gameplay.fs")
    add(source_root / "Nu" / "Nu.Gaia" / "Gaia.fs", Path("source") / "Gaia.fs", "source:Gaia.fs")
    add(build_log, Path("evidence") / build_log.name, "build-log")

    output_roots = {
        "probe-bin": probe.parent,
        "breakout-bin": source_root / "Projects" / "Breakout Mmcc" / "bin" / "Release" / "net10.0",
        "gaia-bin": source_root / "Nu" / "Nu.Gaia" / "bin" / "Release" / "net10.0",
        "pipe-bin": source_root / "Nu" / "Nu.Pipe" / "bin" / "Release" / "net10.0",
    }
    output_root_receipts = {}
    for label, directory in output_roots.items():
        directory = directory.resolve(strict=True)
        selected = selected_output_files(directory)
        for current in selected:
            relative = current.relative_to(directory)
            add(current, Path("outputs") / label / relative, f"output:{label}:{relative.as_posix()}")
        output_root_receipts[label] = {
            "currentRoot": str(directory),
            "snapshotRoot": str(Path("outputs") / label),
            "fileCount": len(selected),
        }

    by_current = {entry["currentPath"]: entry for entry in entries}
    launch_bindings = {}
    for name, path in {"probe": probe, "application": application, "gameplay": gameplay}.items():
        entry = by_current.get(str(path))
        if entry is None:
            raise ValueError(f"launch binding was not selected for snapshot: {path}")
        launch_bindings[name] = {
            "currentPath": entry["currentPath"],
            "snapshotPath": entry["snapshotPath"],
            "sha256": entry["sha256"],
            "bytes": entry["bytes"],
        }
    receipt = {
        "schemaVersion": 3,
        "createdUtc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "arm": args.arm,
        "pin": PIN,
        "nativeLaunch": False,
        "snapshotRoot": str(snapshot_root),
        "copyPolicy": "ordinary copies verified byte-equal and not samefile; snapshot reuse refused",
        "toolchain": toolchain,
        "sourceManifest": {"snapshotPath": "source-manifest.json", "fileCount": ARCHIVE_FILE_COUNT, **manifest_identity},
        "outputRoots": output_root_receipts,
        "oracle": {"path": str(oracle.resolve()), **file_identity(oracle)},
        "launchBindings": launch_bindings,
        "files": entries,
    }
    atomic_json(snapshot_root / "receipt.json", receipt)
    return {"receipt": str(snapshot_root / "receipt.json"), **file_identity(snapshot_root / "receipt.json")}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("arm", choices=("v0", "v1"))
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--application", type=Path, required=True)
    parser.add_argument("--gameplay-source", type=Path, required=True)
    parser.add_argument("--build-log", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(seal(args), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
