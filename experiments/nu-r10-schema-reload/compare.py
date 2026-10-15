"""Validate and compare retained R10 traces from primary observations."""

import argparse
import copy
import hashlib
import json
from pathlib import Path


ORACLE_SHA256 = "327d804d8d780f70894476267f0995554764798309b6a5fa1b88c1fe69b1cb2c"
OLD_SCHEMA = ["GameplayTime", "GameplayState", "Paddle", "Ball", "Bricks", "Score", "Lives"]
NEW_SCHEMA = OLD_SCHEMA + ["BrickReward"]
EXPECTED_FRAMEWORK = ".NET 10.0.10"
EXPECTED_ARCHITECTURE = "X64"


def identity(path: Path) -> dict:
    body = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def read_trace(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {error}") from error
    if not rows:
        raise ValueError(f"{path}: empty trace")
    return rows


def exactly(rows: list[dict], event: str) -> dict:
    matches = [row for row in rows if row.get("event") == event]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {event!r}, found {len(matches)}")
    return matches[0]


def none(rows: list[dict], event: str) -> None:
    matches = [row for row in rows if row.get("event") == event]
    if matches:
        raise ValueError(f"expected no {event!r}, found {len(matches)}")


def optional_one(rows: list[dict], event: str) -> dict | None:
    matches = [row for row in rows if row.get("event") == event]
    if len(matches) > 1:
        raise ValueError(f"expected at most one {event!r}, found {len(matches)}")
    return matches[0] if matches else None


def require_equal(label: str, actual, expected) -> None:
    if actual != expected:
        raise ValueError(f"{label} differs")


def load_public_oracle() -> tuple[dict, dict]:
    path = Path(__file__).with_name("oracle.json").resolve(strict=True)
    info = identity(path)
    if info["sha256"] != ORACLE_SHA256:
        raise ValueError("public independent oracle identity differs")
    return json.loads(path.read_text(encoding="utf-8")), info


def parsed_template(row: dict, name: str):
    value = row.get(name)
    if not isinstance(value, str):
        raise ValueError(f"precomputed oracle {name} is not a JSON string")
    try:
        return json.loads(value)
    except json.JSONDecodeError as error:
        raise ValueError(f"precomputed oracle {name} is invalid JSON") from error


def derive_expected(model_zero: dict, projection_zero: dict, reward: int) -> tuple[dict, dict]:
    if not isinstance(reward, int) or reward < 0 or reward > 1000:
        raise ValueError("observed reward is outside the frozen continuation range")
    model = copy.deepcopy(model_zero)
    projection = copy.deepcopy(projection_zero)
    model["score"] = 100 + reward
    projection["scoreText"] = f"Score: {100 + reward}"
    return model, projection


def validate_precomputed(row: dict, checkpoint: dict, oracle: dict) -> dict:
    if row.get("rewardCasesPrecomputed") != 1001:
        raise ValueError("precomputed oracle reward count differs")
    templates = {
        "checkpointModel": parsed_template(row, "checkpointModelJson"),
        "checkpointProjection": parsed_template(row, "checkpointProjectionJson"),
        "modelZero": parsed_template(row, "expectedModelZeroJson"),
        "model200": parsed_template(row, "expectedModel200Json"),
        "projectionZero": parsed_template(row, "expectedProjectionZeroJson"),
        "projection200": parsed_template(row, "expectedProjection200Json"),
    }
    require_equal("carried checkpoint model", templates["checkpointModel"], checkpoint.get("model"))
    require_equal("carried checkpoint projection", templates["checkpointProjection"], checkpoint.get("projection"))
    require_equal("checkpoint versus independent oracle", templates["checkpointModel"], oracle["checkpoint"])
    require_equal("reward-zero model versus independent oracle", templates["modelZero"], oracle["expected_post_reward_zero"])
    require_equal("reward-200 model versus independent oracle", templates["model200"], oracle["expected_post_reward_200"])
    derived_200 = derive_expected(templates["modelZero"], templates["projectionZero"], 200)
    require_equal("reward-200 model template", templates["model200"], derived_200[0])
    require_equal("reward-200 projection template", templates["projection200"], derived_200[1])
    return templates


def validate_continuation(rows: list[dict], result: dict, templates: dict, reward: int, mode: str) -> dict:
    resume = optional_one(rows, "resume-request")
    schedule = optional_one(rows, "event-schedule")
    post = optional_one(rows, "post-update-halted")
    stable = optional_one(rows, "next-halted-stable")
    attempted = resume is not None
    require_equal(f"{mode}: continuationAttempted flag", result.get("continuationAttempted"), attempted)
    events = (schedule, post, stable)
    if not attempted:
        if any(event is not None for event in events):
            raise ValueError(f"{mode}: withheld continuation has retained continuation events")
        require_equal(f"{mode}: continuationPass flag", result.get("continuationPass"), False)
        return {"attempted": False, "passed": False, "post": None, "stable": None}
    if any(event is None for event in events):
        raise ValueError(f"{mode}: attempted continuation lacks required events")
    require_equal(f"{mode}: event order", schedule.get("order"), ["TimeUpdate", "Update"])
    require_equal(f"{mode}: GameDelta.Updates", schedule.get("gameDeltaUpdates"), [1])
    require_equal(f"{mode}: schedule update count", schedule.get("updates"), 1)
    require_equal(f"{mode}: schedule time-update count", schedule.get("timeUpdates"), 1)
    require_equal(f"{mode}: schedule left input", schedule.get("leftInputs"), 0)
    require_equal(f"{mode}: schedule right input", schedule.get("rightInputs"), 0)
    expected_model, expected_projection = derive_expected(templates["modelZero"], templates["projectionZero"], reward)
    require_equal(f"{mode}: complete post model", post.get("model"), expected_model)
    require_equal(f"{mode}: complete post projection", post.get("projection"), expected_projection)
    require_equal(f"{mode}: post schema", post.get("fieldNames"), NEW_SCHEMA)
    require_equal(f"{mode}: post projection errors", post.get("projectionErrors"), [])
    require_equal(f"{mode}: post reward", post.get("reward"), reward)
    require_equal(f"{mode}: stable model", stable.get("model"), expected_model)
    require_equal(f"{mode}: stable projection", stable.get("projection"), expected_projection)
    require_equal(f"{mode}: stable schema", stable.get("fieldNames"), NEW_SCHEMA)
    require_equal(f"{mode}: stable projection errors", stable.get("projectionErrors"), [])
    require_equal(f"{mode}: stable reward", stable.get("reward"), reward)
    require_equal(f"{mode}: continuationPass flag", result.get("continuationPass"), True)
    require_equal(f"{mode}: result update count", result.get("updates"), 1)
    require_equal(f"{mode}: result time-update count", result.get("timeUpdates"), 1)
    require_equal(f"{mode}: result left input", result.get("leftInputs"), 0)
    require_equal(f"{mode}: result right input", result.get("rightInputs"), 0)
    return {"attempted": True, "passed": True, "post": post, "stable": stable}


def validate_arm(path: Path, mode: str, oracle: dict) -> dict:
    rows = read_trace(path)
    if any(row.get("event") in ("exception", "launch-exception") for row in rows):
        raise ValueError(f"{mode}: successful observation trace contains an exception")
    result = exactly(rows, "result")
    require_equal(f"{mode}: result mode", result.get("mode"), mode)
    require_equal(f"{mode}: observation process", result.get("processPass"), True)
    engine_exit = exactly(rows, "engine-exit")
    require_equal(f"{mode}: engine exit code", engine_exit.get("exitCode"), 0)
    require_equal(f"{mode}: engine done", engine_exit.get("done"), True)
    require_equal(f"{mode}: engine process verdict", engine_exit.get("processPassed"), True)
    configuration = exactly(rows, "configuration")
    require_equal(f"{mode}: configuration mode", configuration.get("mode"), mode)
    require_equal(f"{mode}: framework", configuration.get("runtime"), EXPECTED_FRAMEWORK)
    require_equal(f"{mode}: architecture", configuration.get("architecture"), EXPECTED_ARCHITECTURE)
    if not isinstance(configuration.get("os"), str) or "Windows" not in configuration["os"]:
        raise ValueError(f"{mode}: operating system differs")
    controls = exactly(rows, "oracle-data-controls")
    expected_controls = {
        "resetRejected": True,
        "alteredOldFieldRejected": True,
        "wrongBrickRejected": True,
        "wrongScoreRejected": True,
        "zeroVersus200Rejected": True,
        "rewardCasesPrecomputed": 1001,
    }
    if any(controls.get(key) != value for key, value in expected_controls.items()):
        raise ValueError(f"{mode}: incomplete or failed oracle controls")
    checkpoint = exactly(rows, "checkpoint-halted")
    expected_schema = OLD_SCHEMA if mode == "live" else NEW_SCHEMA
    require_equal(f"{mode}: checkpoint schema", checkpoint.get("fieldNames"), expected_schema)
    require_equal(f"{mode}: checkpoint projection errors", checkpoint.get("projectionErrors"), [])
    require_equal(f"{mode}: checkpoint updates", checkpoint.get("updates"), 0)
    require_equal(f"{mode}: checkpoint time updates", checkpoint.get("timeUpdates"), 0)
    require_equal(f"{mode}: checkpoint left input", checkpoint.get("leftInputs"), 0)
    require_equal(f"{mode}: checkpoint right input", checkpoint.get("rightInputs"), 0)
    templates = validate_precomputed(exactly(rows, "precomputed-oracle"), checkpoint, oracle)

    if mode == "live":
        reload_start = exactly(rows, "reload-start")
        require_equal("live: pre-reload schema", reload_start.get("fieldNames"), OLD_SCHEMA)
        require_equal("live: pre-reload field absence", reload_start.get("brickRewardPresent"), False)
        assemblies = exactly(rows, "fsi-assemblies")
        installed = exactly(rows, "reload-installed")
        preadvance = exactly(rows, "post-reload-pre-advance")
        none(rows, "fresh-initial-model")
        require_equal("live: installed schema", installed.get("fieldNames"), NEW_SCHEMA)
        require_equal("live: preadvance schema", preadvance.get("fieldNames"), NEW_SCHEMA)
        require_equal("live: raw/dispatcher FSI type", installed.get("actualType"), installed.get("dispatcherModelType"))
        returned_mvids = {entry.get("mvid") for entry in assemblies.get("assemblies", [])}
        if installed.get("actualAssembly", {}).get("mvid") not in returned_mvids:
            raise ValueError("live: raw model assembly not in returned FSI set")
        if installed.get("dispatcherAssembly", {}).get("mvid") not in returned_mvids:
            raise ValueError("live: dispatcher assembly not in returned FSI set")
        reward = installed.get("observedReward")
        require_equal("live: installed/result reward", result.get("observedReward"), reward)
        require_equal("live: preadvance reward", preadvance.get("reward"), reward)
        require_equal("live: CodeReloadEvent count", preadvance.get("codeReloadEvents"), 1)
        preservation = bool(
            preadvance.get("model") == checkpoint.get("model")
            and preadvance.get("projection") == checkpoint.get("projection")
            and preadvance.get("projectionErrors") == []
            and preadvance.get("updates") == 0
            and preadvance.get("timeUpdates") == 0
            and preadvance.get("leftInputs") == 0
            and preadvance.get("rightInputs") == 0
        )
        required_reward = reward == 200
        reward_in_range = isinstance(reward, int) and 0 <= reward <= 1000
        mapping = required_reward and preservation
        require_equal("live: installed requiredRewardInstalled", installed.get("requiredRewardInstalled"), required_reward)
        require_equal("live: result requiredRewardInstalled", result.get("requiredRewardInstalled"), required_reward)
        require_equal("live: installed preservationPass", installed.get("preservationPass"), preservation)
        require_equal("live: result preservationPass", result.get("preservationPass"), preservation)
        require_equal("live: installed mappingRequirementPass", installed.get("mappingRequirementPass"), mapping)
        require_equal("live: result mappingRequirementPass", result.get("mappingRequirementPass"), mapping)
        require_equal("live: installed rewardInRange", installed.get("rewardInRange"), reward_in_range)
        require_equal("live: result rewardInRange", result.get("rewardInRange"), reward_in_range)
        require_equal("live: fresh initialization applicability", result.get("freshInitializationApplicable"), False)
        require_equal("live: fresh initialization flag", result.get("freshInitializationPass"), False)
        require_equal("live: fresh initial reward sentinel", result.get("freshInitialReward"), -1)
    else:
        none(rows, "reload-start")
        none(rows, "fsi-assemblies")
        none(rows, "reload-installed")
        none(rows, "post-reload-pre-advance")
        initial = exactly(rows, "fresh-initial-model")
        require_equal("fresh: initial schema", initial.get("fieldNames"), NEW_SCHEMA)
        reward = checkpoint.get("reward")
        require_equal("fresh: reconstructed reward", reward, 200)
        require_equal("fresh: result reward", result.get("observedReward"), reward)
        fresh_initial_pass = initial.get("reward") == 200
        required_reward = reward == 200
        require_equal("fresh: initial reward evidence", result.get("freshInitialReward"), initial.get("reward"))
        require_equal("fresh: initialization flag", result.get("freshInitializationPass"), fresh_initial_pass)
        require_equal("fresh: initialization applicability", result.get("freshInitializationApplicable"), True)
        require_equal("fresh: required reward flag", result.get("requiredRewardInstalled"), required_reward)
        require_equal("fresh: mapping flag is inapplicable", result.get("mappingRequirementPass"), False)
        preservation = None
        mapping = False

    continuation = validate_continuation(rows, result, templates, reward, mode)
    prefix = ["configuration"]
    if mode == "fresh":
        prefix.append("fresh-initial-model")
    prefix.extend(["oracle-data-controls", "precomputed-oracle", "checkpoint-halted"])
    if mode == "live":
        prefix.extend(["reload-start", "fsi-assemblies", "reload-installed", "post-reload-pre-advance"])
    if continuation["attempted"]:
        prefix.extend(["resume-request", "event-schedule", "post-update-halted", "next-halted-stable"])
    prefix.extend(["result", "engine-exit"])
    require_equal(f"{mode}: exact event sequence", [row.get("event") for row in rows], prefix)
    return {
        "mode": mode,
        "trace": identity(path),
        "result": result,
        "checkpoint": checkpoint,
        "templates": templates,
        "reward": reward,
        "requiredReward": required_reward,
        "mapping": mapping,
        "preservation": preservation,
        "freshInitialization": result.get("freshInitializationPass") is True if mode == "fresh" else None,
        "continuation": continuation,
    }


def compare(live_path: Path, fresh_path: Path) -> dict:
    oracle, oracle_identity = load_public_oracle()
    live = validate_arm(live_path, "live", oracle)
    fresh = validate_arm(fresh_path, "fresh", oracle)
    checkpoint_equal = (
        live["checkpoint"].get("model") == fresh["checkpoint"].get("model")
        and live["checkpoint"].get("projection") == fresh["checkpoint"].get("projection")
    )
    fresh_preservation = checkpoint_equal and fresh["checkpoint"].get("projectionErrors") == []
    require_equal("fresh: preservationPass flag", fresh["result"].get("preservationPass"), fresh_preservation)
    require_equal(
        "fresh: rewardInRange flag",
        fresh["result"].get("rewardInRange"),
        fresh["freshInitialization"] and fresh_preservation,
    )
    live_matched = live["mapping"] and live["continuation"]["passed"]
    fresh_matched = fresh["freshInitialization"] and fresh_preservation and fresh["continuation"]["passed"]
    require_equal("live: matchedRequirementPass flag", live["result"].get("matchedRequirementPass"), live_matched)
    require_equal("fresh: matchedRequirementPass flag", fresh["result"].get("matchedRequirementPass"), fresh_matched)
    post_equal = None
    if live["continuation"]["post"] is not None and fresh["continuation"]["post"] is not None:
        post_equal = (
            live["continuation"]["post"].get("model") == fresh["continuation"]["post"].get("model")
            and live["continuation"]["post"].get("projection") == fresh["continuation"]["post"].get("projection")
        )
    matched = bool(live_matched and fresh_matched and checkpoint_equal and post_equal is True)
    return {
        "schemaVersion": 2,
        "observationProcessesPassed": True,
        "oracle": oracle_identity,
        "liveRequiredRewardInstalled": live["requiredReward"],
        "liveMappingRequirementPass": live["mapping"],
        "freshInitializationPass": fresh["freshInitialization"],
        "livePreservationPass": live["preservation"],
        "freshPreservationPass": fresh_preservation,
        "liveContinuationAttempted": live["continuation"]["attempted"],
        "freshContinuationAttempted": fresh["continuation"]["attempted"],
        "liveContinuationPass": live["continuation"]["passed"],
        "freshContinuationPass": fresh["continuation"]["passed"],
        "liveObservedReward": live["reward"],
        "freshObservedReward": fresh["reward"],
        "checkpointSevenAndProjectionEqual": checkpoint_equal,
        "postModelAndProjectionEqual": post_equal,
        "matchedSuccessfulPreservationPair": matched,
        "arms": {"live": live["trace"], "fresh": fresh["trace"]},
        "interpretation": (
            "All verdicts are derived from retained observations. Live mapping requires both the "
            "required reward 200 and complete inherited-state/projection preservation."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("live_trace", type=Path)
    parser.add_argument("fresh_trace", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error("output directory must be new")
    result = compare(args.live_trace.resolve(strict=True), args.fresh_trace.resolve(strict=True))
    output.mkdir(parents=True)
    target = output / "comparison.json"
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
