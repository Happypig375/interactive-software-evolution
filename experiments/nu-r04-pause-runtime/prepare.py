"""Prepare four reference arms and five fixed fault arms without launching them."""

from __future__ import annotations

import argparse
import codecs
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tarfile


PIN = "064f7ae92a8506689cd91aff5e6804a375d6ef3d"
ARCHIVE_SHA256 = "eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b"
GAMEPLAY_SHA256 = "571e2a5ce3f0630972f2fbe4e9a6a3c376bcf4d1a74589d14c882b2ee0db1423"
SIMULANTS_SHA256 = "91f84f7f23c5ec6f4941348c4f7f425144ac57d6c036634771594fe3a79d5dcd"
WORLD_AUDIO_SHA256 = "7dee43d44ead9ead8cfff7af979e63f3d94f1c2c5509223d5d67b7b09e0496c2"
GAIA_SHA256 = "0cf653d4988ceefffd45935b37d0dcbcfb72c44bfd9ed47b3eb5ebd8ebc3b22e"
CHECKPOINT_SHA256 = "ffee72d91c6e4a32b650d45e9addd9e02e179163d0c8bbaaa8cddb9c92bc783a"
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
FAULTS = {
    "fault-missing-toggle": "missing-toggle",
    "fault-hidden-content": "hidden-content",
    "fault-advancing-time": "advancing-time",
    "fault-reset-resume": "reset-resume",
    "fault-stale-quit": "stale-quit",
}
PAUSE_ARMS = {"pause-explicit", "pause-wildcard", *FAULTS}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_source(data: bytes) -> tuple[str, bool, str]:
    bom = data.startswith(codecs.BOM_UTF8)
    text = data.decode("utf-8-sig")
    newline = "\r\n" if "\r\n" in text else "\n"
    return text, bom, newline


def write_source(path: Path, text: str, bom: bool) -> None:
    data = text.encode("utf-8")
    path.write_bytes((codecs.BOM_UTF8 if bom else b"") + data)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"{label}: expected one source anchor, found {text.count(old)}")
    return text.replace(old, new)


def install_gaia_bridge(path: Path) -> None:
    text, bom, nl = decode_source(path.read_bytes())
    anchor = "    let rec private runWithCleanUpAndErrorProtection firstFrame world ="
    bridge = nl.join([
        "    // Research-only post-content observer; no application or engine update logic changes.",
        "    let mutable private researchPostProcess : World -> unit = ignore",
        "",
        "    let setResearchPostProcess callback = researchPostProcess <- callback",
        "",
        "    let private imGuiPostProcessWithResearch world =",
        "        imGuiPostProcess world",
        "        researchPostProcess world",
        "",
        "",
    ])
    call = "World.runWithoutCleanUp tautology ignore ignore imGuiRender imGuiProcess imGuiPostProcess firstFrame world"
    text = replace_once(text, anchor, bridge + anchor, "Gaia bridge")
    text = replace_once(text, call, call.replace("imGuiPostProcess firstFrame", "imGuiPostProcessWithResearch firstFrame"), "Gaia callback")
    write_source(path, text, bom)


def install_audio_observer(path: Path) -> None:
    text, bom, nl = decode_source(path.read_bytes())
    module_anchor = f"module WorldAudio ={nl}{nl}    type World with"
    module_replacement = nl.join([
        "module WorldAudio =",
        "",
        "    // Research-only opt-in request observer. The callback must record only.",
        "    let mutable private audioMessageObserverOpt : (AudioMessage -> unit) option = None",
        "",
        "    type World with",
        "",
        "        static member setAudioMessageObserver observerOpt =",
        "            audioMessageObserverOpt <- observerOpt",
    ])
    text = replace_once(text, module_anchor, module_replacement, "audio module hook")
    single_old = nl.join([
        "        static member enqueueAudioMessage (message : AudioMessage) (world : World) =",
        "            world.Subsystems.AudioPlayer.EnqueueMessage message",
    ])
    single_new = nl.join([
        "        static member enqueueAudioMessage (message : AudioMessage) (world : World) =",
        "            world.Subsystems.AudioPlayer.EnqueueMessage message",
        "            match audioMessageObserverOpt with",
        "            | Some observer -> observer message",
        "            | None -> ()",
    ])
    plural_old = nl.join([
        "        static member enqueueAudioMessages (messages : AudioMessage seq) world =",
        "            let audioPlayer = World.getAudioPlayer world",
        "            for message in messages do audioPlayer.EnqueueMessage message",
    ])
    plural_new = nl.join([
        "        static member enqueueAudioMessages (messages : AudioMessage seq) world =",
        "            let audioPlayer = World.getAudioPlayer world",
        "            for message in messages do",
        "                audioPlayer.EnqueueMessage message",
        "                match audioMessageObserverOpt with",
        "                | Some observer -> observer message",
        "                | None -> ()",
    ])
    text = replace_once(text, single_old, single_new, "single audio enqueue")
    text = replace_once(text, plural_old, plural_new, "plural audio enqueue")
    write_source(path, text, bom)


def apply_application(path: Path, simulants_path: Path, arm: str) -> None:
    text, bom, nl = decode_source(path.read_bytes())
    terminal = "        | Playing | Quit -> gameplay"
    if arm in {"baseline-wildcard", "pause-wildcard"}:
        text = replace_once(text, terminal, "        | _ -> gameplay", f"{arm} terminal")
    if arm in PAUSE_ARMS:
        union = nl.join(["type GameplayState =", "    | Playing", "    | Quit"])
        text = replace_once(text, union, union + nl + "    | Paused", "Paused union")
        messages = nl.join(["    | FinishQuitting", "    | Update", "    | TimeUpdate"])
        text = replace_once(text, messages, nl.join(["    | FinishQuitting", "    | TogglePause", "    | Update", "    | TimeUpdate"]), "TogglePause union")
        update_handler = nl.join([
            "        | Update ->",
            "            let gameplay = Gameplay.update gameplay world",
            "            just gameplay",
            "",
            "        | TimeUpdate ->",
        ])
        toggle_handler = nl.join([
            "        | TogglePause ->",
            "            let gameplay =",
            "                if gameplay.GameplayState = Playing then { gameplay with GameplayState = Paused }",
            "                elif gameplay.GameplayState = Paused then { gameplay with GameplayState = Playing }",
            "                else gameplay",
            "            just gameplay",
            "",
        ])
        text = replace_once(text, update_handler, update_handler.replace("        | TimeUpdate ->", toggle_handler + "        | TimeUpdate ->"), "TogglePause handler")
        time_old = "            let gameplay = { gameplay with GameplayTime = gameplay.GameplayTime + gameDelta.Updates }"
        time_new = nl.join([
            "            let gameplay =",
            "                if gameplay.GameplayState = Paused then gameplay",
            "                else { gameplay with GameplayTime = gameplay.GameplayTime + gameDelta.Updates }",
        ])
        text = replace_once(text, time_old, time_new, "paused TimeUpdate")
        content_gate = nl.join(["        [// the scene group while playing", "         if gameplay.GameplayState = Playing then"])
        paused_content_gate = nl.join(["        [// the scene group while playing", "         if gameplay.GameplayState = Playing || gameplay.GameplayState = Paused then"])
        text = replace_once(text, content_gate, paused_content_gate, "paused content gate")
        quit_button = nl.join([
            "                 // quit",
            "                 Content.button Simulants.GameplayQuit.Name",
        ])
        pause_button = nl.join([
            "                 // pause / resume",
            "                 Content.button Simulants.GameplayPause.Name",
            "                    [Entity.Position == v3 232.0f -112.0f 0.0f",
            "                     Entity.Elevation == 10.0f",
            "                     Entity.Text := if gameplay.GameplayState = Paused then \"Resume\" else \"Pause\"",
            "                     Entity.ClickEvent => TogglePause]",
            "",
            "                 // quit",
            "                 Content.button Simulants.GameplayQuit.Name",
        ])
        text = replace_once(text, quit_button, pause_button, "pause content")
        if arm != "pause-wildcard":
            text = replace_once(text, terminal, "        | Playing | Quit | Paused -> gameplay", "paused explicit terminal")
        simulants, simulants_bom, _ = decode_source(simulants_path.read_bytes())
        simulants = replace_once(simulants, "    let GameplayQuit = GameplayScene / \"Quit\"", "    let GameplayQuit = GameplayScene / \"Quit\"" + nl + "    let GameplayPause = GameplayScene / \"Pause\"", "pause simulant")
        write_source(simulants_path, simulants, simulants_bom)
    write_source(path, text, bom)


def apply_fault(path: Path, arm: str) -> None:
    fault = FAULTS.get(arm)
    if fault is None:
        return
    text, bom, nl = decode_source(path.read_bytes())
    if fault == "missing-toggle":
        old = nl.join([
            "                     Entity.Text := if gameplay.GameplayState = Paused then \"Resume\" else \"Pause\"",
            "                     Entity.ClickEvent => TogglePause]",
        ])
        new = "                     Entity.Text := if gameplay.GameplayState = Paused then \"Resume\" else \"Pause\"]"
    elif fault == "hidden-content":
        old = "         if gameplay.GameplayState = Playing || gameplay.GameplayState = Paused then"
        new = "         if gameplay.GameplayState = Playing then"
    elif fault == "advancing-time":
        old = nl.join([
            "            let gameplay =",
            "                if gameplay.GameplayState = Paused then gameplay",
            "                else { gameplay with GameplayTime = gameplay.GameplayTime + gameDelta.Updates }",
        ])
        new = "            let gameplay = { gameplay with GameplayTime = gameplay.GameplayTime + gameDelta.Updates }"
    elif fault == "reset-resume":
        old = "                elif gameplay.GameplayState = Paused then { gameplay with GameplayState = Playing }"
        new = "                elif gameplay.GameplayState = Paused then Gameplay.initial"
    elif fault == "stale-quit":
        old = nl.join([
            "        | FinishQuitting ->",
            "            let gameplay = Gameplay.empty",
            "            just gameplay",
        ])
        new = nl.join([
            "        | FinishQuitting ->",
            "            just gameplay",
        ])
    else:
        raise AssertionError(fault)
    text = replace_once(text, old, new, fault)
    write_source(path, text, bom)


def main() -> int:
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("checkpoint", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    archive = args.archive.resolve(strict=True)
    checkpoint = args.checkpoint.resolve(strict=True)
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        parser.error("output must be new or empty")
    output.mkdir(parents=True, exist_ok=True)
    if digest(archive) != ARCHIVE_SHA256:
        parser.error("archive hash differs")
    if digest(checkpoint) != CHECKPOINT_SHA256:
        parser.error("checkpoint symbol hash differs")
    with tarfile.open(archive) as bundle:
        if bundle.pax_headers.get("comment") != PIN:
            parser.error("archive comment does not identify the selected commit")
    package = Path(__file__).resolve().parent
    receipts = {}
    for arm, kind in ARMS.items():
        arm_root = output / "arms" / arm
        source = arm_root / "source"
        source.mkdir(parents=True)
        extraction = subprocess.run(["tar", "-xf", str(archive), "-C", str(source)], capture_output=True, text=True)
        (arm_root / "extract.stdout.log").write_text(extraction.stdout, encoding="utf-8")
        (arm_root / "extract.stderr.log").write_text(extraction.stderr, encoding="utf-8")
        if extraction.returncode:
            raise SystemExit(f"archive extraction failed for {arm}")
        gameplay = source / "Projects/Breakout Mmcc/Gameplay.fs"
        simulants = source / "Projects/Breakout Mmcc/Simulants.fs"
        world_audio = source / "Nu/Nu/World/WorldAudio.fs"
        gaia = source / "Nu/Nu.Gaia/Gaia.fs"
        original = {"Gameplay.fs": digest(gameplay), "Simulants.fs": digest(simulants), "WorldAudio.fs": digest(world_audio), "Gaia.fs": digest(gaia)}
        expected = {"Gameplay.fs": GAMEPLAY_SHA256, "Simulants.fs": SIMULANTS_SHA256, "WorldAudio.fs": WORLD_AUDIO_SHA256, "Gaia.fs": GAIA_SHA256}
        if original != expected:
            raise SystemExit(f"{arm}: extracted source hashes differ: {original}")
        install_gaia_bridge(gaia)
        install_audio_observer(world_audio)
        apply_application(gameplay, simulants, arm)
        apply_fault(gameplay, arm)
        probe = arm_root / "probe"
        probe.mkdir()
        for name in ["Probe.fsproj", "Common.fs", "BaselineProbe.fs", "PauseProbe.fs"]:
            shutil.copy2(package / name, probe / name)
        receipts[arm] = {
            "probe_kind": kind,
            "fault": FAULTS.get(arm),
            "original": original,
            "instrumented": {"Gameplay.fs": digest(gameplay), "Simulants.fs": digest(simulants), "WorldAudio.fs": digest(world_audio), "Gaia.fs": digest(gaia)},
            "probe_sources": {name: digest(probe / name) for name in ["Probe.fsproj", "Common.fs", "BaselineProbe.fs", "PauseProbe.fs"]},
        }
    pause_common = [receipts[name]["instrumented"][file] for name in ("pause-explicit", "pause-wildcard") for file in ("Simulants.fs", "WorldAudio.fs", "Gaia.fs")]
    if pause_common[0:3] != pause_common[3:6]:
        raise SystemExit("pause arms do not share identical common sources/instrumentation")
    baseline_instrumentation = [receipts[name]["instrumented"][file] for name in ("baseline-explicit", "baseline-wildcard") for file in ("Simulants.fs", "WorldAudio.fs", "Gaia.fs")]
    if baseline_instrumentation[0:3] != baseline_instrumentation[3:6]:
        raise SystemExit("baseline arms do not share identical non-treatment sources/instrumentation")
    fault_diffs = output / "variant-diffs"
    fault_diffs.mkdir()
    reference_source = output / "arms/pause-explicit/source"
    for arm, fault in FAULTS.items():
        for file in ("Simulants.fs", "WorldAudio.fs", "Gaia.fs"):
            if receipts[arm]["instrumented"][file] != receipts["pause-explicit"]["instrumented"][file]:
                raise SystemExit(f"{arm}: non-fault source {file} differs from pause-explicit")
        if receipts[arm]["probe_sources"] != receipts["pause-explicit"]["probe_sources"]:
            raise SystemExit(f"{arm}: probe sources differ from pause-explicit")
        if receipts[arm]["instrumented"]["Gameplay.fs"] == receipts["pause-explicit"]["instrumented"]["Gameplay.fs"]:
            raise SystemExit(f"{arm}: Gameplay fault was not applied")
        reference_text = (reference_source / "Projects/Breakout Mmcc/Gameplay.fs").read_text(encoding="utf-8-sig").splitlines()
        fault_text = (output / "arms" / arm / "source/Projects/Breakout Mmcc/Gameplay.fs").read_text(encoding="utf-8-sig").splitlines()
        patch = "\n".join(difflib.unified_diff(reference_text, fault_text, fromfile="a/Projects/Breakout Mmcc/Gameplay.fs", tofile=f"b/{arm}/Gameplay.fs", lineterm="")) + "\n"
        patch_path = fault_diffs / f"{fault}.patch"
        patch_path.write_text(patch, encoding="utf-8", newline="\n")
        receipts[arm]["fault_patch_sha256"] = digest(patch_path)
        receipts[arm]["source_delta_files"] = ["Projects/Breakout Mmcc/Gameplay.fs"]
    receipt = {"pin": PIN, "archive_sha256": digest(archive), "checkpoint_sha256": digest(checkpoint), "arms": receipts}
    (output / "prepare-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
