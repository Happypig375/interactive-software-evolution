"""Install a narrow, opt-in observer bridge in an isolated pinned Gaia export.

Required Notice:
Copyright (C) Bryan Edds.
Gaia is licensed under the Nu Game Engine Noncommercial License.
https://github.com/bryanedds/Nu/blob/master/License.md
"""
import argparse
import hashlib
import json
import tarfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("source", type=Path)
parser.add_argument("archive", type=Path)
args = parser.parse_args()
source = args.source.resolve()
relative = "Nu/Nu.Gaia/Gaia.fs"
target = source / relative
with tarfile.open(args.archive) as archive:
    if archive.pax_headers.get("comment") != "064f7ae92a8506689cd91aff5e6804a375d6ef3d":
        raise SystemExit("Archive does not identify the selected Nu commit")
    original = archive.extractfile(relative).read()
if target.read_bytes() != original:
    raise SystemExit("Gaia source differs from archive; refusing to overwrite it")
body = original.decode("utf-8-sig")
anchor = "    let rec private runWithCleanUpAndErrorProtection firstFrame world ="
bridge = """    // Research-only instrumentation. No application or engine update logic changes.
    let mutable private researchPostProcess : World -> unit = ignore
    let mutable private researchCheckpoint : WorldState option = None

    let setResearchPostProcess callback = researchPostProcess <- callback

    let researchSnapshot (world : World) =
        if world.Imperative || world.Advancing then
            invalidOp "Research checkpoint must be functional and halted."
        snapshot RestorePoint world
        researchCheckpoint <- Some (snd (List.head Pasts))

    let researchUndo (world : World) =
        match researchCheckpoint, Pasts with
        | Some expected, (RestorePoint, actual) :: _ when Object.ReferenceEquals (expected, actual) ->
            tryUndo world
        | _ -> invalidOp "Research checkpoint is not the next Gaia undo target."

    let private imGuiPostProcessWithResearch world =
        imGuiPostProcess world
        researchPostProcess world

"""
call = "World.runWithoutCleanUp tautology ignore ignore imGuiRender imGuiProcess imGuiPostProcess firstFrame world"
if body.count(anchor) != 1 or body.count(call) != 1:
    raise SystemExit("Unexpected Gaia implementation; bridge anchors are not unique")
body = body.replace(anchor, bridge + anchor).replace(
    call, call.replace("imGuiPostProcess firstFrame", "imGuiPostProcessWithResearch firstFrame")
)
if not body.endswith("\n"):
    body += "\n"
target.write_text(body, encoding="utf-8", newline="")
receipt = {
    "file": relative,
    "original_sha256": hashlib.sha256(original).hexdigest(),
    "instrumented_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
    "application_sources_modified": False,
}
print(json.dumps(receipt, indent=2))
