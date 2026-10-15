"""Extract and instrument a fresh exact Nu tree for the R10 schema probe."""

import argparse
import hashlib
import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path


PIN = "064f7ae92a8506689cd91aff5e6804a375d6ef3d"
ARCHIVE_SHA256 = "eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b"
ARCHIVE_BYTES = 998_277_120
GAIA_ORIGINAL_SHA256 = "0cf653d4988ceefffd45935b37d0dcbcfb72c44bfd9ed47b3eb5ebd8ebc3b22e"
GAIA_INSTRUMENTED_SHA256 = "0700ba1472a9751356ffb2d54061cd269bc4d4488e5c673858187112d2196490"
GAMEPLAY_V0_SHA256 = "571e2a5ce3f0630972f2fbe4e9a6a3c376bcf4d1a74589d14c882b2ee0db1423"


def identity(path: Path) -> dict:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return {
        "path": str(path),
        "sha256": digest.hexdigest(),
        "bytes": size,
    }


parser = argparse.ArgumentParser()
parser.add_argument("archive", type=Path)
parser.add_argument("artifact", type=Path)
args = parser.parse_args()

archive = args.archive.resolve(strict=True)
artifact = args.artifact.resolve()
if artifact.exists():
    raise SystemExit("artifact directory must not already exist")
archive_identity = identity(archive)
if (
    archive_identity["sha256"] != ARCHIVE_SHA256
    or archive_identity["bytes"] != ARCHIVE_BYTES
):
    raise SystemExit(
        "archive identity differs: expected "
        f"{ARCHIVE_BYTES} bytes / {ARCHIVE_SHA256}, got "
        f"{archive_identity['bytes']} / {archive_identity['sha256']}"
    )

artifact.mkdir(parents=True)
source = artifact / "source"
source.mkdir()
with tarfile.open(archive) as bundle:
    bundle.extractall(source, filter="data")

gaia = source / "Nu/Nu.Gaia/Gaia.fs"
gameplay = source / "Projects/Breakout Mmcc/Gameplay.fs"
before_gaia = identity(gaia)
before_gameplay = identity(gameplay)
if before_gaia["sha256"] != GAIA_ORIGINAL_SHA256:
    raise SystemExit("pristine Gaia.fs identity differs")
if before_gameplay["sha256"] != GAMEPLAY_V0_SHA256:
    raise SystemExit("pristine Gameplay.fs identity differs")

game_text = gameplay.read_text(encoding="utf-8-sig")
v0_anchors = {
    "seven_field_record": "      Score : int\n      Lives : int }",
    "empty_lives": "          Score = 0\n          Lives = 0 }",
    "score_literal": "                let scoring = Map.count bricksIntersected * 100",
}
for name, anchor in v0_anchors.items():
    if game_text.count(anchor) != 1:
        raise SystemExit(f"unexpected pristine Gameplay anchor: {name}")
if "BrickReward" in game_text:
    raise SystemExit("pristine Gameplay.fs unexpectedly contains BrickReward")

gaia_text = gaia.read_text(encoding="utf-8-sig")
session_anchor = (
    "    let mutable private FsiSession = "
    "Unchecked.defaultof<Shell.FsiEvaluationSession>\n"
)
if gaia_text.count(session_anchor) != 1:
    raise SystemExit("unexpected FsiSession anchor")
gaia_text = gaia_text.replace(
    session_anchor,
    session_anchor + "    let mutable private ResearchGeneratedScript = \"\"\n",
)

script_anchor = (
    "                        String.Join (\"\\n\", Array.map "
    "(fun (filePath : string) -> \"#load \\\"../../../\" + filePath + "
    "\"\\\"\") fsprojFsFilePaths)\n\n"
    "                    // dispose of existing fsi eval session"
)
if gaia_text.count(script_anchor) != 1:
    raise SystemExit("unexpected generated-script anchor")
gaia_text = gaia_text.replace(
    script_anchor,
    script_anchor.replace(
        "\n\n                    // dispose",
        "\n                    ResearchGeneratedScript <- fsxFileString"
        "\n\n                    // dispose",
    ),
)

reload_anchor = "    let private tryReloadAll initializing world ="
bridge = '''    // Research-only bridge: guarded access to the ordinary reload core plus its exact generated script.
    let researchReloadCode (world : World) =
        if world.Imperative || world.Advancing then
            invalidOp "Research reload requires a functional halted world."
        if not (World.getAllowCodeReload world) then
            invalidOp "Code reload is disabled by the selected plugin."
        let requireFieldInfo name (owner : obj) =
            let field = owner.GetType().GetField (name, BindingFlags.NonPublic ||| BindingFlags.Instance)
            if isNull field then invalidOp ("Missing FSI private field: " + name)
            field
        let requireFieldValue name (owner : obj) =
            let field = requireFieldInfo name owner
            let value = field.GetValue owner
            if isNull value then invalidOp ("Null FSI private field: " + name)
            value
        let compiler = requireFieldValue "fsiDynamicCompiler" FsiSession
        requireFieldInfo "resolveAssemblyRef" compiler |> ignore
        let config = requireFieldValue "tcConfigB" FsiSession
        requireFieldInfo "tryGetMetadataSnapshot@" config |> ignore
        ResearchGeneratedScript <- ""
        tryReloadCode false world
        (ResearchGeneratedScript, FsiSession.DynamicAssemblies)

'''
if gaia_text.count(reload_anchor) != 1:
    raise SystemExit("unexpected reload bridge anchor")
gaia_text = gaia_text.replace(reload_anchor, bridge + reload_anchor)

run_anchor = "    let rec private runWithCleanUpAndErrorProtection firstFrame world ="
observer = '''    // Research-only postprocess access. No application update logic changes.
    let mutable private researchPostProcess : World -> unit = ignore
    let setResearchPostProcess callback = researchPostProcess <- callback
    let private imGuiPostProcessWithResearch world =
        imGuiPostProcess world
        researchPostProcess world

'''
postprocess_call = (
    "World.runWithoutCleanUp tautology ignore ignore imGuiRender imGuiProcess "
    "imGuiPostProcess firstFrame world"
)
if gaia_text.count(run_anchor) != 1 or gaia_text.count(postprocess_call) != 1:
    raise SystemExit("unexpected postprocess anchors")
gaia_text = gaia_text.replace(run_anchor, observer + run_anchor).replace(
    postprocess_call,
    postprocess_call.replace(
        "imGuiPostProcess firstFrame", "imGuiPostProcessWithResearch firstFrame"
    ),
)
gaia.write_text(gaia_text, encoding="utf-8", newline="")

after_gaia = identity(gaia)
after_gameplay = identity(gameplay)
if after_gaia["sha256"] != GAIA_INSTRUMENTED_SHA256:
    raise SystemExit("instrumented Gaia.fs identity differs from accepted bridge")
if after_gameplay != before_gameplay:
    raise SystemExit("preparer changed Gameplay.fs")

receipt = {
    "schemaVersion": 1,
    "createdUtc": datetime.now(timezone.utc).isoformat(),
    "pin": PIN,
    "archive": archive_identity,
    "source": str(source),
    "sourceFileCount": sum(1 for path in source.rglob("*") if path.is_file()),
    "originals": {"Gaia.fs": before_gaia, "Gameplay.fs": before_gameplay},
    "prepared": {"Gaia.fs": after_gaia, "Gameplay.fs": after_gameplay},
    "gaiaMatchesAcceptedInstrumentedBridge": True,
    "gameplayIsPristineSevenFieldV0": True,
    "nativeRun": False,
}
(artifact / "prepare-receipt.json").write_text(
    json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, indent=2))
