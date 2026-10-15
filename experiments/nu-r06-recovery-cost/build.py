"""Build the frozen R06 probe after source and parent preflight approval."""

import argparse
import collections
import hashlib
import json
import re
import shutil
import subprocess
import time
from pathlib import Path


PIN = "064f7ae92a8506689cd91aff5e6804a375d6ef3d"
SDK = "10.0.302"
REQUIRED_BINARIES = (
    "RecoveryCost.dll",
    "RecoveryCost.runtimeconfig.json",
    "RecoveryCost.deps.json",
    "Probe.dll",
    "Breakout Mmcc.dll",
    "Nu.dll",
    "Nu.Gaia.dll",
)
STAGED_SOURCES = (
    "RecoveryCost.fs",
    "RecoveryCost.fsproj",
    "global.json",
)
STAGED_B0_SOURCES = (
    "Probe.fs",
    "Probe.fsproj",
)


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def identity(path):
    return {"path": str(path.resolve()), "sha256": digest(path), "bytes": path.stat().st_size}


def same_bytes(left, right):
    return left.stat().st_size == right.stat().st_size and digest(left) == digest(right)


def tree_identity(path):
    files = []
    combined = hashlib.sha256()
    for item in sorted((item for item in path.rglob("*") if item.is_file()), key=lambda item: item.relative_to(path).as_posix()):
        relative = item.relative_to(path).as_posix()
        item_hash = digest(item)
        item_size = item.stat().st_size
        files.append({"path": relative, "sha256": item_hash, "bytes": item_size})
        combined.update(relative.encode("utf-8"))
        combined.update(b"\0")
        combined.update(str(item_size).encode("ascii"))
        combined.update(b"\0")
        combined.update(item_hash.encode("ascii"))
        combined.update(b"\n")
    return {"path": str(path.resolve()), "fileCount": len(files), "manifestSha256": combined.hexdigest(), "files": files}


def source_identities(root, here, source):
    checkpoint = root / "experiments/nu-history-b1/checkpoint"
    files = {
        "r06/RecoveryCost.fs": here / "RecoveryCost.fs",
        "r06/RecoveryCost.fsproj": here / "RecoveryCost.fsproj",
        "r06/global.json": here / "global.json",
        "r06/prepare.py": here / "prepare.py",
        "r06/build.py": here / "build.py",
        "r06/run.py": here / "run.py",
        "r06/attempt-plan.json": here / "attempt-plan.json",
        "r06/README.md": here / "README.md",
        "r06/pre-execution-contract.md": here / "pre-execution-contract.md",
        "r06/pre-build-setup-amendment-2026-10-15.md": here / "pre-build-setup-amendment-2026-10-15.md",
        "b0/Probe.fs": root / "experiments/nu-history-b0/Probe.fs",
        "b0/Probe.fsproj": root / "experiments/nu-history-b0/Probe.fsproj",
        "b0/prepare.py": root / "experiments/nu-history-b0/prepare.py",
        "b1/B1.fs": root / "experiments/nu-history-b1/B1.fs",
        "isolated/Nu/Nu.Gaia/Gaia.fs": source / "Nu/Nu.Gaia/Gaia.fs",
        "fixed/gameplay.symbol": checkpoint / "gameplay.symbol",
        "fixed/projection.json": checkpoint / "projection.json",
    }
    return {name: identity(path) for name, path in files.items()}


def main():
    here = Path(__file__).resolve().parent
    root = here.parents[1]
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--prepare-receipt", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve(strict=True)
    output = args.output.resolve()
    if output.exists():
        parser.error("output directory must be new")
    prepare_path = args.prepare_receipt.resolve(strict=True)
    prepare = json.loads(prepare_path.read_text(encoding="utf-8"))
    if prepare.get("schemaVersion") != 2 or prepare.get("status") != "passed":
        raise SystemExit("prepare receipt is not a successful R06 source receipt")
    if Path(prepare["source"]).resolve() != source:
        raise SystemExit("prepare receipt identifies a different source tree")
    gaia_hash = digest(source / "Nu/Nu.Gaia/Gaia.fs")
    if gaia_hash != prepare["gaiaBridge"]["r06WeakWitnessSha256"]:
        raise SystemExit("isolated Gaia differs from the accepted preparation receipt")
    if not prepare["finalFullArchiveComparison"]["passes"]:
        raise SystemExit("prepare receipt lacks a passing full archive comparison")

    sdk = subprocess.run(["dotnet", "--version"], cwd=here, capture_output=True, text=True, check=False)
    if sdk.returncode != 0 or sdk.stdout.strip() != SDK:
        raise SystemExit(f"required SDK {SDK}; observed {sdk.stdout.strip()!r}")
    sources_before = source_identities(root, here, source)
    output.mkdir(parents=True, exist_ok=False)
    staged_r06 = output / "projects/nu-r06-recovery-cost"
    staged_b0 = output / "projects/nu-history-b0"
    staged_r06.mkdir(parents=True)
    staged_b0.mkdir(parents=True)
    copied_sources = {}
    for name in STAGED_SOURCES:
        original = here / name
        copied = staged_r06 / name
        shutil.copyfile(original, copied)
        copied_sources[f"r06/{name}"] = {"original": original, "copy": copied}
    b0_here = root / "experiments/nu-history-b0"
    for name in STAGED_B0_SOURCES:
        original = b0_here / name
        copied = staged_b0 / name
        shutil.copyfile(original, copied)
        copied_sources[f"b0/{name}"] = {"original": original, "copy": copied}
    copied_before = {
        name: {
            "original": identity(paths["original"]),
            "copy": identity(paths["copy"]),
            "byteEqual": same_bytes(paths["original"], paths["copy"]),
        }
        for name, paths in copied_sources.items()
    }
    generated_source_directories_before = sorted(
        str(path.resolve())
        for dirname in ("bin", "obj")
        for path in source.rglob(dirname)
        if path.is_dir()
    )
    command = [
        "dotnet", "build", str(staged_r06 / "RecoveryCost.fsproj"),
        "--configuration", "Release",
        f"-p:NuSource={source}",
        f"-p:SourceRevisionId={PIN}",
    ]
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with (output / "stdout.log").open("wb") as stdout, (output / "stderr.log").open("wb") as stderr:
        completed = subprocess.run(command, cwd=staged_r06, stdout=stdout, stderr=stderr, check=False)

    stdout_text = (output / "stdout.log").read_text(encoding="utf-8", errors="replace")
    summary_marker = "Build succeeded." if "Build succeeded." in stdout_text else "Build FAILED."
    primary_output = stdout_text.split(summary_marker, 1)[0]
    warning_codes = re.findall(r": warning ([A-Z]+[0-9]+):", primary_output)
    error_codes = re.findall(r": error ([A-Z]+[0-9]+):", primary_output)

    executable_candidate = staged_r06 / "bin/Release/net10.0/RecoveryCost.dll"
    executable = executable_candidate if (
        executable_candidate.is_file()
        and (executable_candidate.parent / "RecoveryCost.runtimeconfig.json").is_file()
        and (executable_candidate.parent / "RecoveryCost.deps.json").is_file()
    ) else None
    candidates = [executable] if executable else []
    application_directory = source / "Projects/Breakout Mmcc/bin/Release/net10.0"
    application_path = application_directory / "Breakout Mmcc.dll"
    binaries = {}
    missing_binaries = []
    if executable:
        for name in REQUIRED_BINARIES:
            path = application_path if name == "Breakout Mmcc.dll" else executable.parent / name
            if path.is_file():
                binaries[name] = identity(path)
            else:
                missing_binaries.append(name)
    else:
        missing_binaries.extend(REQUIRED_BINARIES)
    probe_application_copy = executable.parent / "Breakout Mmcc.dll" if executable else None
    application_assets = application_directory / "Assets"
    application_runtime_assets = application_directory / "runtimes"
    required_application_files = (
        application_path,
        application_directory / "Breakout Mmcc.deps.json",
        application_directory / "Breakout Mmcc.runtimeconfig.json",
        application_directory / "AssetGraph.nuag",
    )
    runtime_assets = {
        "applicationFiles": {
            path.name: identity(path) for path in required_application_files if path.is_file()
        },
        "missingApplicationFiles": [str(path.resolve()) for path in required_application_files if not path.is_file()],
        "assets": tree_identity(application_assets) if application_assets.is_dir() else None,
        "runtimes": tree_identity(application_runtime_assets) if application_runtime_assets.is_dir() else None,
        "applicationAssemblyMatchesProbeCopy": bool(
            probe_application_copy
            and probe_application_copy.is_file()
            and application_path.is_file()
            and same_bytes(probe_application_copy, application_path)
        ),
        "probeApplicationCopy": identity(probe_application_copy) if probe_application_copy and probe_application_copy.is_file() else None,
    }
    runtime_assets["passes"] = bool(
        not runtime_assets["missingApplicationFiles"]
        and runtime_assets["assets"]
        and runtime_assets["assets"]["fileCount"] > 0
        and runtime_assets["runtimes"]
        and runtime_assets["runtimes"]["fileCount"] > 0
        and runtime_assets["applicationAssemblyMatchesProbeCopy"]
    )
    copied_after = {
        name: {
            "original": identity(paths["original"]),
            "copy": identity(paths["copy"]),
            "byteEqual": same_bytes(paths["original"], paths["copy"]),
        }
        for name, paths in copied_sources.items()
    }
    copied_sources_stable = copied_before == copied_after and all(
        entry["byteEqual"] for entry in copied_after.values()
    )
    sources_after = source_identities(root, here, source)
    sources_stable = sources_before == sources_after
    generated_source_directories_after = sorted(
        str(path.resolve())
        for dirname in ("bin", "obj")
        for path in source.rglob(dirname)
        if path.is_dir()
    )
    receipt = {
        "schemaVersion": 2,
        "status": "passed" if completed.returncode == 0 and executable and not missing_binaries and sources_stable and copied_sources_stable and runtime_assets["passes"] else "failed",
        "startedUtc": started,
        "command": command,
        "sdk": sdk.stdout.strip(),
        "pin": PIN,
        "exitCode": completed.returncode,
        "prepareReceipt": identity(prepare_path),
        "isolatedSource": str(source),
        "sourceIdentities": sources_after,
        "sourcesStableAcrossBuild": sources_stable,
        "copiedProjectSourcesBefore": copied_before,
        "copiedProjectSourcesAfter": copied_after,
        "copiedProjectSourcesStable": copied_sources_stable,
        "isolatedSourceGeneratedBinObjBefore": generated_source_directories_before,
        "isolatedSourceGeneratedBinObjAfter": generated_source_directories_after,
        "fixedInputs": {
            key: value for key, value in sources_after.items() if key.startswith("fixed/")
        },
        "commonBinaries": binaries,
        "probePath": binaries.get("RecoveryCost.dll", {}).get("path"),
        "applicationPath": binaries.get("Breakout Mmcc.dll", {}).get("path"),
        "runtimeAssets": runtime_assets,
        "buildDiagnostics": {
            "warningOccurrencesByCode": dict(sorted(collections.Counter(warning_codes).items())),
            "warnings": len(warning_codes),
            "errorOccurrencesByCode": dict(sorted(collections.Counter(error_codes).items())),
            "errors": len(error_codes),
            "summaryMarker": summary_marker,
        },
        "candidateProbeExecutables": [str(path.resolve()) for path in candidates],
        "missingRequiredBinaries": missing_binaries,
    }
    receipt_path = output / "build.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    if receipt["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
