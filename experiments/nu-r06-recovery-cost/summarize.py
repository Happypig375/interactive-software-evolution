"""Offline descriptive summarizer for explicitly supplied R06 process receipts.

This program reads retained files only.  It does not launch Gaia, perform a
semantic replay, select a preferred attempt, or repair missing observations.
"""

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys
import time


COMPONENTS = {
    "acquisition": ("acquisitionStart", "acquisitionStop", "acquisitionTicks"),
    "directRecovery": ("recoveryStart", "recoveryDirectStop", "recoveryDirectTicks"),
    "requestToReady": ("recoveryStart", "readinessStop", "requestToReadyTicks"),
    "oracleWork": ("oracleWorkStart", "oracleWorkStop", "oracleWorkTicks"),
}
SUMMARY_COMPONENTS = ("acquisition", "directRecovery", "requestToReady")
EXPECTED_PROCESS_SCHEMA = 2
EXPECTED_DEADLINE_SECONDS = 600


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def is_integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def is_number(value):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value))


def identity_projection(entries):
    """Compare identities, not machine-specific absolute paths."""
    if not isinstance(entries, dict):
        raise ValueError("identity map is not an object")
    projected = {}
    for name, entry in sorted(entries.items()):
        if not isinstance(name, str) or not isinstance(entry, dict):
            raise ValueError("identity entry has the wrong shape")
        sha = entry.get("sha256")
        size = entry.get("bytes")
        if (not isinstance(sha, str) or len(sha) != 64
                or any(character not in "0123456789abcdefABCDEF" for character in sha)):
            raise ValueError(f"identity {name!r} has no SHA-256")
        if not is_integer(size) or size < 0:
            raise ValueError(f"identity {name!r} has invalid byte count")
        projected[name] = {"sha256": sha.lower(), "bytes": size}
    return projected


def identity_bundle(receipt):
    build = receipt.get("acceptedBuildReceipt")
    if not isinstance(build, dict):
        raise ValueError("acceptedBuildReceipt is missing")
    build_sha = build.get("sha256")
    if (not isinstance(build_sha, str) or len(build_sha) != 64
            or any(character not in "0123456789abcdefABCDEF" for character in build_sha)):
        raise ValueError("accepted build receipt SHA-256 is invalid")
    fixed = receipt.get("fixedInputs")
    if not isinstance(fixed, dict) or not fixed:
        raise ValueError("fixedInputs is missing")
    normalized_fixed = {}
    for name, sha in sorted(fixed.items()):
        if (not isinstance(sha, str) or len(sha) != 64
                or any(character not in "0123456789abcdefABCDEF" for character in sha)):
            raise ValueError(f"fixed input {name!r} has invalid SHA-256")
        normalized_fixed[name] = sha.lower()
    return {
        "acceptedBuildReceiptSha256": build_sha.lower(),
        "sourceIdentities": identity_projection(receipt.get("verifiedSourceIdentities")),
        "binaryIdentities": identity_projection(receipt.get("verifiedCommonBinaries")),
        "fixedInputs": normalized_fixed,
    }


def bundle_signature(bundle):
    encoded = json.dumps(bundle, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def read_json_file(path):
    raw = path.read_bytes()
    return raw, json.loads(raw.decode("utf-8-sig"))


def read_trace(path):
    raw = path.read_bytes()
    events = []
    errors = []
    for number, line in enumerate(raw.decode("utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
            if not isinstance(event, dict):
                raise ValueError("event is not an object")
            events.append(event)
        except (json.JSONDecodeError, ValueError) as error:
            errors.append(f"trace line {number}: {error}")
    return raw, events, errors


def one_event(events, name, errors, required):
    matching = [event for event in events if event.get("event") == name]
    if len(matching) > 1:
        errors.append(f"trace contains {len(matching)} {name!r} events")
    if required and len(matching) != 1:
        errors.append(f"successful trace requires exactly one {name!r} event")
    return matching[0] if len(matching) == 1 else None


def verify_declared_file(process_path, receipt, name):
    declaration = receipt.get("probeOutputs", {}).get(name) if isinstance(receipt.get("probeOutputs"), dict) else None
    path = process_path.parent / "probe" / name
    result = {
        "path": str(path),
        "declared": copy.deepcopy(declaration),
        "exists": path.is_file(),
        "actual": None,
        "status": "missing",
    }
    if not path.is_file():
        if declaration is not None:
            result["status"] = "declared-but-missing"
        return result
    actual = {"bytes": path.stat().st_size, "sha256": digest(path)}
    result["actual"] = actual
    if not isinstance(declaration, dict):
        result["status"] = "present-but-undeclared"
    elif declaration.get("bytes") == actual["bytes"] and declaration.get("sha256") == actual["sha256"]:
        result["status"] = "verified"
    else:
        result["status"] = "hash-or-size-mismatch"
    return result


def clock_interval(event, start_name, stop_name, ticks_name, frequency):
    raw = {
        "start": event.get(start_name) if isinstance(event, dict) else None,
        "stop": event.get(stop_name) if isinstance(event, dict) else None,
        "ticks": event.get(ticks_name) if isinstance(event, dict) else None,
        "frequency": frequency,
    }
    issues = []
    if not is_integer(frequency) or frequency <= 0:
        issues.append("stopwatch frequency is not a positive integer")
    if not is_integer(raw["start"]) or raw["start"] <= 0:
        issues.append(f"{start_name} is not a positive integer")
    if not is_integer(raw["stop"]) or raw["stop"] <= 0:
        issues.append(f"{stop_name} is not a positive integer")
    if not is_integer(raw["ticks"]) or raw["ticks"] < 0:
        issues.append(f"{ticks_name} is not a nonnegative integer")
    if (is_integer(raw["start"]) and is_integer(raw["stop"])
            and is_integer(raw["ticks"]) and raw["stop"] - raw["start"] != raw["ticks"]):
        issues.append(f"{ticks_name} does not equal stop minus start")
    valid = not issues
    return {
        "raw": raw,
        "valid": valid,
        "issues": issues,
        "milliseconds": raw["ticks"] * 1000.0 / frequency if valid else None,
    }


def accumulated_ticks(value, frequency):
    valid = is_integer(value) and value >= 0 and is_integer(frequency) and frequency > 0
    return {
        "ticks": value,
        "frequency": frequency,
        "valid": valid,
        "milliseconds": value * 1000.0 / frequency if valid else None,
    }


def compare_fields(left, right, fields, label, errors):
    if not isinstance(left, dict) or not isinstance(right, dict):
        return
    for field in fields:
        if field in left and field in right and left[field] != right[field]:
            errors.append(f"{label} differs for {field}: {left[field]!r} versus {right[field]!r}")


def inspect_input(index, supplied_path, expected_by_id):
    path = supplied_path.resolve(strict=False)
    record = {
        "inputIndex": index,
        "suppliedPath": str(supplied_path),
        "resolvedPath": str(path),
        "processFile": None,
        "processReceipt": None,
        "attemptId": None,
        "assigned": None,
        "identityBundle": None,
        "identitySignature": None,
        "traceVerification": None,
        "resultVerification": None,
        "traceEvents": [],
        "resultFile": None,
        "rawClocks": {},
        "crossClockValidation": None,
        "clockPairs": [],
        "gcAndMemorySamples": [],
        "auxiliaryTimes": {},
        "runtimeOutcome": None,
        "validationErrors": [],
        "validationWarnings": [],
    }
    errors = record["validationErrors"]
    warnings = record["validationWarnings"]
    if path.name != "process.json":
        errors.append("supplied path is not named process.json")
    if not path.is_file():
        errors.append("supplied process receipt does not exist")
        return record
    try:
        raw, receipt = read_json_file(path)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        errors.append(f"cannot read process receipt: {error}")
        return record
    record["processFile"] = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    record["processReceipt"] = receipt
    if not isinstance(receipt, dict):
        errors.append("process receipt is not an object")
        return record
    attempt = receipt.get("attempt")
    if isinstance(attempt, dict):
        record["attemptId"] = attempt.get("attemptId")
    else:
        errors.append("process receipt attempt is missing")
    assigned = expected_by_id.get(record["attemptId"])
    record["assigned"] = copy.deepcopy(assigned)
    if assigned is None:
        errors.append("receipt attemptId is not assigned by attempt-plan.json")
    elif attempt != assigned:
        errors.append("embedded attempt assignment differs from attempt-plan.json")
    if receipt.get("schemaVersion") != EXPECTED_PROCESS_SCHEMA:
        errors.append(f"process schemaVersion is not {EXPECTED_PROCESS_SCHEMA}")
    if receipt.get("timeoutSeconds") != EXPECTED_DEADLINE_SECONDS:
        errors.append(f"process deadline is not {EXPECTED_DEADLINE_SECONDS} seconds")
    command = receipt.get("command")
    if assigned is not None:
        if not isinstance(command, list) or len(command) < 5:
            errors.append("process command is missing")
        elif command[2:5] != [assigned["route"], assigned["kind"], assigned["attemptId"]]:
            errors.append("process command route/kind/id differs from assignment")
    try:
        record["identityBundle"] = identity_bundle(receipt)
        record["identitySignature"] = bundle_signature(record["identityBundle"])
    except ValueError as error:
        errors.append(f"identity receipt invalid: {error}")

    trace_verification = verify_declared_file(path, receipt, "trace.jsonl")
    result_verification = verify_declared_file(path, receipt, "result.json")
    record["traceVerification"] = trace_verification
    record["resultVerification"] = result_verification
    integrity_statuses = {trace_verification["status"], result_verification["status"]}
    if "hash-or-size-mismatch" in integrity_statuses or "declared-but-missing" in integrity_statuses:
        errors.append("a declared probe output does not match the process receipt")
    if "present-but-undeclared" in integrity_statuses:
        errors.append("a probe output exists without a process-receipt identity")

    events = []
    if trace_verification["exists"]:
        try:
            _, events, trace_errors = read_trace(Path(trace_verification["path"]))
            errors.extend(trace_errors)
            record["traceEvents"] = events
        except (OSError, UnicodeError) as error:
            errors.append(f"cannot read trace: {error}")
    result_file = None
    if result_verification["exists"]:
        try:
            _, result_file = read_json_file(Path(result_verification["path"]))
            if not isinstance(result_file, dict):
                errors.append("result.json is not an object")
                result_file = None
            record["resultFile"] = result_file
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            errors.append(f"cannot read result.json: {error}")

    timed_out = receipt.get("timedOut") is True
    exit_code = receipt.get("exitCode")
    driver_error = receipt.get("driverError")
    process_failed = timed_out or driver_error is not None or (is_integer(exit_code) and exit_code != 0)
    provisional_success = not process_failed and exit_code == 0
    configuration = one_event(events, "configuration", errors, provisional_success)
    acquisition = one_event(events, "acquisition", errors, provisional_success)
    readiness = one_event(events, "readiness-timing", errors, provisional_success)
    result_event = one_event(events, "result", errors, provisional_success)
    engine_exit = one_event(events, "engine-exit", errors, provisional_success)

    identity_fields = ("attemptId", "attemptKind", "route")
    if assigned is not None:
        expected_identity = {"attemptId": assigned["attemptId"], "attemptKind": assigned["kind"], "route": assigned["route"]}
        for label, observed in (("configuration", configuration), ("result event", result_event), ("result.json", result_file)):
            if isinstance(observed, dict):
                compare_fields(observed, expected_identity, identity_fields, label, errors)
                for field in identity_fields:
                    if field not in observed:
                        errors.append(f"{label} lacks {field}")
    result_fields = ("pass", "exitCode", "stopwatchFrequency", "acquisitionTicks",
                     "recoveryDirectTicks", "requestToReadyTicks", "oracleWorkTicks",
                     "updates", "timeUpdates", "callbacks")
    compare_fields(result_event, result_file, result_fields, "trace result and result.json", errors)
    if isinstance(configuration, dict) and isinstance(result_event, dict):
        compare_fields(configuration, result_event, ("stopwatchFrequency",), "configuration and result", errors)
    if isinstance(acquisition, dict) and isinstance(result_event, dict):
        compare_fields(acquisition, result_event, ("route",), "acquisition and result", errors)
        if acquisition.get("start") != result_event.get("acquisitionStart"):
            errors.append("acquisition event start differs from result acquisitionStart")
        if acquisition.get("stop") != result_event.get("acquisitionStop"):
            errors.append("acquisition event stop differs from result acquisitionStop")
        if acquisition.get("ticks") != result_event.get("acquisitionTicks"):
            errors.append("acquisition event ticks differ from result acquisitionTicks")
    if isinstance(readiness, dict) and isinstance(result_event, dict):
        mapping = {
            "start": "recoveryStart",
            "directStop": "recoveryDirectStop",
            "readyStop": "readinessStop",
            "directTicks": "recoveryDirectTicks",
            "requestToReadyTicks": "requestToReadyTicks",
            "oracleWorkTicks": "oracleWorkTicks",
        }
        for left_name, right_name in mapping.items():
            if readiness.get(left_name) != result_event.get(right_name):
                errors.append(f"readiness event {left_name} differs from result {right_name}")

    frequency = result_event.get("stopwatchFrequency") if isinstance(result_event, dict) else None
    for name, names in COMPONENTS.items():
        record["rawClocks"][name] = clock_interval(result_event, *names, frequency)
    direct_clock = record["rawClocks"]["directRecovery"]
    ready_clock = record["rawClocks"]["requestToReady"]
    cross_issues = []
    if direct_clock["valid"] and ready_clock["valid"]:
        direct_raw, ready_raw = direct_clock["raw"], ready_clock["raw"]
        if direct_raw["start"] != ready_raw["start"]:
            cross_issues.append("direct recovery and request-to-ready do not share recoveryStart")
        if direct_raw["stop"] > ready_raw["stop"]:
            cross_issues.append("recoveryDirectStop is after readinessStop")
        if direct_raw["ticks"] > ready_raw["ticks"]:
            cross_issues.append("recoveryDirectTicks exceeds requestToReadyTicks")
        cross_available = True
    else:
        cross_available = False
        cross_issues.append("cross-interval ordering unavailable because an individual interval is invalid")
    record["crossClockValidation"] = {
        "raw": {
            "recoveryStart": direct_clock["raw"]["start"],
            "recoveryDirectStop": direct_clock["raw"]["stop"],
            "readinessStop": ready_clock["raw"]["stop"],
            "recoveryDirectTicks": direct_clock["raw"]["ticks"],
            "requestToReadyTicks": ready_clock["raw"]["ticks"],
        },
        "available": cross_available,
        "valid": cross_available and not cross_issues,
        "issues": cross_issues,
    }
    clock_pairs = result_event.get("clockPairs") if isinstance(result_event, dict) else None
    if isinstance(clock_pairs, list):
        for pair_index, pair in enumerate(clock_pairs, 1):
            item = clock_interval(pair, "start", "stop", "ticks", frequency)
            item["pair"] = pair_index
            record["clockPairs"].append(item)
    elif provisional_success:
        errors.append("successful result lacks clockPairs")

    samples = result_event.get("gcAndMemorySamples") if isinstance(result_event, dict) else None
    if isinstance(samples, list):
        record["gcAndMemorySamples"] = copy.deepcopy(samples)
    elif provisional_success:
        errors.append("successful result lacks gcAndMemorySamples")
    trace_ticks = result_event.get("traceWorkTicksBeforeResult") if isinstance(result_event, dict) else None
    record["auxiliaryTimes"] = {
        "oracleWork": record["rawClocks"]["oracleWork"],
        "traceWorkBeforeResult": accumulated_ticks(trace_ticks, frequency),
        "processElapsedSecondsNotComponentCost": receipt.get("processElapsedSecondsNotComponentCost"),
    }
    if is_number(receipt.get("processElapsedSecondsNotComponentCost")) is False:
        warnings.append("process elapsed time is missing or non-numeric")

    event_pass = result_event.get("pass") if isinstance(result_event, dict) else None
    file_pass = result_file.get("pass") if isinstance(result_file, dict) else None
    if event_pass is False or file_pass is False:
        process_failed = True
    if provisional_success and (event_pass is not True or file_pass is not True):
        errors.append("zero-exit process lacks matching successful result records")
    if provisional_success:
        for name in SUMMARY_COMPONENTS:
            if not record["rawClocks"][name]["valid"]:
                errors.append(f"successful result has invalid {name} clock")
        if direct_clock["valid"] and ready_clock["valid"] and not record["crossClockValidation"]["valid"]:
            errors.append("successful result has impossible direct-recovery/request-to-ready ordering")
    record["runtimeOutcome"] = {
        "timedOut": receipt.get("timedOut"),
        "exitCode": exit_code,
        "driverError": driver_error,
        "traceResultPass": event_pass,
        "resultFilePass": file_pass,
        "classificationBeforeIntegrity": "fail" if process_failed else ("pass" if provisional_success else "invalid"),
    }
    return record


def percentile_summary(values):
    if not values:
        return {"medianMilliseconds": None, "rangeMilliseconds": None}
    return {
        "medianMilliseconds": statistics.median(values),
        "rangeMilliseconds": {"minimum": min(values), "maximum": max(values)},
    }


def markdown_number(value):
    return "—" if value is None else f"{value:.6f}"


def compact_clock(attempt, name):
    clock = attempt.get("rawClocks", {}).get(name, {})
    raw = clock.get("raw", {})
    ticks = raw.get("ticks")
    milliseconds = clock.get("milliseconds")
    return f"{ticks if ticks is not None else '—'} / {markdown_number(milliseconds)}"


def build_report(plan_path, process_paths):
    plan_raw, plan = read_json_file(plan_path)
    if plan.get("schemaVersion") != 1:
        raise ValueError("attempt-plan.json schemaVersion is not 1")
    ordered = plan.get("feasibility", []) + plan.get("measuredOrder", [])
    expected_by_id = {entry["attemptId"]: entry for entry in ordered}
    if len(expected_by_id) != len(ordered):
        raise ValueError("attempt-plan.json contains duplicate attempt IDs")
    inputs = [inspect_input(index, path, expected_by_id) for index, path in enumerate(process_paths, 1)]

    by_id = {}
    for record in inputs:
        if isinstance(record.get("attemptId"), str):
            by_id.setdefault(record["attemptId"], []).append(record)
    duplicate_ids = sorted(attempt_id for attempt_id, records in by_id.items() if len(records) > 1)
    for attempt_id in duplicate_ids:
        for record in by_id[attempt_id]:
            record["validationErrors"].append(f"duplicate supplied attempt ID {attempt_id}; no receipt selected")

    measured_records = [record for record in inputs
                        if record.get("assigned", {}).get("kind") == "measured"
                        and len(by_id.get(record.get("attemptId"), [])) == 1]
    signature_groups = {}
    missing_identity_indices = []
    for record in measured_records:
        signature = record.get("identitySignature")
        if signature is None:
            missing_identity_indices.append(record["inputIndex"])
        else:
            signature_groups.setdefault(signature, []).append(record["attemptId"])
    series_mismatch = len(signature_groups) > 1
    if series_mismatch:
        for record in measured_records:
            record["validationErrors"].append("measured-series source/binary/build identity mismatch; no identity group selected")

    assigned_attempts = []
    for assigned in ordered:
        records = by_id.get(assigned["attemptId"], [])
        row = copy.deepcopy(assigned)
        row["inputIndices"] = [record["inputIndex"] for record in records]
        if not records:
            row.update({"status": "not-run", "statusReasons": ["no process.json supplied"],
                        "rawClocks": {}, "crossClockValidation": None, "clockPairs": [],
                        "gcAndMemorySamples": [], "auxiliaryTimes": {}})
        elif len(records) > 1:
            row.update({"status": "invalid", "statusReasons": ["duplicate attempt ID; no receipt selected"],
                        "rawClocks": {}, "crossClockValidation": None, "clockPairs": [],
                        "gcAndMemorySamples": [], "auxiliaryTimes": {}})
        else:
            record = records[0]
            outcome = record.get("runtimeOutcome", {}).get("classificationBeforeIntegrity")
            if record["validationErrors"]:
                status = "invalid"
                reasons = list(record["validationErrors"])
            elif outcome == "pass":
                status, reasons = "pass", []
            elif outcome == "fail":
                status, reasons = "fail", ["retained process or probe outcome failed"]
            else:
                status, reasons = "invalid", ["process outcome cannot be classified"]
            row.update({
                "status": status,
                "statusReasons": reasons,
                "rawClocks": copy.deepcopy(record["rawClocks"]),
                "crossClockValidation": copy.deepcopy(record["crossClockValidation"]),
                "clockPairs": copy.deepcopy(record["clockPairs"]),
                "gcAndMemorySamples": copy.deepcopy(record["gcAndMemorySamples"]),
                "auxiliaryTimes": copy.deepcopy(record["auxiliaryTimes"]),
                "inputIndex": record["inputIndex"],
            })
        assigned_attempts.append(row)

    measured = [row for row in assigned_attempts if row["kind"] == "measured"]
    route_summaries = []
    for component in SUMMARY_COMPONENTS:
        for route in ("H", "R"):
            route_rows = [row for row in measured if row["route"] == route]
            used = [row for row in route_rows if row["status"] == "pass"
                    and row["rawClocks"].get(component, {}).get("valid")]
            values = [row["rawClocks"][component]["milliseconds"] for row in used]
            counts = {status: sum(row["status"] == status for row in route_rows)
                      for status in ("pass", "fail", "not-run", "invalid")}
            route_summaries.append({
                "component": component,
                "route": route,
                "assignedDenominator": len(route_rows),
                "validCompleteUsed": len(used),
                "statusCounts": counts,
                "attemptIdsUsed": [row["attemptId"] for row in used],
                **percentile_summary(values),
            })

    rows_by_id = {row["attemptId"]: row for row in assigned_attempts}
    pairs = []
    for pair_number in range(1, 7):
        history, reconstruction = rows_by_id[f"H{pair_number}"], rows_by_id[f"R{pair_number}"]
        complete = history["status"] == reconstruction["status"] == "pass"
        differences = {}
        for component in SUMMARY_COMPONENTS:
            h_clock = history.get("rawClocks", {}).get(component, {})
            r_clock = reconstruction.get("rawClocks", {}).get(component, {})
            usable = complete and h_clock.get("valid") and r_clock.get("valid")
            differences[component] = {
                "historyMilliseconds": h_clock.get("milliseconds") if h_clock else None,
                "reconstructionMilliseconds": r_clock.get("milliseconds") if r_clock else None,
                "historyMinusReconstructionMilliseconds": h_clock["milliseconds"] - r_clock["milliseconds"] if usable else None,
            }
        pairs.append({
            "pair": pair_number,
            "historyStatus": history["status"],
            "reconstructionStatus": reconstruction["status"],
            "validCompletePair": complete,
            "missingOrInvalidReason": None if complete else f"H{pair_number}={history['status']}; R{pair_number}={reconstruction['status']}",
            "differences": differences,
        })
    pair_summaries = []
    for component in SUMMARY_COMPONENTS:
        values = [pair["differences"][component]["historyMinusReconstructionMilliseconds"]
                  for pair in pairs if pair["differences"][component]["historyMinusReconstructionMilliseconds"] is not None]
        pair_summaries.append({
            "component": component,
            "assignedPairDenominator": 6,
            "validCompletePairsUsed": len(values),
            "missingOrInvalidPairs": [pair["pair"] for pair in pairs if not pair["validCompletePair"]],
            **percentile_summary(values),
        })

    unassigned_inputs = [record["inputIndex"] for record in inputs if record.get("assigned") is None]
    report = {
        "schemaVersion": 1,
        "generatedUtc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "programScope": "offline descriptive summarization only; no Gaia run, semantic replay, attempt selection, imputation, exclusion, or benefit inference",
        "attemptPlan": {"path": str(plan_path), "bytes": len(plan_raw), "sha256": hashlib.sha256(plan_raw).hexdigest(), "plan": plan},
        "suppliedInputs": inputs,
        "assignedAttempts": assigned_attempts,
        "integrityFlags": {
            "duplicateAttemptIds": duplicate_ids,
            "unassignedInputIndices": unassigned_inputs,
            "measuredIdentitySignatures": signature_groups,
            "measuredInputsMissingIdentity": missing_identity_indices,
            "measuredSeriesMismatch": series_mismatch,
            "noIdentityGroupSelected": series_mismatch,
        },
        "descriptiveSummaries": {
            "eligibility": "measured, assigned, unique, identity-consistent, successful attempts with complete validated clocks only",
            "feasibilityAttemptsExcluded": ["FH", "FR"],
            "byRoute": route_summaries,
            "pairs": pairs,
            "historyMinusReconstruction": pair_summaries,
        },
        "caveats": [
            "Medians and ranges are descriptive for retained valid complete measured attempts only; they are not p-values or benefit estimates.",
            "Failed, invalid, missing, duplicate, and not-run attempts remain in their assigned denominators; no attempt is replaced, imputed, or deleted as an outlier.",
            "Measured-series identity consistency compares the build, source, binary, and fixed-input SHA/byte identities embedded in each process receipt; it does not rehash mutable external paths.",
            "Acquisition, direct recovery, request-to-ready, oracle work, trace work, and whole-process elapsed time are separate clocks.",
            "allocatedBytesApproximate uses GC.GetTotalAllocatedBytes(false), is process-wide and approximate, and excludes native allocations; zero difference does not establish zero allocation.",
            "Collection counts and phase-boundary counter differences can include engine/runtime and observation work; no forced collection or GC attribution is inferred.",
            "managedHeapBytesSecondary excludes fragmentation and does not measure retained checkpoint roots; working-set/private bytes include native and unrelated process memory and do not establish retention or release.",
            "The observations concern the declared one-checkpoint B0 service and do not establish total maintenance value, efficacy, or population benefit.",
        ],
    }
    return report


def render_markdown(report):
    lines = [
        "# R06 offline recovery-cost summary",
        "",
        "This is a descriptive report over explicitly supplied retained receipts. It did not run Gaia or replay semantics.",
        "",
        "## Assigned attempts",
        "",
        "| ID | Kind | Route | Pair | Status | Input | Acquisition ticks / ms | Direct ticks / ms | Request-to-ready ticks / ms |",
        "| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in report["assignedAttempts"]:
        lines.append("| {attemptId} | {kind} | {route} | {pair} | {status} | {input} | {acq} | {direct} | {ready} |".format(
            attemptId=row["attemptId"], kind=row["kind"], route=row["route"],
            pair=row.get("pair", "—"), status=row["status"], input=row.get("inputIndex", "—"),
            acq=compact_clock(row, "acquisition"), direct=compact_clock(row, "directRecovery"),
            ready=compact_clock(row, "requestToReady")))
    lines.extend(["", "## Measured route summaries", "",
                  "| Component | Route | Used / assigned | Status counts P/F/N/I | Median ms | Range ms |",
                  "| --- | --- | ---: | --- | ---: | --- |"])
    for item in report["descriptiveSummaries"]["byRoute"]:
        counts = item["statusCounts"]
        range_ = item["rangeMilliseconds"]
        range_text = "—" if range_ is None else f"{range_['minimum']:.6f}–{range_['maximum']:.6f}"
        lines.append(f"| {item['component']} | {item['route']} | {item['validCompleteUsed']} / {item['assignedDenominator']} | "
                     f"{counts['pass']}/{counts['fail']}/{counts['not-run']}/{counts['invalid']} | "
                     f"{markdown_number(item['medianMilliseconds'])} | {range_text} |")
    lines.extend(["", "## Valid complete pair differences (H − R)", "",
                  "| Pair | H | R | Acquisition ms | Direct ms | Request-to-ready ms |",
                  "| ---: | --- | --- | ---: | ---: | ---: |"])
    for pair in report["descriptiveSummaries"]["pairs"]:
        lines.append(f"| {pair['pair']} | {pair['historyStatus']} | {pair['reconstructionStatus']} | "
                     f"{markdown_number(pair['differences']['acquisition']['historyMinusReconstructionMilliseconds'])} | "
                     f"{markdown_number(pair['differences']['directRecovery']['historyMinusReconstructionMilliseconds'])} | "
                     f"{markdown_number(pair['differences']['requestToReady']['historyMinusReconstructionMilliseconds'])} |")
    lines.extend(["", "Pair-summary medians and ranges:", ""])
    for item in report["descriptiveSummaries"]["historyMinusReconstruction"]:
        range_ = item["rangeMilliseconds"]
        range_text = "—" if range_ is None else f"{range_['minimum']:.6f} to {range_['maximum']:.6f} ms"
        lines.append(f"- {item['component']}: {item['validCompletePairsUsed']}/6 pairs; median "
                     f"{markdown_number(item['medianMilliseconds'])} ms; range {range_text}; "
                     f"missing/invalid pairs {item['missingOrInvalidPairs'] or 'none'}.")
    flags = report["integrityFlags"]
    lines.extend(["", "## Integrity and scope", "",
                  f"- Duplicate attempt IDs: {flags['duplicateAttemptIds'] or 'none'}.",
                  f"- Measured-series identity mismatch: {str(flags['measuredSeriesMismatch']).lower()}.",
                  f"- Measured inputs missing identity: {flags['measuredInputsMissingIdentity'] or 'none'}.",
                  "- Feasibility attempts FH and FR are reported above and excluded from measured summaries.",
                  "- Raw receipts, trace events, clocks, GC/memory samples, validation findings, and separate oracle/trace/process times are retained in `summary.json`.",
                  ""])
    lines.extend(f"- {caveat}" for caveat in report["caveats"])
    return "\n".join(lines) + "\n"


def main(argv=None):
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("process_receipts", nargs="+", type=Path,
                        help="explicit retained process.json paths; no discovery or latest selection is performed")
    parser.add_argument("--output", required=True, type=Path, help="new output directory")
    args = parser.parse_args(argv)
    output = args.output.resolve(strict=False)
    if output.exists():
        parser.error("output directory must be new")
    report = build_report(here / "attempt-plan.json", args.process_receipts)
    markdown = render_markdown(report)
    output.mkdir(parents=True, exist_ok=False)
    (output / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (output / "summary.md").write_text(markdown, encoding="utf-8", newline="\n")
    print(json.dumps({
        "output": str(output),
        "summaryJsonSha256": digest(output / "summary.json"),
        "summaryMarkdownSha256": digest(output / "summary.md"),
        "suppliedInputs": len(report["suppliedInputs"]),
        "statusCounts": {status: sum(row["status"] == status for row in report["assignedAttempts"])
                         for status in ("pass", "fail", "not-run", "invalid")},
        "measuredSeriesMismatch": report["integrityFlags"]["measuredSeriesMismatch"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
