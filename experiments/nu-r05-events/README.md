# Nu R05 event observation probe

This package reproduces the bounded event capability observation reported in
[`docs/nu-event-feasibility-2026-10-15.md`](../../docs/nu-event-feasibility-2026-10-15.md).
Read [`PROTOCOL.md`](PROTOCOL.md) for the observations, falsifiers, corrected
ordering assumption, and scope limits.

Requirements are Windows PowerShell 5.1 or PowerShell 7 or later, .NET SDK 10.0.302, and an already-built
Release `Nu.dll` from Nu source pin
`064f7ae92a8506689cd91aff5e6804a375d6ef3d`. The runner never builds or writes
the supplied Nu tree. It accepts either an exact Git checkout or the extraction
integrity manifest used by the archived feasibility run.

From the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File experiments/nu-r05-events/run-probe.ps1 `
  -NuSourceRoot (Resolve-Path '.artifacts/r03-feasibility-20261015/source') `
  -OutputRoot '.artifacts/nu-r05-events/review-01'
```

`OutputRoot` must be absent or empty and must be outside the Nu source and this
tracked package. A nonempty directory is rejected so no prior attempt is
overwritten. The output retains restore, build and runtime logs, binary/source
hashes, commands, and run metadata. `result-receipt.json` is the compact record
of the original and publication-check runs; generated binaries and full logs
remain under `.artifacts`.
