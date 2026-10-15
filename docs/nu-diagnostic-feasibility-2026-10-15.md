# R04 / D1 compiler-diagnostic feasibility, 2026-10-15

**Maintainer disposition, 2026-10-15:** source cases, runner and retained receipts have been reviewed and accepted for publication at the bounded scope below. This is AI maintainer review, not human scientific approval or an independent replication.

## Result

The bounded independent probe supports the narrow diagnostic premise and exposes its limits. Under .NET SDK 10.0.302 and the selected Nu project's explicit warning policy, adding an unhandled union case to the explicit `Playing | Quit` form produced one unique FS0025 **warning**, not an error; the build succeeded. The equivalent wildcard form produced no FS0025. This held for a `ReadyToServe` case needing distinct local behavior and a `Paused` case for which identity was declared correct.

The pure current-domain matrix returned equal records for the explicit and wildcard forms on all eight combinations of `Playing`/`Quit`, zero/positive lives and zero/positive brick count. This is finite local evidence for the adapted match, not whole-Nu observational equivalence.

The behavior checks give the necessary adverse results. The wildcard was silent and wrong for the declared `ReadyToServe` paddle step. Enumerating `ReadyToServe` with the wrong identity body was also warning-free and wrong. Conversely, the wildcard was silent and correct for the declared paused identity behavior. FS0025 therefore provides a source-site inspection opportunity; it neither entails the successor behavior nor implies that editing the site has value.

## Frozen construction

The pre-execution comparison, predictions and falsifiers were written before the first command and are preserved in the tracked [`pre-execution-contract.md`](../experiments/nu-r04-diagnostics/pre-execution-contract.md). The input was the integrity-checked copy of Nu `064f7ae92a8506689cd91aff5e6804a375d6ef3d` in `.artifacts/r03-feasibility-20261015/source`; its manifest reports archive SHA-256 `eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b`, 3,240 checked files and no mismatches. The selected `Gameplay.fs` hash was `571E2A5CE3F0630972F2FBE4E9A6A3C376BCF4D1A74589D14C882B2EE0DB1423` before and after the probe.

Tracked [`source-provenance.md`](../experiments/nu-r04-diagnostics/source-provenance.md) preserves the exact pinned lines used: the `Playing | Quit` union at source lines 9-11, the guard at lines 89-90 and terminal clause at lines 167-168. The derived case files preserve the names and guard but replace the Nu-dependent record and active update body with a deterministic five-field pure record. This made the compiler contrast independent of the concurrent Nu build; it is an adaptation.

The exact transformations are published in tracked [`cases`](../experiments/nu-r04-diagnostics/cases/):

| Case | Derived source lines that define the contrast |
| --- | --- |
| Current baseline | `baseline.fs` lines 3-5 define the original domain; lines 19-27 place `Playing | Quit` and `_` beside the identical guard |
| Distinct explicit successor | `successor-distinct-explicit.fs` line 6 adds `ReadyToServe`; lines 18-21 leave the explicit terminal pattern unchanged |
| Distinct wildcard successor | `successor-distinct-catchall.fs` line 6 adds `ReadyToServe`; line 21 uses `_` |
| Exhaustive but wrong successor | `successor-distinct-explicit-wrong.fs` line 21 enumerates `ReadyToServe` with the identity body |
| Legitimate-fallback explicit successor | `successor-fallback-explicit.fs` line 6 adds `Paused`; lines 18-21 leave the explicit terminal pattern unchanged |
| Legitimate-fallback wildcard successor | `successor-fallback-catchall.fs` line 6 adds `Paused`; line 21 uses `_` |

[`case-hashes.tsv`](../experiments/nu-r04-diagnostics/case-hashes.tsv) fixes every derived source identity. The tracked project and portable runner are [`R04DiagnosticProbe.fsproj`](../experiments/nu-r04-diagnostics/R04DiagnosticProbe.fsproj) and [`run-probe.ps1`](../experiments/nu-r04-diagnostics/run-probe.ps1). Every case used `net10.0`, warning level 5, `WarnOn=FS1182`, the Nu project's six explicit suppressions, and its explicit FS0026/FS0049/FS3239 error list. The effective compiler invocation added SDK-inherited numeric `3239`, set `TreatWarningsAsErrors=false`, and did not suppress or promote FS0025.

## Observations

| Case | Unique FS0025 diagnostic | Build | Behavioral observation | Run exit |
| --- | --- | --- | --- | ---: |
| Current baseline | none | success | 8 samples, 0 explicit/wildcard mismatches | 0 |
| Distinct explicit, new case unhandled | warning naming `ReadyToServe` | success | `Microsoft.FSharp.Core.MatchFailureException` when reached | 2 |
| Distinct wildcard | none | success | required paddle step failed: actual 12, expected 16 | 1 |
| Distinct explicit, exhaustive wrong body | none | success | required paddle step failed: actual 12, expected 16 | 1 |
| Legitimate-fallback explicit, new case unhandled | warning naming `Paused` | success | `Microsoft.FSharp.Core.MatchFailureException` when reached | 2 |
| Legitimate-fallback wildcard | none | success | paused identity passed | 0 |

MSBuild prints each FS0025 once at compilation and repeats it once in the build summary, so the tracked [`original-results.tsv`](../experiments/nu-r04-diagnostics/original-results.tsv) records two raw log mentions for each explicit unhandled successor. Deduplicating by source location and message yields one diagnostic in each. Full original build and run streams remain privately retained under `.artifacts/r04-diagnostics-20261015/logs/`, including the expected nonzero behavior exits.

The frozen toolchain was:

- .NET SDK 10.0.302, SDK commit `35b593bebf`; MSBuild 18.6.11; .NET host/runtime 10.0.10.
- F# Interactive 15.2.302.0 for F# 10.0.
- `fsc.dll` product version `15.2.302-servicing.26329.109+35b593bebfcba58f8e78298cef14c2761f5d86c6`, SHA-256 `3DB18554E1D49181C6A184EE1AD4C8C0C5DB457DE7F3CCE2AF5A098497B79A68`.
- Resolved `FSharp.Core` 10.1.302, installed from the SDK library pack into the task-private package cache.

The first runner attempt stopped before any case build because PowerShell promoted an informational `dotnet fsi` stderr line while `ErrorActionPreference` was `Stop`; it also launched `dotnet --info` from the repository root, which did not report the task-local `global.json`. Its completed tool output was preserved as `logs/attempt-01-dotnet-info.log`; the interruption occurred before an FSI log was written. The repair changed only runner output handling and set the working directory to the artifact root. No case source, policy or prediction changed.

## Reproduction and disposition

From the repository root:

```powershell
$nuSource = Resolve-Path '.artifacts/r03-feasibility-20261015/source'
powershell -NoProfile -ExecutionPolicy Bypass -File experiments/nu-r04-diagnostics/run-probe.ps1 `
    -NuSourceRoot $nuSource `
    -OutputRoot '.artifacts/nu-r04-diagnostics/review-01'
```

The tracked [`README`](../experiments/nu-r04-diagnostics/README.md) documents Git-checkout and integrity-manifest routes. The runner pins SDK 10.0.302, verifies the Nu pin and selected source hash, requires a fresh parameterized output directory, uses task-private `DOTNET_CLI_HOME`, NuGet package, `obj` and `bin` directories, builds each case with a distinct `ProbeCase`, and retains commands and outputs. The pinned Nu source is neither modified nor built.

The final portable runner was executed into the fresh private directory `.artifacts/nu-r04-diagnostics/publication-check-20261015-04`. All six rows matched the original receipt, including the two unique FS0025 warnings and expected adverse run exits; the compact tracked receipt is [`publication-check-results.tsv`](../experiments/nu-r04-diagnostics/publication-check-results.tsv). Publication-check attempts 01 and 02 stopped before any build on a Windows PowerShell 5.1 process-argument incompatibility; attempt 03 succeeded after portable quoting, and attempt 04 revalidated the final metadata-corrected script. All attempts remain preserved.

**Execution disposition: complete for the bounded compiler-diagnostic feasibility question.** The provisional audit claim is now updated from "unprobed" at this adapted site: under this exact SDK and reproduced checked-in source policy, an unhandled added case yields warning FS0025 while an equivalent wildcard is silent, and FS0025 is not build-blocking.

This does not validate the actual Nu application's runtime equivalence, any serve/pause temporal or lifecycle oracle, warning delivery or attention in an agent workflow, source-convention benefit, task prevalence or representative coverage. It also does not evaluate parent/imported policy in an eventual full Nu build beyond the selected project's explicit properties; the isolated effective invocation is preserved. A later source-integrated feasibility check would need to build an isolated copy of the actual project and independently observe its relevant runtime behavior. A later agent study still needs frozen information delivery, task provenance, valid alternatives, all-attempt accounting and independent behavioral scoring.

## Actual-project continuation, 2026-10-15

The [four actual MMCC project builds](nu-application-diagnostic-feasibility-2026-10-15.md)
now resolve the preceding full-graph diagnostic dependency. Both baselines and
both union-extended variants build successfully. Adding `Paused` to the explicit
arm yields one FS0025 warning; the wildcard remains silent. The unchanged
project also emits 210 dependency warnings in each variant. Exact source,
policy, package and assembly identities and both attempts are retained.

This extends compiler evidence only. A correct paused update fallback still
requires separate content, clock, trigger, effect and lifecycle work; the
application was not launched in this continuation. Runtime and agent-delivery
feasibility remain distinct next steps.
