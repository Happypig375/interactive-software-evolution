# R10 behavior-only Gaia reload probe

This package reproduces the bounded result reported in
[`docs/nu-live-reload-feasibility-2026-10-15.md`](../../docs/nu-live-reload-feasibility-2026-10-15.md).
It calls the ordinary pinned Gaia `tryReloadCode false` core through a small
guarded bridge. The gate covers functional MMCC model, projection, dispatcher,
and reward behavior across one halted reload. It does not cover the F9/menu
path, observed audio, framebuffer, native-host state, or a general insertion
point.

The prospective contract was frozen before execution in
[`pre-execution-contract.md`](pre-execution-contract.md).
The published contract differs from the frozen bytes only by removal of one
trailing empty line; both hashes are recorded in `result-receipt.json`.
The source preparer
checks the frozen archive SHA-256 before extraction, checks exact textual
anchors, and records original and instrumented hashes.
`LiveReload.fs` checks the raw post-reload model and dispatcher by actual
runtime `Type` identity, allowing the valid FSI-generated namespace prefix.
`compare.py` compares the accepted live run with a fresh reward-200
reconstruction.

## Requirements

- Windows x64 (the observed run used Windows 10.0.19045)
- Python 3.12
- .NET SDK 10.0.302 and runtime 10.0.10
- a Nu Git checkout containing commit
  `064f7ae92a8506689cd91aff5e6804a375d6ef3d`
- this repository's `experiments/nu-history-b1/checkpoint/gameplay.symbol`
- enough space for a fresh Nu archive, extracted source, project-local build
  outputs, logs, and a task-private NuGet cache

## Reproduction

Run from the repository root. Replace `A:/Nu` if the Nu checkout is elsewhere.
Use a new artifact directory: `prepare.py` and `run.py` refuse to overwrite an
existing preparation or attempt.

```powershell
$artifact = Resolve-Path .artifacts | ForEach-Object { Join-Path $_ 'r10-live-reload-reproduction' }
$env:NUGET_PACKAGES = Join-Path $artifact 'nuget-packages'
$sdk = (& dotnet --version).Trim()
if ($sdk -ne '10.0.302') { throw "R10 reproduction requires .NET SDK 10.0.302; found $sdk" }

python experiments/nu-r10-live-reload/prepare.py A:/Nu $artifact

dotnet build experiments/nu-r10-live-reload/LiveReload.fsproj `
  --configuration Release `
  -p:NuSource="$artifact/source"

$probe = Resolve-Path experiments/nu-r10-live-reload/bin/Release/net10.0/LiveReload.dll
$app = Resolve-Path "$artifact/source/Projects/Breakout Mmcc/bin/Release/net10.0/Breakout Mmcc.dll"
$seed = Resolve-Path experiments/nu-history-b1/checkpoint/gameplay.symbol
$gameplay = Resolve-Path "$artifact/source/Projects/Breakout Mmcc/Gameplay.fs"

python experiments/nu-r10-live-reload/run.py live $probe $app $seed `
  "$artifact/checkpoint" "$artifact/live-01" --gameplay-source $gameplay

dotnet build experiments/nu-r10-live-reload/LiveReload.fsproj `
  --configuration Release --no-restore `
  -p:NuSource="$artifact/source"

$app = Resolve-Path "$artifact/source/Projects/Breakout Mmcc/bin/Release/net10.0/Breakout Mmcc.dll"
python experiments/nu-r10-live-reload/run.py fresh $probe $app $seed `
  "$artifact/checkpoint" "$artifact/fresh-01"

python experiments/nu-r10-live-reload/compare.py `
  "$artifact/live-01/probe/trace.jsonl" `
  "$artifact/fresh-01/probe/trace.jsonl" `
  "$artifact/comparison.json"
```

The live runner waits for the fully observed old checkpoint, preserves its
receipt, changes exactly one `static member BrickReward = 100` occurrence to
`200`, and then permits reload. The fresh arm starts from the saved symbol with
the reward-200 binary. A passing comparison requires identical complete model
and projection snapshots before advance, identical live/fresh snapshots after
one update, zero sampled updates with Left or Right held, the declared event
word and delta, and a stable next halted observation. Native input event capture
or replay is not tested. Private artifacts contain all build and runtime
attempts; binaries, the Nu archive/source, caches, and large traces are
intentionally excluded from this package.
