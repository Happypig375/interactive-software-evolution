"""Create retained synthetic receipts and validate the offline R06 summarizer."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
PLAN = json.loads((HERE / "attempt-plan.json").read_text(encoding="utf-8"))
ASSIGNED = {item["attemptId"]: item for item in PLAN["feasibility"] + PLAN["measuredOrder"]}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fake_sha(character):
    return character * 64


def result_event(attempt, frequency, acquisition_ticks, direct_ticks, ready_ticks, passed=True,
                 missing_direct=False, gc_marker=1):
    acquisition_start = 1000
    recovery_start = 2000
    direct_stop = 0 if missing_direct else recovery_start + direct_ticks
    readiness_stop = recovery_start + ready_ticks
    oracle_start, oracle_stop = 3000, 3007
    return {
        "event": "result",
        "pass": passed,
        "detail": "synthetic",
        "phase": "complete" if passed else "failed",
        "route": attempt["route"],
        "attemptKind": attempt["kind"],
        "attemptId": attempt["attemptId"],
        "updates": 10,
        "timeUpdates": 10,
        "callbacks": 20,
        "leftInputUpdates": 0,
        "rightInputUpdates": 0,
        "stopwatchFrequency": frequency,
        "acquisitionStart": acquisition_start,
        "acquisitionStop": acquisition_start + acquisition_ticks,
        "acquisitionTicks": acquisition_ticks,
        "recoveryStart": recovery_start,
        "recoveryDirectStop": direct_stop,
        "recoveryDirectTicks": -1 if missing_direct else direct_ticks,
        "readinessStop": readiness_stop,
        "requestToReadyTicks": ready_ticks,
        "oracleWorkStart": oracle_start,
        "oracleWorkStop": oracle_stop,
        "oracleWorkTicks": 7,
        "traceWorkTicksBeforeResult": 11,
        "clockPairs": [
            {"start": 900, "stop": 902, "ticks": 2},
            {"start": 910, "stop": 910, "ticks": 0},
        ],
        "gcAndMemorySamples": [
            {
                "label": "synthetic",
                "timestamp": 800,
                "allocatedBytesApproximate": 10000 + gc_marker,
                "gen0Collections": 1,
                "gen1Collections": 0,
                "gen2Collections": 0,
                "managedHeapBytesSecondary": 20000 + gc_marker,
                "workingSetBytesSecondary": 30000 + gc_marker,
                "privateBytesSecondary": 40000 + gc_marker,
            }
        ],
    }


def write_process(directory, attempt_id, *, frequency=1000, acquisition_ticks=10,
                  direct_ticks=20, ready_ticks=50, outcome="pass", build_marker="a",
                  missing_direct=False, gc_marker=1):
    attempt = ASSIGNED[attempt_id]
    probe = directory / "probe"
    probe.mkdir(parents=True)
    passed = outcome == "pass"
    event = result_event(attempt, frequency, acquisition_ticks, direct_ticks, ready_ticks,
                         passed=passed, missing_direct=missing_direct, gc_marker=gc_marker)
    trace = [
        {"event": "configuration", "route": attempt["route"], "attemptKind": attempt["kind"],
         "attemptId": attempt_id, "stopwatchFrequency": frequency},
        {"event": "acquisition", "route": attempt["route"], "start": event["acquisitionStart"],
         "stop": event["acquisitionStop"], "ticks": event["acquisitionTicks"], "payloadUtf8Bytes": 123},
        {"event": "readiness-timing", "start": event["recoveryStart"],
         "directStop": event["recoveryDirectStop"], "readyStop": event["readinessStop"],
         "directTicks": event["recoveryDirectTicks"], "requestToReadyTicks": event["requestToReadyTicks"],
         "oracleWorkTicks": event["oracleWorkTicks"]},
        event,
        {"event": "engine-exit", "exitCode": 0 if passed else 1, "probeFinished": True,
         "probePassed": passed, "probeEndTick": 4000, "traceWorkTicksBeforeExit": 20},
    ]
    trace_path = probe / "trace.jsonl"
    trace_path.write_text("".join(json.dumps(item, separators=(",", ":")) + "\n" for item in trace), encoding="utf-8", newline="\n")
    result = {key: event[key] for key in (
        "attemptId", "attemptKind", "route", "pass", "stopwatchFrequency", "acquisitionTicks",
        "recoveryDirectTicks", "requestToReadyTicks", "oracleWorkTicks", "updates", "timeUpdates", "callbacks")}
    result["exitCode"] = 0 if passed else 1
    result_path = probe / "result.json"
    result_path.write_text(json.dumps(result, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
    identity_entry = {"path": "synthetic", "sha256": fake_sha(build_marker), "bytes": 1}
    receipt = {
        "schemaVersion": 2,
        "attempt": attempt,
        "command": ["dotnet", "synthetic.dll", attempt["route"], attempt["kind"], attempt_id,
                    "project.dll", "checkpoint", str(probe)],
        "timeoutSeconds": 600,
        "startedUtc": "2026-10-15T00:00:00Z",
        "timedOut": False,
        "acceptedBuildReceipt": {"path": "synthetic-build.json", "sha256": fake_sha(build_marker)},
        "verifiedSourceIdentities": {"r06/RecoveryCost.fs": identity_entry},
        "verifiedCommonBinaries": {"RecoveryCost.dll": identity_entry},
        "fixedInputs": {"gameplay.symbol": fake_sha("b"), "projection.json": fake_sha("c")},
        "pid": 1,
        "exitCode": 0 if passed else 1,
        "processElapsedSecondsNotComponentCost": 1.25 + gc_marker,
        "probeOutputs": {
            "trace.jsonl": {"bytes": trace_path.stat().st_size, "sha256": sha(trace_path)},
            "result.json": {"bytes": result_path.stat().st_size, "sha256": sha(result_path)},
        },
    }
    process_path = directory / "process.json"
    process_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    return process_path


def run_case(root, name, inputs):
    output = root / f"{name}-summary"
    command = [sys.executable, str(HERE / "summarize.py"), *[str(path) for path in inputs], "--output", str(output)]
    completed = subprocess.run(command, cwd=HERE, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise AssertionError(f"{name} summarizer failed: {completed.stderr}")
    report = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    return report, {
        "command": command,
        "exitCode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "summaryJson": {"path": str(output / "summary.json"), "sha256": sha(output / "summary.json")},
        "summaryMarkdown": {"path": str(output / "summary.md"), "sha256": sha(output / "summary.md")},
    }


def by_id(report):
    return {row["attemptId"]: row for row in report["assignedAttempts"]}


def route_summary(report, component, route):
    return next(item for item in report["descriptiveSummaries"]["byRoute"]
                if item["component"] == component and item["route"] == route)


def require_close(actual, expected):
    if not isinstance(actual, (int, float)) or abs(actual - expected) > 1e-12:
        raise AssertionError(f"expected {expected}, got {actual}")


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("output", type=Path, help="new private validation receipt directory")
    args = parser.parse_args()
    root = args.output.resolve(strict=False)
    if root.exists():
        parser.error("validation output directory must be new")
    root.mkdir(parents=True)
    cases = {}

    core_inputs = root / "core-inputs"
    paths = [
        write_process(core_inputs / "FH", "FH", frequency=1000, acquisition_ticks=999,
                      direct_ticks=999, ready_ticks=999, gc_marker=10),
        write_process(core_inputs / "FR", "FR", outcome="fail", gc_marker=11),
        write_process(core_inputs / "H1", "H1", frequency=1000, acquisition_ticks=10,
                      direct_ticks=20, ready_ticks=50, gc_marker=12),
        write_process(core_inputs / "R1", "R1", frequency=2000, acquisition_ticks=10,
                      direct_ticks=20, ready_ticks=60, gc_marker=13),
        write_process(core_inputs / "H2", "H2", outcome="fail", ready_ticks=50, gc_marker=14),
        write_process(core_inputs / "H3", "H3", missing_direct=True, gc_marker=15),
        write_process(core_inputs / "R3", "R3", frequency=1000, acquisition_ticks=15,
                      direct_ticks=30, ready_ticks=70, gc_marker=16),
        write_process(core_inputs / "R4", "R4", frequency=1000, acquisition_ticks=0,
                      direct_ticks=0, ready_ticks=0, gc_marker=17),
        write_process(core_inputs / "H4", "H4", frequency=1000, acquisition_ticks=0,
                      direct_ticks=0, ready_ticks=0, gc_marker=18),
        write_process(core_inputs / "H5", "H5", frequency=1000, acquisition_ticks=7,
                      direct_ticks=60, ready_ticks=20, gc_marker=19),
    ]
    core, cases["core"] = run_case(root, "core", paths)
    statuses = {key: value["status"] for key, value in by_id(core).items()}
    expected_statuses = {"FH": "pass", "FR": "fail", "H1": "pass", "R1": "pass",
                         "H2": "fail", "R2": "not-run", "H3": "invalid", "R3": "pass",
                         "R4": "pass", "H4": "pass", "H5": "invalid"}
    for attempt_id, expected in expected_statuses.items():
        assert statuses[attempt_id] == expected, (attempt_id, statuses[attempt_id])
    h_acquisition = route_summary(core, "acquisition", "H")
    assert h_acquisition["assignedDenominator"] == 6 and h_acquisition["validCompleteUsed"] == 2
    require_close(h_acquisition["medianMilliseconds"], 5.0)
    require_close(h_acquisition["rangeMilliseconds"]["minimum"], 0.0)
    require_close(h_acquisition["rangeMilliseconds"]["maximum"], 10.0)
    r_acquisition = route_summary(core, "acquisition", "R")
    assert r_acquisition["assignedDenominator"] == 6 and r_acquisition["validCompleteUsed"] == 3
    require_close(r_acquisition["medianMilliseconds"], 5.0)
    require_close(r_acquisition["rangeMilliseconds"]["minimum"], 0.0)
    require_close(r_acquisition["rangeMilliseconds"]["maximum"], 15.0)
    pair1 = core["descriptiveSummaries"]["pairs"][0]
    require_close(pair1["differences"]["acquisition"]["historyMinusReconstructionMilliseconds"], 5.0)
    require_close(pair1["differences"]["directRecovery"]["historyMinusReconstructionMilliseconds"], 10.0)
    require_close(pair1["differences"]["requestToReady"]["historyMinusReconstructionMilliseconds"], 20.0)
    pair4 = core["descriptiveSummaries"]["pairs"][3]
    assert pair4["validCompletePair"] is True
    for component in ("acquisition", "directRecovery", "requestToReady"):
        require_close(pair4["differences"][component]["historyMilliseconds"], 0.0)
        require_close(pair4["differences"][component]["reconstructionMilliseconds"], 0.0)
        require_close(pair4["differences"][component]["historyMinusReconstructionMilliseconds"], 0.0)
    pair_summaries = {item["component"]: item for item in core["descriptiveSummaries"]["historyMinusReconstruction"]}
    assert pair_summaries["acquisition"]["validCompletePairsUsed"] == 2
    require_close(pair_summaries["acquisition"]["medianMilliseconds"], 2.5)
    require_close(pair_summaries["directRecovery"]["medianMilliseconds"], 5.0)
    require_close(pair_summaries["requestToReady"]["medianMilliseconds"], 10.0)
    assert by_id(core)["H2"]["rawClocks"]["requestToReady"]["raw"]["ticks"] == 50
    assert by_id(core)["H1"]["gcAndMemorySamples"][0]["allocatedBytesApproximate"] == 10012
    assert h_acquisition["attemptIdsUsed"] == ["H1", "H4"]  # FH is excluded; zero is retained.
    h4 = by_id(core)["H4"]
    assert h4["crossClockValidation"]["valid"] is True
    assert h4["rawClocks"]["directRecovery"]["raw"]["start"] == h4["rawClocks"]["directRecovery"]["raw"]["stop"]
    h5 = by_id(core)["H5"]
    assert h5["status"] == "invalid"
    assert h5["rawClocks"]["directRecovery"]["valid"] is True
    assert h5["rawClocks"]["requestToReady"]["valid"] is True
    assert h5["crossClockValidation"]["available"] is True
    assert h5["crossClockValidation"]["valid"] is False
    assert "recoveryDirectStop is after readinessStop" in h5["crossClockValidation"]["issues"]
    assert "H5" not in h_acquisition["attemptIdsUsed"]

    duplicate_inputs = root / "duplicate-inputs"
    duplicate, cases["duplicate"] = run_case(root, "duplicate", [
        write_process(duplicate_inputs / "first", "H1"),
        write_process(duplicate_inputs / "second", "H1"),
    ])
    assert duplicate["integrityFlags"]["duplicateAttemptIds"] == ["H1"]
    assert by_id(duplicate)["H1"]["status"] == "invalid"
    assert len(duplicate["suppliedInputs"]) == 2

    mismatch_inputs = root / "mismatch-inputs"
    mismatch, cases["identityMismatch"] = run_case(root, "identity-mismatch", [
        write_process(mismatch_inputs / "H1", "H1", build_marker="a"),
        write_process(mismatch_inputs / "R1", "R1", build_marker="d"),
    ])
    assert mismatch["integrityFlags"]["measuredSeriesMismatch"] is True
    assert by_id(mismatch)["H1"]["status"] == "invalid"
    assert by_id(mismatch)["R1"]["status"] == "invalid"
    assert route_summary(mismatch, "acquisition", "H")["validCompleteUsed"] == 0
    assert route_summary(mismatch, "acquisition", "R")["validCompleteUsed"] == 0

    receipt = {
        "schemaVersion": 1,
        "validatedUtc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "passed",
        "summarizer": {"path": str(HERE / "summarize.py"), "sha256": sha(HERE / "summarize.py")},
        "validationScript": {"path": str(Path(__file__).resolve()), "sha256": sha(Path(__file__).resolve())},
        "cases": cases,
        "handChecks": {
            "H1Milliseconds": {"acquisition": 10.0, "directRecovery": 20.0, "requestToReady": 50.0},
            "R1Milliseconds": {"acquisition": 5.0, "directRecovery": 10.0, "requestToReady": 30.0},
            "pair1HistoryMinusReconstructionMilliseconds": {"acquisition": 5.0, "directRecovery": 10.0, "requestToReady": 20.0},
            "pair4ZeroMillisecondsIncluded": {"acquisition": 0.0, "directRecovery": 0.0, "requestToReady": 0.0},
            "pairSummaryMediansWithZero": {"acquisition": 2.5, "directRecovery": 5.0, "requestToReady": 10.0},
            "routeDenominators": 6,
            "feasibilityExcluded": True,
            "failureMissingDuplicateIdentityMismatchCovered": True,
            "readyBeforeDirectInvalidAndExcluded": True,
        },
    }
    receipt_path = root / "validation.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "passed", "receipt": str(receipt_path), "sha256": sha(receipt_path)}, indent=2))


if __name__ == "__main__":
    main()
