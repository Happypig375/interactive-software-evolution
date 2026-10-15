# Nu R04 actual-application diagnostic probe

This package builds four source variants of the actual pinned MMCC Breakout project. It checks the effective compiler diagnostic at one selected match under the complete project graph. It performs no application runtime or candidate/model execution.

Read [`pre-execution-contract.md`](pre-execution-contract.md) for the frozen predictions and limits, and [`source-provenance.md`](source-provenance.md) for the exact source correspondence.

From the repository root, supply a verified Git archive of Nu pin `064f7ae92a8506689cd91aff5e6804a375d6ef3d` and a fresh output directory:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File experiments/nu-r04-application-diagnostics/run-probe.ps1 `
    -NuArchive '.artifacts/r03-feasibility-20261015/nu-064f7ae.tar' `
    -OutputRoot '.artifacts/r04-application-diagnostics-20261015/reproduction-01'
```

The runner verifies the archive and selected source hashes, extracts into the output directory, resolves SDK 10.0.302 from the tracked `global.json`, uses task-private CLI and NuGet homes, creates a separate artifacts path for every build, and retains exact variant sources, commands, full logs, diagnostic inventories, effective properties, assembly identities, and run metadata. It refuses a nonempty output directory.

The source tree is temporary experiment input. Do not point the runner at or build an existing Nu checkout. Package downloads are shared only among the four builds inside the selected fresh output directory.

Tracked compact receipts summarize the maintainer's original execution. Full source, logs, packages, objects, assets, and binaries remain under ignored `.artifacts/` and are not publication inputs.
