"""Static, synthetic, sealing, and cleanup checks; never launches Nu."""

import argparse
import copy
import hashlib
import json
import os
import py_compile
import subprocess
import sys
from pathlib import Path

import compare as comparator
import run as runner
from schema_edit import GAMEPLAY_V0_SHA256, GAMEPLAY_V1_SHA256, derive_v1
from seal_build import atomic_json, copy_entry, file_identity, verify_output_roots, verify_receipt
from source_manifest import verify_source_manifest


CONTRACT_SHA256 = "4c6bc39e4927c593f14026373d8e1a147a721c15dc1228a260c1643cf0006076"
AMENDMENT_SHA256 = "8ac641cedeb4d130773d70e8367e3effb285f1a6f670f1ca8975ad284a5a8465"
ORACLE_SHA256 = "327d804d8d780f70894476267f0995554764798309b6a5fa1b88c1fe69b1cb2c"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_trace(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8", newline="\n")


def projection_templates() -> tuple[dict, dict, dict]:
    checkpoint = {
        "names": ["@455", "Ball", "Life+0", "Life+1", "Life+2", "Life+3", "Life+4", "Paddle", "Score"],
        "paddle": {"name": "Paddle", "exists": True},
        "ball": {"name": "Ball", "exists": True},
        "bricks": [{"name": "@455", "exists": True}],
        "scoreText": "Score: 100",
        "messageText": "",
        "rotation": ["checkpoint"],
    }
    zero = {
        "names": ["Ball", "Life+0", "Life+1", "Life+2", "Life+3", "Life+4", "Paddle", "Score"],
        "paddle": {"name": "Paddle", "exists": True},
        "ball": {"name": "Ball", "exists": True},
        "bricks": [],
        "scoreText": "Score: 100",
        "messageText": "",
        "rotation": ["post"],
    }
    two_hundred = copy.deepcopy(zero)
    two_hundred["scoreText"] = "Score: 300"
    return checkpoint, zero, two_hundred


def arm_rows(
    mode: str,
    oracle: dict,
    reward: int,
    preservation: bool = True,
    continue_once: bool = True,
) -> list[dict]:
    checkpoint_projection, projection_zero, projection_200 = projection_templates()
    checkpoint = copy.deepcopy(oracle["checkpoint"])
    model_zero = copy.deepcopy(oracle["expected_post_reward_zero"])
    model_200 = copy.deepcopy(oracle["expected_post_reward_200"])
    precomputed = {
        "event": "precomputed-oracle",
        "checkpointModelJson": json.dumps(checkpoint, separators=(",", ":")),
        "checkpointProjectionJson": json.dumps(checkpoint_projection, separators=(",", ":")),
        "expectedModelZeroJson": json.dumps(model_zero, separators=(",", ":")),
        "expectedModel200Json": json.dumps(model_200, separators=(",", ":")),
        "expectedProjectionZeroJson": json.dumps(projection_zero, separators=(",", ":")),
        "expectedProjection200Json": json.dumps(projection_200, separators=(",", ":")),
        "rewardCasesPrecomputed": 1001,
    }
    schema = comparator.OLD_SCHEMA if mode == "live" else comparator.NEW_SCHEMA
    checkpoint_row = {
        "event": "checkpoint-halted",
        "fieldNames": schema,
        "model": checkpoint,
        "projection": checkpoint_projection,
        "projectionErrors": [],
        "reward": None if mode == "live" else 200,
        "updates": 0,
        "timeUpdates": 0,
        "leftInputs": 0,
        "rightInputs": 0,
    }
    rows = [
        {
            "event": "configuration",
            "mode": mode,
            "runtime": comparator.EXPECTED_FRAMEWORK,
            "os": "Microsoft Windows 10.0.19045",
            "architecture": comparator.EXPECTED_ARCHITECTURE,
        }
    ]
    if mode == "fresh":
        rows.append({"event": "fresh-initial-model", "fieldNames": comparator.NEW_SCHEMA, "reward": 200})
    rows.extend([
        {
            "event": "oracle-data-controls",
            "resetRejected": True,
            "alteredOldFieldRejected": True,
            "wrongBrickRejected": True,
            "wrongScoreRejected": True,
            "zeroVersus200Rejected": True,
            "rewardCasesPrecomputed": 1001,
        },
        precomputed,
        checkpoint_row,
    ])
    required_reward = reward == 200
    mapping = required_reward and preservation if mode == "live" else False
    if mode == "live":
        rows.extend(
            [
                {"event": "reload-start", "fieldNames": comparator.OLD_SCHEMA, "brickRewardPresent": False},
                {
                    "event": "fsi-assemblies",
                    "assemblies": [{"mvid": "model-mvid"}, {"mvid": "dispatcher-mvid"}],
                },
                {
                    "event": "reload-installed",
                    "fieldNames": comparator.NEW_SCHEMA,
                    "actualType": "FSI_1.Breakout.Gameplay",
                    "dispatcherModelType": "FSI_1.Breakout.Gameplay",
                    "actualAssembly": {"mvid": "model-mvid"},
                    "dispatcherAssembly": {"mvid": "dispatcher-mvid"},
                    "observedReward": reward,
                    "rewardInRange": 0 <= reward <= 1000,
                    "requiredRewardInstalled": required_reward,
                    "preservationPass": preservation,
                    "mappingRequirementPass": mapping,
                },
                {
                    "event": "post-reload-pre-advance",
                    "fieldNames": comparator.NEW_SCHEMA,
                    "model": checkpoint if preservation else {**checkpoint, "lives": 4},
                    "projection": checkpoint_projection,
                    "projectionErrors": [],
                    "reward": reward,
                    "codeReloadEvents": 1,
                    "updates": 0,
                    "timeUpdates": 0,
                    "leftInputs": 0,
                    "rightInputs": 0,
                },
            ]
        )
    continuation_attempted = continue_once and preservation
    if continuation_attempted:
        expected_model = copy.deepcopy(model_zero)
        expected_model["score"] = 100 + reward
        expected_projection = copy.deepcopy(projection_zero)
        expected_projection["scoreText"] = f"Score: {100 + reward}"
        rows.extend(
            [
                {"event": "resume-request"},
                {
                    "event": "event-schedule",
                    "order": ["TimeUpdate", "Update"],
                    "gameDeltaUpdates": [1],
                    "updates": 1,
                    "timeUpdates": 1,
                    "leftInputs": 0,
                    "rightInputs": 0,
                },
                {
                    "event": "post-update-halted",
                    "fieldNames": comparator.NEW_SCHEMA,
                    "model": expected_model,
                    "projection": expected_projection,
                    "projectionErrors": [],
                    "reward": reward,
                },
                {
                    "event": "next-halted-stable",
                    "fieldNames": comparator.NEW_SCHEMA,
                    "model": expected_model,
                    "projection": expected_projection,
                    "projectionErrors": [],
                    "reward": reward,
                },
            ]
        )
    matched = (
        mapping and continuation_attempted
        if mode == "live"
        else preservation and continuation_attempted
    )
    rows.append(
        {
            "event": "result",
            "mode": mode,
            "processPass": True,
            "requiredRewardInstalled": required_reward,
            "mappingRequirementPass": mapping,
            "preservationPass": preservation,
            "continuationAttempted": continuation_attempted,
            "continuationPass": continuation_attempted,
            "freshInitializationPass": mode == "fresh",
            "freshInitializationApplicable": mode == "fresh",
            "freshInitialReward": 200 if mode == "fresh" else -1,
            "observedReward": reward,
            "rewardInRange": (0 <= reward <= 1000) if mode == "live" else preservation,
            "matchedRequirementPass": matched,
            "updates": 1 if continuation_attempted else 0,
            "timeUpdates": 1 if continuation_attempted else 0,
            "leftInputs": 0,
            "rightInputs": 0,
        }
    )
    rows.append({"event": "engine-exit", "exitCode": 0, "done": True, "processPassed": True})
    return rows


def expect_rejected(live_rows: list[dict], fresh_rows: list[dict], directory: Path, name: str) -> bool:
    case = directory / name
    case.mkdir()
    live, fresh = case / "live.jsonl", case / "fresh.jsonl"
    write_trace(live, live_rows)
    write_trace(fresh, fresh_rows)
    try:
        comparator.compare(live, fresh)
    except ValueError:
        return True
    return False


def sealing_control(gameplay_v0: Path, directory: Path) -> bool:
    root = directory / "sealing"
    current, snapshot = root / "current", root / "snapshot"
    current.mkdir(parents=True)
    snapshot.mkdir()
    probe = current / "probe.dll"
    application = current / "application.dll"
    gameplay = current / "Gameplay.fs"
    probe.write_bytes(b"probe")
    application.write_bytes(b"application")
    gameplay.write_bytes(gameplay_v0.read_bytes())
    files = []
    for name, path in (("probe", probe), ("application", application), ("gameplay", gameplay)):
        files.append(copy_entry(path, snapshot / "outputs" / "test" / path.name, f"output:test:{path.name}", snapshot))
    receipt = {
        "outputRoots": {
            "test": {
                "currentRoot": str(current.resolve()),
                "snapshotRoot": "outputs/test",
                "fileCount": 3,
            }
        }
    }
    verify_output_roots(receipt, files, snapshot.resolve())
    unexpected = current / "unsealed-content.txt"
    unexpected.write_text("unsealed", encoding="utf-8")
    rejected = False
    try:
        verify_output_roots(receipt, files, snapshot.resolve())
    except ValueError:
        rejected = True
    return rejected and all(not os.path.samefile(Path(entry["currentPath"]), snapshot / entry["snapshotPath"]) for entry in files)


def cleanup_control(directory: Path) -> bool:
    child = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(60)"],
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    cleanup = runner.terminate_process_tree(child, "objective-benign-child", timeout=10.0)
    receipt = directory / "cleanup-control.json"
    atomic_json(receipt, {"schemaVersion": 1, "nativeLaunch": False, "cleanup": cleanup})
    return cleanup.get("attempted") is True and cleanup.get("pass") is True and child.poll() is not None


def cleanup_primary_failure_control(directory: Path) -> bool:
    child = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(60)"],
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )

    def fail_primary(*_args, **_kwargs):
        raise subprocess.TimeoutExpired("forced-primary-cleanup", 0.01)

    cleanup = runner.terminate_process_tree(
        child,
        "objective-forced-primary-error",
        timeout=10.0,
        primary_runner=fail_primary,
    )
    receipt = directory / "cleanup-primary-failure-control.json"
    atomic_json(receipt, {"schemaVersion": 1, "nativeLaunch": False, "cleanup": cleanup})
    return bool(
        cleanup.get("fallback", {}).get("attempted")
        and cleanup.get("fallback", {}).get("rootCompleted")
        and child.poll() is not None
        and cleanup.get("treeCleanupConfirmed") is False
        and cleanup.get("pass") is False
        and cleanup.get("furtherNativeWorkAllowed") is False
    )


def accepted_receipt_control(receipt_path: Path, receipt_sha256: str, directory: Path) -> bool:
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    bindings = receipt["launchBindings"]
    checked = verify_receipt(
        receipt_path,
        receipt_sha256,
        receipt["arm"],
        Path(bindings["probe"]["currentPath"]),
        Path(bindings["application"]["currentPath"]),
        Path(bindings["gameplay"]["currentPath"]),
    )
    manifest_path = receipt_path.parent / receipt["sourceManifest"]["snapshotPath"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    corrupted = copy.deepcopy(manifest)
    first = next(entry for entry in corrupted["entries"] if entry["override"] is None)
    first["acceptedSha256"] = "0" * 64
    rejected = False
    try:
        verify_source_manifest(corrupted, Path(manifest["sourceRoot"]), receipt["arm"])
    except ValueError:
        rejected = True
    control = {
        "schemaVersion": 1,
        "nativeLaunch": False,
        "receipt": checked["identity"],
        "sourceManifestVerification": checked["sourceManifestVerification"],
        "toolchainVerification": checked["toolchainVerification"],
        "corruptedManifestRejected": rejected,
    }
    atomic_json(directory / "accepted-arm-receipt-control.json", control)
    return checked["sourceManifestVerification"]["fileCount"] == 3240 and rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--gameplay-v0", type=Path, required=True)
    parser.add_argument("--arm-receipt", type=Path)
    parser.add_argument("--arm-receipt-sha256")
    args = parser.parse_args()
    if bool(args.arm_receipt) != bool(args.arm_receipt_sha256):
        parser.error("--arm-receipt and --arm-receipt-sha256 must be supplied together")
    root = Path(__file__).resolve().parents[2]
    output = args.output.resolve()
    if output.exists():
        parser.error("output directory must be new")
    output.mkdir(parents=True)
    checks = []
    contract = root / "experiments/nu-r10-schema-reload/pre-execution-contract.md"
    amendment = root / "experiments/nu-r10-schema-reload/protocol-amendment-01.md"
    oracle_path = Path(__file__).with_name("oracle.json")
    gameplay_v0 = args.gameplay_v0.resolve(strict=True)
    checks.append({"name": "contract identity", "pass": sha(contract) == CONTRACT_SHA256})
    checks.append({"name": "amendment identity", "pass": sha(amendment) == AMENDMENT_SHA256})
    checks.append({"name": "independent oracle identity", "pass": sha(oracle_path) == ORACLE_SHA256})
    for name in (
        "prepare.py",
        "schema_edit.py",
        "source_manifest.py",
        "seal_build.py",
        "run.py",
        "compare.py",
        "objective_checks.py",
    ):
        py_compile.compile(str(Path(__file__).with_name(name)), doraise=True)
        checks.append({"name": f"compile {name}", "pass": True})
    gameplay_body = gameplay_v0.read_bytes()
    derived = derive_v1(gameplay_body)
    checks.append(
        {
            "name": "byte-exact BOM/CRLF V0-to-V1 derivation",
            "pass": sha(gameplay_v0) == GAMEPLAY_V0_SHA256
            and hashlib.sha256(derived).hexdigest() == GAMEPLAY_V1_SHA256
            and derived.startswith(b"\xef\xbb\xbf")
            and derived.count(b"\r\n") == 307
            and derived.count(b"\n") - derived.count(b"\r\n") == 0,
        }
    )
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    valid = output / "valid"
    valid.mkdir()
    live_success = arm_rows("live", oracle, 200)
    fresh_success = arm_rows("fresh", oracle, 200)
    write_trace(valid / "live.jsonl", live_success)
    write_trace(valid / "fresh.jsonl", fresh_success)
    successful = comparator.compare(valid / "live.jsonl", valid / "fresh.jsonl")
    checks.append({"name": "observation-derived reward-200 matched pair", "pass": successful["matchedSuccessfulPreservationPair"] is True})

    mapping_failure = output / "mapping-failure"
    mapping_failure.mkdir()
    write_trace(mapping_failure / "live.jsonl", arm_rows("live", oracle, 0))
    write_trace(mapping_failure / "fresh.jsonl", fresh_success)
    failed = comparator.compare(mapping_failure / "live.jsonl", mapping_failure / "fresh.jsonl")
    checks.append(
        {
            "name": "observed zero remains valid failed mapping",
            "pass": failed["observationProcessesPassed"] is True
            and failed["liveRequiredRewardInstalled"] is False
            and failed["liveMappingRequirementPass"] is False
            and failed["matchedSuccessfulPreservationPair"] is False,
        }
    )

    preservation_failure = output / "preservation-failure"
    preservation_failure.mkdir()
    write_trace(preservation_failure / "live.jsonl", arm_rows("live", oracle, 200, preservation=False, continue_once=False))
    write_trace(preservation_failure / "fresh.jsonl", fresh_success)
    preservation_result = comparator.compare(preservation_failure / "live.jsonl", preservation_failure / "fresh.jsonl")
    checks.append(
        {
            "name": "reward 200 plus truthful preservation failure is valid failed mapping",
            "pass": preservation_result["liveRequiredRewardInstalled"] is True
            and preservation_result["livePreservationPass"] is False
            and preservation_result["liveMappingRequirementPass"] is False
            and preservation_result["liveContinuationAttempted"] is False,
        }
    )

    adversarial = output / "adversarial"
    adversarial.mkdir()
    wrong_flags = arm_rows("live", oracle, 0)
    next(row for row in wrong_flags if row["event"] == "reload-installed")["mappingRequirementPass"] = True
    next(row for row in wrong_flags if row["event"] == "result")["mappingRequirementPass"] = True
    checks.append({"name": "reject reward/flag disagreement", "pass": expect_rejected(wrong_flags, fresh_success, adversarial, "wrong-flags")})

    shared_wrong_live, shared_wrong_fresh = copy.deepcopy(live_success), copy.deepcopy(fresh_success)
    for rows in (shared_wrong_live, shared_wrong_fresh):
        for event in ("post-update-halted", "next-halted-stable"):
            next(row for row in rows if row["event"] == event)["model"]["score"] = 999
    checks.append({"name": "reject shared wrong post-state", "pass": expect_rejected(shared_wrong_live, shared_wrong_fresh, adversarial, "shared-wrong-post")})

    wrong_schema = copy.deepcopy(live_success)
    next(row for row in wrong_schema if row["event"] == "checkpoint-halted")["fieldNames"] = comparator.NEW_SCHEMA
    checks.append({"name": "reject wrong mode schema", "pass": expect_rejected(wrong_schema, fresh_success, adversarial, "wrong-schema")})

    for field, value, name in (
        ("runtime", ".NET 10.0.9", "wrong-runtime"),
        ("os", "Linux", "wrong-os"),
        ("architecture", "Arm64", "wrong-architecture"),
    ):
        wrong_configuration = copy.deepcopy(live_success)
        next(row for row in wrong_configuration if row["event"] == "configuration")[field] = value
        checks.append({"name": f"reject mismatched configuration {field}", "pass": expect_rejected(wrong_configuration, fresh_success, adversarial, name)})

    missing_identity = [row for row in copy.deepcopy(live_success) if row["event"] != "reload-installed"]
    checks.append({"name": "reject missing identity event", "pass": expect_rejected(missing_identity, fresh_success, adversarial, "missing-identity")})

    duplicate_identity = copy.deepcopy(live_success)
    duplicate_identity.insert(-1, copy.deepcopy(next(row for row in duplicate_identity if row["event"] == "reload-installed")))
    checks.append({"name": "reject duplicate identity event", "pass": expect_rejected(duplicate_identity, fresh_success, adversarial, "duplicate-identity")})

    missing_oracle = [row for row in copy.deepcopy(live_success) if row["event"] != "precomputed-oracle"]
    checks.append({"name": "reject missing precomputed oracle", "pass": expect_rejected(missing_oracle, fresh_success, adversarial, "missing-oracle")})

    contradictory_preservation = copy.deepcopy(live_success)
    next(row for row in contradictory_preservation if row["event"] == "post-reload-pre-advance")["model"]["lives"] = 4
    checks.append({"name": "reject contradictory preservation flags", "pass": expect_rejected(contradictory_preservation, fresh_success, adversarial, "contradictory-preservation")})

    controls = output / "controls"
    controls.mkdir()
    checks.append({"name": "sealed copied paths and receipt hash verify", "pass": sealing_control(gameplay_v0, controls)})
    checks.append({"name": "bounded full-tree cleanup of benign child", "pass": cleanup_control(controls)})
    checks.append({"name": "primary cleanup failure forces direct fallback and unresolved-tree stop", "pass": cleanup_primary_failure_control(controls)})
    if args.arm_receipt:
        checks.append(
            {
                "name": "accepted 3240-file source and complete output-root receipt verifies",
                "pass": accepted_receipt_control(
                    args.arm_receipt.resolve(strict=True),
                    args.arm_receipt_sha256.lower(),
                    controls,
                ),
            }
        )

    fs = Path(__file__).with_name("SchemaReload.fs").read_text(encoding="utf-8")
    run_source = Path(__file__).with_name("run.py").read_text(encoding="utf-8")
    checks.append(
        {
            "name": "required source control-flow surfaces",
            "pass": all(
                needle in fs + run_source
                for needle in (
                    "precomputed-oracle",
                    "requiredRewardInstalled && preservationPass",
                    "except BaseException as error",
                    "finally:",
                    "KeyboardInterrupt",
                    "checkpoint-binding.json",
                )
            ),
        }
    )
    result = {
        "schemaVersion": 3,
        "nativeLaunch": False,
        "pass": all(check["pass"] for check in checks),
        "checks": checks,
        "mappingFailureComparison": failed,
        "preservationFailureComparison": preservation_result,
        "mappingSuccessComparison": successful,
    }
    (output / "objective-checks.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
