"""Create and verify the isolated exact-pin source tree for the R06 probe."""

import argparse
import difflib
import hashlib
import json
import subprocess
import sys
import tarfile
from pathlib import Path


PIN = "064f7ae92a8506689cd91aff5e6804a375d6ef3d"
ARCHIVE_SHA256 = "eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b"
GAIA_RELATIVE = "Nu/Nu.Gaia/Gaia.fs"
ORIGINAL_GAIA_SHA256 = "0cf653d4988ceefffd45935b37d0dcbcfb72c44bfd9ed47b3eb5ebd8ebc3b22e"
GENERATED_DIRECTORY_NAMES = {"bin", "obj", ".vs", ".idea"}


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def digest_bytes(body):
    return hashlib.sha256(body).hexdigest()


def tree_comparison(archive, source, allowed_differences):
    missing = []
    differences = []
    allowed = []
    archive_names = set()
    archive_manifest = hashlib.sha256()
    source_manifest = hashlib.sha256()
    with tarfile.open(archive) as bundle:
        members = [member for member in bundle.getmembers() if member.isfile()]
        for member in members:
            name = member.name
            archive_names.add(name)
            archive_body = bundle.extractfile(member).read()
            archive_hash = digest_bytes(archive_body)
            archive_manifest.update(f"{name}\0{archive_hash}\n".encode())
            path = source / name
            if not path.is_file():
                missing.append(name)
                continue
            source_hash = digest(path)
            source_manifest.update(f"{name}\0{source_hash}\n".encode())
            if source_hash != archive_hash:
                entry = {"path": name, "archiveSha256": archive_hash, "sourceSha256": source_hash}
                if name in allowed_differences and source_hash == allowed_differences[name]:
                    allowed.append(entry)
                else:
                    differences.append(entry)
    unexpected_tracked = []
    unexpected_generated = []
    for path in source.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        name = relative.as_posix()
        if name in archive_names:
            continue
        if any(part in GENERATED_DIRECTORY_NAMES for part in relative.parts):
            unexpected_generated.append(name)
        else:
            unexpected_tracked.append(name)
    return {
        "archiveRegularFileCount": len(archive_names),
        "archiveManifestSha256": archive_manifest.hexdigest(),
        "sourceManifestSha256": source_manifest.hexdigest(),
        "missingArchiveMembers": missing,
        "unexpectedTrackedSourceFiles": unexpected_tracked,
        "unexpectedGeneratedFiles": unexpected_generated,
        "unreviewedDifferences": differences,
        "reviewedExceptions": allowed,
        "passes": not missing and not unexpected_tracked and not differences,
    }


def install_weak_witness(gaia):
    before = gaia.read_text(encoding="utf-8-sig")
    replacements = [
        (
            "    let mutable private researchCheckpoint : WorldState option = None",
            "    let mutable private researchCheckpoint : WeakReference<WorldState> option = None",
        ),
        (
            "        researchCheckpoint <- Some (snd (List.head Pasts))",
            "        researchCheckpoint <- Some (WeakReference<WorldState> (snd (List.head Pasts)))",
        ),
        (
            """        match researchCheckpoint, Pasts with
        | Some expected, (RestorePoint, actual) :: _ when Object.ReferenceEquals (expected, actual) ->
            tryUndo world
        | _ -> invalidOp \"Research checkpoint is not the next Gaia undo target.\"""",
            """        match researchCheckpoint, Pasts with
        | Some expectedWeak, (RestorePoint, actual) :: _ ->
            let mutable expected = Unchecked.defaultof<WorldState>
            if expectedWeak.TryGetTarget &expected && Object.ReferenceEquals (expected, actual)
            then tryUndo world
            else invalidOp \"Research checkpoint is not the next Gaia undo target.\"
        | _ -> invalidOp \"Research checkpoint is not the next Gaia undo target.\"""",
        ),
    ]
    after = before
    for old, new in replacements:
        if after.count(old) != 1:
            raise RuntimeError("reviewed B0 weak-witness replacement anchor is not unique")
        after = after.replace(old, new)
    gaia.write_text(after, encoding="utf-8", newline="")
    return replacements


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("source", type=Path, help="new isolated source directory")
    parser.add_argument("archive", type=Path)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    archive = args.archive.resolve(strict=True)
    receipt = args.receipt.resolve()
    if source.exists():
        parser.error("source directory must be new")
    if receipt.exists():
        parser.error("receipt path must be new")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "schemaVersion": 2,
        "status": "failed",
        "pin": PIN,
        "archive": str(archive),
        "archiveSha256": digest(archive),
        "source": str(source),
        "gaiaRelativePath": GAIA_RELATIVE,
        "applicationSourcesModified": False,
    }
    try:
        if result["archiveSha256"] != ARCHIVE_SHA256:
            raise RuntimeError("archive hash differs from the frozen contract")
        with tarfile.open(archive) as bundle:
            if bundle.pax_headers.get("comment") != PIN:
                raise RuntimeError("archive does not identify the selected Nu pin")
            original_gaia = bundle.extractfile(GAIA_RELATIVE).read()
            if digest_bytes(original_gaia) != ORIGINAL_GAIA_SHA256:
                raise RuntimeError("archive Gaia bytes differ from the reviewed original")
            source.mkdir(parents=True, exist_ok=False)
            bundle.extractall(source, filter="data")
        exact = tree_comparison(archive, source, {})
        result["postExtractionComparison"] = exact
        if not exact["passes"]:
            raise RuntimeError("fresh extraction differs from the full archive member set")

        bridge = here.parent / "nu-history-b0" / "prepare.py"
        completed = subprocess.run(
            [sys.executable, str(bridge), str(source), str(archive)],
            cwd=here.parent.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        result["b0BridgeInstaller"] = {
            "path": str(bridge),
            "sha256": digest(bridge),
            "exitCode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
        if completed.returncode != 0:
            raise RuntimeError("reviewed B0 bridge installer failed")

        gaia = source / GAIA_RELATIVE
        b0_gaia_hash = digest(gaia)
        replacements = install_weak_witness(gaia)
        r06_gaia_hash = digest(gaia)
        diff_path = receipt.with_name(receipt.stem + "-gaia-r06.diff")
        if diff_path.exists():
            raise RuntimeError("Gaia diff path must be new")
        diff_lines = difflib.unified_diff(
            original_gaia.decode("utf-8-sig").splitlines(),
            gaia.read_text(encoding="utf-8-sig").splitlines(),
            fromfile=f"archive/{GAIA_RELATIVE}",
            tofile=f"r06/{GAIA_RELATIVE}",
            lineterm="",
        )
        diff_text = "\n".join(diff_lines) + "\n"
        diff_path.write_text(diff_text, encoding="utf-8", newline="")
        result["gaiaBridge"] = {
            "archiveSha256": ORIGINAL_GAIA_SHA256,
            "reviewedB0Sha256": b0_gaia_hash,
            "r06WeakWitnessSha256": r06_gaia_hash,
            "weakWitnessReplacementCount": len(replacements),
            "byteNormalization": "Retained B0 installer converts the archive UTF-8 BOM/CRLF file to UTF-8 without BOM/LF; the diff is line-ending-normalized while the exact byte hashes remain authoritative.",
            "diff": str(diff_path),
            "diffSha256": digest(diff_path),
        }
        final = tree_comparison(archive, source, {GAIA_RELATIVE: r06_gaia_hash})
        result["finalFullArchiveComparison"] = final
        if not final["passes"] or len(final["reviewedExceptions"]) != 1:
            raise RuntimeError("prepared source differs outside the one reviewed R06 Gaia exception")
        result["status"] = "passed"
    except Exception as error:
        result["errorType"] = type(error).__name__
        result["error"] = str(error)
    receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
