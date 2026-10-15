"""Derive and verify the exact R10 prepared-source manifest from the pinned archive."""

import hashlib
import tarfile
from pathlib import Path, PurePosixPath

from schema_edit import GAMEPLAY_V0_SHA256, GAMEPLAY_V1_SHA256


PIN = "064f7ae92a8506689cd91aff5e6804a375d6ef3d"
ARCHIVE_SHA256 = "eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b"
ARCHIVE_BYTES = 998_277_120
ARCHIVE_FILE_COUNT = 3_240
GAIA_PATH = "Nu/Nu.Gaia/Gaia.fs"
GAMEPLAY_PATH = "Projects/Breakout Mmcc/Gameplay.fs"
GAIA_INSTRUMENTED_SHA256 = "0700ba1472a9751356ffb2d54061cd269bc4d4488e5c673858187112d2196490"


def stream_identity(stream) -> dict:
    digest = hashlib.sha256()
    size = 0
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(chunk)
        size += len(chunk)
    return {"sha256": digest.hexdigest(), "bytes": size}


def path_identity(path: Path) -> dict:
    with path.open("rb") as stream:
        return stream_identity(stream)


def safe_member_path(name: str) -> str:
    candidate = PurePosixPath(name)
    if candidate.is_absolute() or not candidate.parts or ".." in candidate.parts:
        raise ValueError(f"unsafe archive member path: {name!r}")
    normalized = candidate.as_posix()
    if normalized != name or normalized.startswith("./"):
        raise ValueError(f"noncanonical archive member path: {name!r}")
    return normalized


def resolved_source_path(source_root: Path, relative: str) -> Path:
    resolved = (source_root / Path(*PurePosixPath(relative).parts)).resolve(strict=True)
    try:
        resolved.relative_to(source_root)
    except ValueError as error:
        raise ValueError(f"source file resolves outside prepared root: {relative}") from error
    return resolved


def expected_override(path: str, arm: str, current: dict) -> tuple[str, str] | None:
    if path == GAIA_PATH:
        if current["sha256"] != GAIA_INSTRUMENTED_SHA256:
            raise ValueError("prepared Gaia.fs identity differs from the accepted bridge")
        return "instrumented-gaia", GAIA_INSTRUMENTED_SHA256
    if path == GAMEPLAY_PATH:
        expected = GAMEPLAY_V0_SHA256 if arm == "v0" else GAMEPLAY_V1_SHA256
        if current["sha256"] != expected:
            raise ValueError(f"Gameplay.fs identity differs from arm {arm}")
        return f"gameplay-{arm}", expected
    return None


def build_source_manifest(archive: Path, source_root: Path, arm: str, archive_identity: dict) -> dict:
    archive = archive.resolve(strict=True)
    source_root = source_root.resolve(strict=True)
    if arm not in ("v0", "v1"):
        raise ValueError(f"unsupported arm {arm!r}")
    if archive_identity != {"sha256": ARCHIVE_SHA256, "bytes": ARCHIVE_BYTES}:
        raise ValueError("pinned archive identity differs")
    entries = []
    seen = set()
    with tarfile.open(archive, mode="r:") as bundle:
        for member in bundle:
            if not member.isfile():
                continue
            relative = safe_member_path(member.name)
            if relative in seen:
                raise ValueError(f"duplicate archive file: {relative}")
            seen.add(relative)
            extracted = bundle.extractfile(member)
            if extracted is None:
                raise ValueError(f"archive file could not be read: {relative}")
            with extracted:
                archived = stream_identity(extracted)
            if archived["bytes"] != member.size:
                raise ValueError(f"archive member size differs: {relative}")
            current = path_identity(resolved_source_path(source_root, relative))
            override = expected_override(relative, arm, current)
            if override is None:
                accepted = archived
                override_name = None
                if current != archived:
                    raise ValueError(f"prepared source differs from pinned archive: {relative}")
            else:
                override_name, expected_hash = override
                if current["sha256"] != expected_hash:
                    raise ValueError(f"prepared override differs: {relative}")
                accepted = current
            entries.append(
                {
                    "path": relative,
                    "archiveSha256": archived["sha256"],
                    "archiveBytes": archived["bytes"],
                    "acceptedSha256": accepted["sha256"],
                    "acceptedBytes": accepted["bytes"],
                    "override": override_name,
                }
            )
    if len(entries) != ARCHIVE_FILE_COUNT:
        raise ValueError(f"pinned archive file count differs: {len(entries)}")
    entries.sort(key=lambda entry: entry["path"])
    return {
        "schemaVersion": 1,
        "pin": PIN,
        "arm": arm,
        "archive": {"path": str(archive), **archive_identity},
        "sourceRoot": str(source_root),
        "fileCount": len(entries),
        "overridePolicy": {
            GAIA_PATH: "instrumented-gaia",
            GAMEPLAY_PATH: f"gameplay-{arm}",
        },
        "entries": entries,
    }


def verify_source_manifest(manifest: dict, source_root: Path, arm: str) -> dict:
    source_root = source_root.resolve(strict=True)
    if manifest.get("schemaVersion") != 1 or manifest.get("pin") != PIN or manifest.get("arm") != arm:
        raise ValueError("source manifest schema, pin, or arm differs")
    archive = manifest.get("archive", {})
    if {"sha256": archive.get("sha256"), "bytes": archive.get("bytes")} != {
        "sha256": ARCHIVE_SHA256,
        "bytes": ARCHIVE_BYTES,
    }:
        raise ValueError("source manifest archive identity differs")
    if manifest.get("sourceRoot") != str(source_root):
        raise ValueError("source manifest root differs")
    entries = manifest.get("entries", [])
    if manifest.get("fileCount") != ARCHIVE_FILE_COUNT or len(entries) != ARCHIVE_FILE_COUNT:
        raise ValueError("source manifest file count differs")
    paths = [entry.get("path") for entry in entries]
    if len(set(paths)) != ARCHIVE_FILE_COUNT or paths != sorted(paths):
        raise ValueError("source manifest paths are duplicate or unsorted")
    expected_overrides = {GAIA_PATH: "instrumented-gaia", GAMEPLAY_PATH: f"gameplay-{arm}"}
    if manifest.get("overridePolicy") != expected_overrides:
        raise ValueError("source manifest override policy differs")
    checked_bytes = 0
    for entry in entries:
        relative = safe_member_path(entry["path"])
        override = entry.get("override")
        if relative in expected_overrides:
            if override != expected_overrides[relative]:
                raise ValueError(f"source override label differs: {relative}")
            expected_hash = GAIA_INSTRUMENTED_SHA256 if relative == GAIA_PATH else (
                GAMEPLAY_V0_SHA256 if arm == "v0" else GAMEPLAY_V1_SHA256
            )
            if entry.get("acceptedSha256") != expected_hash:
                raise ValueError(f"source override identity differs: {relative}")
        else:
            if override is not None:
                raise ValueError(f"unexpected source override: {relative}")
            if entry.get("acceptedSha256") != entry.get("archiveSha256") or entry.get("acceptedBytes") != entry.get("archiveBytes"):
                raise ValueError(f"non-override source differs from archive manifest: {relative}")
        current = path_identity(resolved_source_path(source_root, relative))
        expected = {"sha256": entry.get("acceptedSha256"), "bytes": entry.get("acceptedBytes")}
        if current != expected:
            raise ValueError(f"current prepared source differs from accepted manifest: {relative}")
        checked_bytes += current["bytes"]
    return {"fileCount": len(entries), "checkedBytes": checked_bytes, "overrides": expected_overrides}
