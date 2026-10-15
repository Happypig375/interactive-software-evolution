"""Prepare one fresh pinned source graph and two standalone lifecycle probes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tarfile


PIN = "064f7ae92a8506689cd91aff5e6804a375d6ef3d"
ARCHIVE_SHA256 = "eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b"
APP_MANIFESTS = {
    "mmcc": {"directory": "Projects/Breakout Mmcc", "files": 159, "sha256": "04be72819f6c40e87dd71ade056e0ecdff7520b1823c00384781c4956db8747f"},
    "imsim": {"directory": "Projects/Breakout ImSim", "files": 158, "sha256": "d3217d7fe6b2cf9dc9d3708f57ae831d855f10cfbcb2cd3b68f12e9391a0e7da"},
}
PROBE_FILES = ("global.json", "Probe.fsproj", "Common.fs", "Probe.fs", "pre-execution-contract.md", "initializer-diagnostic-addendum.md")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(root: Path, *, exclude_build: bool = False) -> list[dict[str, object]]:
    rows = []
    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root)
        if exclude_build and {"bin", "obj", "refinement"}.intersection(relative.parts):
            continue
        rows.append({"path": relative.as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)})
    return rows


def manifest_digest(rows: list[dict[str, object]]) -> str:
    body = "".join(f"{row['sha256']}  {row['path']}\n" for row in rows).encode("utf-8")
    return hashlib.sha256(body).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    archive = args.archive.resolve(strict=True)
    output = args.output.resolve()
    if output.exists():
        parser.error("output must not exist")
    if digest(archive) != ARCHIVE_SHA256:
        parser.error("archive hash differs")
    with tarfile.open(archive) as bundle:
        if bundle.pax_headers.get("comment") != PIN:
            parser.error("archive comment does not identify the selected pin")

    output.mkdir(parents=True)
    source = output / "source"
    source.mkdir()
    extraction = subprocess.run(["tar", "-xf", str(archive), "-C", str(source)], capture_output=True, text=True)
    (output / "extract.stdout.log").write_text(extraction.stdout, encoding="utf-8")
    (output / "extract.stderr.log").write_text(extraction.stderr, encoding="utf-8")
    if extraction.returncode:
        raise SystemExit("archive extraction failed")

    source_rows = manifest(source)
    (output / "source-input-manifest.json").write_text(json.dumps(source_rows, indent=2) + "\n", encoding="utf-8")
    app_results = {}
    for arm, expected in APP_MANIFESTS.items():
        rows = manifest(source / str(expected["directory"]), exclude_build=True)
        actual = {"files": len(rows), "sha256": manifest_digest(rows)}
        if actual != {"files": expected["files"], "sha256": expected["sha256"]}:
            raise SystemExit(f"{arm} unchanged application manifest differs: {actual}")
        app_manifest = output / f"{arm}-unchanged-application-manifest.json"
        app_manifest.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
        app_results[arm] = actual | {
            "manifest": {
                "path": app_manifest.relative_to(output).as_posix(),
                "bytes": app_manifest.stat().st_size,
                "sha256": digest(app_manifest),
            }
        }

    package = Path(__file__).resolve().parent
    public_inputs = {}
    for name in PROBE_FILES + ("prepare.py", "build.py", "run.py"):
        path = package / name
        public_inputs[name] = {"bytes": path.stat().st_size, "sha256": digest(path)}
    for arm in APP_MANIFESTS:
        probe = output / "arms" / arm / "probe"
        probe.mkdir(parents=True)
        for name in PROBE_FILES:
            shutil.copy2(package / name, probe / name)

    receipt = {
        "pin": PIN,
        "archive": {"path": str(archive), "bytes": archive.stat().st_size, "sha256": ARCHIVE_SHA256},
        "source_manifest": {"path": "source-input-manifest.json", "files": len(source_rows), "sha256": digest(output / "source-input-manifest.json")},
        "unchanged_application_manifests": app_results,
        "application_manifest_normalization": {
            "ordering": "ordinal ascending POSIX relative path",
            "excluded_path_components": ["bin", "obj", "refinement"],
            "aggregate": "SHA-256 of concatenated UTF-8 lowercase-sha256 + two spaces + POSIX path + LF",
            "per_file_fields": ["path", "bytes", "sha256"],
        },
        "public_inputs": public_inputs,
        "arms": ["mmcc", "imsim"],
        "source_copies": 1,
    }
    (output / "prepare-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
