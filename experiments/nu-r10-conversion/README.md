# Nu R10 Prime conversion feasibility probe

This package reproduces the bounded Prime 11.5.1 conversion result reported in
[`docs/nu-conversion-feasibility-2026-10-15.md`](../../docs/nu-conversion-feasibility-2026-10-15.md).
Its frozen predictions and falsifiers are in
[`pre-execution-contract.md`](pre-execution-contract.md).

The probe exercises Prime directly. It does not load Nu, Gaia, or MMCC
Breakout. The seven outer field names mirror the selected Gameplay model, but
nested geometry and color use discriminating integer values instead of MMCC's
Vector3 and Color values. It does not cross Nu's mutable model slot or validate
shared references, callbacks, effects, reload synchronization, resumed
behavior, or an insertion point. The source-aware symbol augmentation is a
proposed isolated mapping, not an established Nu integration.

## Requirements and run

- .NET SDK 10.0.302, the version used for the recorded run and publication
  check;
- access to the packages fixed by `packages.lock.json`, either through the
  ordinary NuGet source or an existing package cache; and
- no Nu source tree or native dependency.

From the repository root, these commands work in PowerShell, Bash, and ordinary
command prompts:

```text
dotnet restore experiments/nu-r10-conversion/R10ConversionProbe.fsproj --locked-mode
dotnet build experiments/nu-r10-conversion/R10ConversionProbe.fsproj --no-restore --configuration Release
dotnet run --project experiments/nu-r10-conversion/R10ConversionProbe.fsproj --no-build --configuration Release
```

The program writes one Prime assembly-identity JSON line followed by eight case
JSON lines. Exit code zero means every frozen case matched its expected
observation. It does not convert the eight checks into evidence of live-reload
or gameplay success. `bin/`, `obj/`, package caches and full private attempt
logs are intentionally excluded. The small
[`result-receipt.json`](result-receipt.json) records the completed publication
check without checking in binaries or verbose output.

## Reading the result

The consequential adverse case is `raw-v0-to-v1-default`: conversion succeeds,
retains the representative V0 witness and supplies reward zero, so an
exception-only fallback does not run and cannot supply the required first-use
value 200. `explicit-v0-installation` shows that a source-edition-aware symbol
augmentation can produce the declared isolated values. It does not show where
that mapping can safely run in Nu or whether the resulting live application
state has the intended meaning. The positional nested-record case deliberately
demonstrates successful conversion with incorrect field meaning.
