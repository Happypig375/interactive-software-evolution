"""Create and instrument a fresh exact Nu source archive for the R10 probe."""
import argparse, hashlib, json, shutil, subprocess, tarfile
from pathlib import Path

PIN = "064f7ae92a8506689cd91aff5e6804a375d6ef3d"
ARCHIVE_SHA256 = "eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b"

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

p = argparse.ArgumentParser()
p.add_argument("nu_repo", type=Path)
p.add_argument("artifact", type=Path)
p.add_argument("--archive", type=Path, help="reuse a previously preserved exact git archive")
a = p.parse_args()
repo, art = a.nu_repo.resolve(), a.artifact.resolve()
if art.exists(): raise SystemExit("artifact directory must not exist")
art.mkdir(parents=True)
archive, source = (a.archive.resolve(strict=True) if a.archive else art / "nu-pin.tar"), art / "source"
if not a.archive:
    subprocess.run(["git", "-C", str(repo), "archive", "--format=tar", "-o", str(archive), PIN], check=True)
archive_sha256 = sha(archive)
if archive_sha256 != ARCHIVE_SHA256:
    raise SystemExit(f"archive SHA-256 differs: expected {ARCHIVE_SHA256}, got {archive_sha256}")
source.mkdir()
with tarfile.open(archive) as tf:
    tf.extractall(source, filter="data")

gaia = source / "Nu/Nu.Gaia/Gaia.fs"
game = source / "Projects/Breakout Mmcc/Gameplay.fs"
originals = {"Gaia.fs": sha(gaia), "Gameplay.fs": sha(game)}

g = gaia.read_text(encoding="utf-8-sig")
session_anchor = "    let mutable private FsiSession = Unchecked.defaultof<Shell.FsiEvaluationSession>\n"
if g.count(session_anchor) != 1: raise SystemExit("unexpected FsiSession anchor")
g = g.replace(session_anchor, session_anchor + "    let mutable private ResearchGeneratedScript = \"\"\n")

script_anchor = "                        String.Join (\"\\n\", Array.map (fun (filePath : string) -> \"#load \\\"../../../\" + filePath + \"\\\"\") fsprojFsFilePaths)\n\n                    // dispose of existing fsi eval session"
if g.count(script_anchor) != 1: raise SystemExit("unexpected generated-script anchor")
g = g.replace(script_anchor, script_anchor.replace("\n\n                    // dispose", "\n                    ResearchGeneratedScript <- fsxFileString\n\n                    // dispose"))

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
if g.count(reload_anchor) != 1: raise SystemExit("unexpected reload bridge anchor")
g = g.replace(reload_anchor, bridge + reload_anchor)

run_anchor = "    let rec private runWithCleanUpAndErrorProtection firstFrame world ="
observer = '''    // Research-only postprocess access. No application update logic changes.
    let mutable private researchPostProcess : World -> unit = ignore
    let setResearchPostProcess callback = researchPostProcess <- callback
    let private imGuiPostProcessWithResearch world =
        imGuiPostProcess world
        researchPostProcess world

'''
call = "World.runWithoutCleanUp tautology ignore ignore imGuiRender imGuiProcess imGuiPostProcess firstFrame world"
if g.count(run_anchor) != 1 or g.count(call) != 1: raise SystemExit("unexpected postprocess anchors")
g = g.replace(run_anchor, observer + run_anchor).replace(call, call.replace("imGuiPostProcess firstFrame", "imGuiPostProcessWithResearch firstFrame"))
gaia.write_text(g, encoding="utf-8", newline="")

b = game.read_text(encoding="utf-8-sig")
record_anchor = "      Score : int\n      Lives : int }\n\n    // this represents the gameplay model"
record_replacement = "      Score : int\n      Lives : int }\n\n    static member BrickReward = 100\n\n    // this represents the gameplay model"
score_anchor = "                let scoring = Map.count bricksIntersected * 100"
if b.count(record_anchor) != 1 or b.count(score_anchor) != 1: raise SystemExit("unexpected Gameplay anchors")
b = b.replace(record_anchor, record_replacement).replace(score_anchor, "                let scoring = Map.count bricksIntersected * Gameplay.BrickReward")
game.write_text(b, encoding="utf-8", newline="")

receipt = {
    "pin": PIN, "archive_sha256": archive_sha256, "source": str(source),
    "originals": originals,
    "instrumented": {"Gaia.fs": sha(gaia), "Gameplay.fs": sha(game)},
    "gameplay_literal": 100,
}
(art / "prepare-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
