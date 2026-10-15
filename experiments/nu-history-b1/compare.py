"""Compare normalized B1 arm traces and check deliberately corrupted observations."""

import argparse
import copy
import json
from pathlib import Path


def validate(history, fresh):
    results = []
    rows = []
    for name, trace in (("history", history), ("fresh", fresh)):
        result = [r for r in trace if r["event"] == "result"]
        assert len(result) == 1 and result[0]["pass"], f"{name}: runtime failed"
        assert result[0]["leftInputUpdates"] == result[0]["rightInputUpdates"] == 0
        exit_rows = [r for r in trace if r["event"] == "engine-exit"]
        assert len(exit_rows) == 1 and exit_rows[0]["exitCode"] == 0
        schedules = [r for r in trace if r["event"] == "event-schedule"]
        assert [r["phase"] for r in schedules] == (["drift", "continuation"] if name == "history" else ["continuation"])
        for schedule in schedules:
            count = 10 if schedule["phase"] == "drift" else 20
            assert schedule["updates"] == schedule["timeUpdates"] == count
            assert schedule["order"] == [event for _ in range(count) for event in ("TimeUpdate", "Update")]
        steps = [r for r in trace if r["event"] == "continuation-step"]
        assert [r["step"] for r in steps] == list(range(1, 21)), f"{name}: step sequence"
        seed = [r for r in trace if r["event"] == "seeded-B0"]
        assert len(seed) == 1
        for row in steps:
            assert row["model"]["time"] == 149 + row["step"]
            assert row["functional"] and row["accompanied"]
            assert row["advancing"] == (row["step"] < 20)
            assert row["projectionErrors"] == []
            assert row["projection"]["names"] == seed[0]["projection"]["names"]
        final = [r for r in trace if r["event"] == "continuation-next-halted"]
        assert len(final) == 1 and not final[0]["advancing"]
        assert final[0]["model"] == steps[-1]["model"]
        assert final[0]["projection"] == steps[-1]["projection"]
        assert final[0]["updates"] == steps[-1]["updates"]
        assert final[0]["timeUpdates"] == steps[-1]["timeUpdates"]
        rows.append(steps)
        results.append({"arm": name, "observedSteps": len(steps), "schedules": len(schedules),
                        "absoluteUpdates": result[0]["updates"], "absoluteTimeUpdates": result[0]["timeUpdates"]})
    for left, right in zip(*rows):
        assert left["step"] == right["step"]
        assert left["model"] == right["model"], f"model mismatch at {left['step']}"
        assert left["projection"] == right["projection"], f"projection mismatch at {left['step']}"
    return {"pass": True, "arms": results, "completeModelsCompared": 20,
            "selectedProjectionsCompared": 20, "finalModel": rows[0][-1]["model"]}


def negative_controls(history, fresh):
    checks = []
    for kind in ("projection", "step-order", "event-order"):
        corrupted = copy.deepcopy(fresh)
        steps = [r for r in corrupted if r["event"] == "continuation-step"]
        if kind == "projection":
            steps[9]["projection"]["ball"]["position"][0] = "00000000"
        elif kind == "step-order":
            steps[9]["step"], steps[10]["step"] = steps[10]["step"], steps[9]["step"]
        else:
            schedule = next(r for r in corrupted if r["event"] == "event-schedule")
            schedule["order"][0], schedule["order"][1] = schedule["order"][1], schedule["order"][0]
        try:
            validate(history, corrupted)
        except AssertionError:
            checks.append({"kind": kind, "rejected": True})
        else:
            raise AssertionError(f"negative control accepted: {kind}")
    return checks


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("history_trace", type=Path)
    parser.add_argument("fresh_trace", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output receipt must be new")
    history, fresh = [[json.loads(line) for line in p.read_text(encoding="utf-8").splitlines()]
                      for p in (args.history_trace, args.fresh_trace)]
    result = validate(history, fresh)
    result["analysisNegativeControls"] = negative_controls(history, fresh)
    result["negativeControlScope"] = "Mutated in-memory observations, not additional application executions."
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "finalModel"}, indent=2))


if __name__ == "__main__":
    main()
