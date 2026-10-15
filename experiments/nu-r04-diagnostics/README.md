# Nu R04 compiler-diagnostic feasibility probe

This package reproduces the bounded R04 / D1 probe recorded in [`docs/nu-diagnostic-feasibility-2026-10-15.md`](../../docs/nu-diagnostic-feasibility-2026-10-15.md). It compares explicit enumeration of Nu Breakout's current `Playing | Quit` cases with the locally equivalent wildcard, then adds one case needing distinct behavior and one case for which identity is a legitimate fallback.

The package tests compiler diagnostics and small pure functions. It does not build Nu, prove whole-Nu equivalence, test temporal/lifecycle behavior, measure agent attention or establish a maintenance benefit.

[`case-hashes.tsv`](case-hashes.tsv) records the source identities from the original run.

## Requirements and source identity

- Windows PowerShell 5.1 or PowerShell 7 or later.
- .NET SDK 10.0.302. [`global.json`](global.json) disables roll-forward.
- Nu source at revision `064f7ae92a8506689cd91aff5e6804a375d6ef3d`.
- Either a Git checkout at that exact HEAD or a JSON integrity manifest with the same `pin` and an empty `mismatches` array. The archived feasibility source uses a sibling `source-integrity.json`, which the runner discovers automatically.

Before invoking `dotnet`, the runner verifies the source identity route and requires `Projects/Breakout Mmcc/Gameplay.fs` SHA-256 `571E2A5CE3F0630972F2FBE4E9A6A3C376BCF4D1A74589D14C882B2EE0DB1423`. It checks that hash again after execution. [`source-provenance.md`](source-provenance.md) preserves the selected source lines and adaptation boundary.

## Run

From the repository root, using the preserved archive source:

```powershell
$nuSource = Resolve-Path '.artifacts/r03-feasibility-20261015/source'
powershell -NoProfile -ExecutionPolicy Bypass -File experiments/nu-r04-diagnostics/run-probe.ps1 `
    -NuSourceRoot $nuSource `
    -OutputRoot '.artifacts/nu-r04-diagnostics/review-01'
```

For an exact Git checkout, pass its root to `-NuSourceRoot`. If its integrity manifest is elsewhere, also pass `-NuIntegrityManifest <path>`.

`-OutputRoot` must be a fresh empty directory outside both the Nu source and this tracked package. When omitted, the runner creates a timestamped directory under `.artifacts/nu-r04-diagnostics/`. It stores the NuGet package cache, CLI home, `obj`, `bin`, full logs, command receipt and run metadata there. Reusing a nonempty output directory is rejected so earlier attempts are preserved.

The command exits successfully only when all six builds and run exits reproduce [`original-results.tsv`](original-results.tsv), both unique FS0025 counts match, and the selected source hash is unchanged. Expected run exits 1 and 2 are behavioral observations, not runner failures.

## Original observation

The original 2026-10-15 run used .NET SDK 10.0.302, F# compiler product version `15.2.302-servicing.26329.109`, and FSharp.Core 10.1.302. All six cases built. The two unchanged explicit successors each emitted one unique warning FS0025 and still built; wildcard successors emitted none. The current-domain matrix had zero mismatches across eight inputs. The legitimate paused wildcard passed, while the distinct wildcard and an exhaustive but wrong explicit branch failed the declared paddle oracle.

MSBuild wrote each FS0025 once during compilation and repeated it in the summary, so the original logs contain two raw mentions for each one unique diagnostic. The full original and publication-check logs, binaries, package cache and failed first runner attempt remain private under `.artifacts`; they are excluded from this package. [`pre-execution-contract.md`](pre-execution-contract.md) preserves the contract written before the first run.

The publication runner was checked on 2026-10-15. Attempts 01 and 02 stopped before any build because the first wrapper used a process argument API unavailable in Windows PowerShell 5.1. Attempt 03 reproduced all original rows after portable argument quoting was added. Attempt 04 reproduced them again after adding accurate start/completion metadata; [`publication-check-results.tsv`](publication-check-results.tsv) is its compact receipt. The four fresh private attempt directories are preserved under `.artifacts/nu-r04-diagnostics/`.
