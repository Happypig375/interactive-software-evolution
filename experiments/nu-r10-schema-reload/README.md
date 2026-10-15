# R10 initializer-only schema reload probe

This package implements the prospective observation protocol in
[`pre-execution-contract.md`](pre-execution-contract.md) and its frozen
[`protocol-amendment-01.md`](protocol-amendment-01.md). It tests whether an
added immutable F# record field receives its application-required initializer
during Gaia's ordinary functional reload. It separately checks complete
old-field and entity-projection preservation and one declared post-edit brick
hit. Process exit zero is only a transport observation; every scientific
verdict is recomputed from the retained trace.

The completed live/fresh pair observed reward 0 after live conversion and 200 in
the fresh reference. Both preserved the old checkpoint and passed their declared
continuations, with scores 100 and 300 respectively. The live application mapping
failed. See the [execution record](../../docs/nu-schema-reload-feasibility-2026-10-16.md),
[complete selected observations](observations.json), [result receipt](result-receipt.json)
and [all-attempt ledger](attempt-ledger.json). This README's outcome/reproduction
prose was updated after both runs; the executed source/build snapshots retain
the original README identity.

The preparer requires the pinned Nu archive, creates a private source tree,
verifies pristine `Gameplay.fs`, and installs the same narrow Gaia research
bridge used by the accepted behavior-only reload probe. The runtime driver
makes exactly three byte-level replacements while preserving the original
UTF-8 BOM and CRLF line endings: the `BrickReward` field, its `empty`
initializer of 200, and the scoring use. The probe records the fresh initial
value before reconstruction, reconstructs all seven old fields plus an
explicit reward of 200, and obtains the live value from the actual FSI record.

## Compile-only preparation

The accepted 2026-10-16 construction uses .NET SDK 10.0.302 and runtime
10.0.10. Run from the repository root. Every preparation, objective-check,
and build-snapshot destination must be new.

```powershell
$artifact = 'A:/nu-value-research/.artifacts/r10-schema-20261016/initializer'
$package = 'A:/nu-value-research/experiments/nu-r10-schema-reload'
$archive = 'A:/nu-value-research/.artifacts/r10-live-reload-20261015/nu-pin.tar'
$source = "$artifact/source"
$gameplay = "$source/Projects/Breakout Mmcc/Gameplay.fs"
$application = "$source/Projects/Breakout Mmcc/bin/Release/net10.0/Breakout Mmcc.dll"
$probe = "$package/bin/Release/net10.0/SchemaReload.dll"
$env:NUGET_PACKAGES = 'A:/nu-value-research/.artifacts/r10-schema-20261016/nuget-packages'

python "$package/prepare.py" $archive $artifact

dotnet build "$package/SchemaReload.fsproj" `
  --configuration Release `
  -p:NuSource="$source" `
  -p:SourceRevisionId=064f7ae92a8506689cd91aff5e6804a375d6ef3d `
  *> "$artifact/build-full-graph-NEW.log"

python "$package/objective_checks.py" `
  "$artifact/objective-checks-NEW" `
  --gameplay-v0 $gameplay
```

The first build restores dependencies and builds the complete project graph.
Only later probe-source corrections against that already restored and built
tree use the incremental command recorded for build 04:

```powershell

dotnet build "$package/SchemaReload.fsproj" `
  --configuration Release --no-restore `
  -p:BuildProjectReferences=false `
  -p:NuSource="$source" `
  -p:SourceRevisionId=064f7ae92a8506689cd91aff5e6804a375d6ef3d `
  *> "$artifact/build-attempt-NEW.log"

python "$package/seal_build.py" v0 `
  "$artifact/build-snapshots/v0-build-NEW" `
  --archive $archive `
  --source-root $source `
  --probe $probe `
  --application $application `
  --gameplay-source $gameplay `
  --build-log "$artifact/build-attempt-NEW.log"
```

`seal_build.py` derives a 3,240-file manifest from the exact pinned archive and
accepts only the fixed instrumented Gaia file plus the arm-specific Gameplay
hash as overrides. It recursively copies every file under all four actual
probe/application/Gaia/Pipe output roots, including content, assets, native
files, configuration, and runtime files. It also copies the runner, checker,
toolchain inputs, both accepted source overrides, the exact archive-derived
source manifest, and the build log. It rejects a reused destination or a
same-file/hardlink result. The receipt binds the project-local launch
paths Gaia needs to the independent copies and their hashes. Compute and
externally accept the resulting `receipt.json` SHA-256 before a run; the runner
rechecks the full source manifest, exact output-root file sets and bytes, and
the actually probed toolchain before `Popen`.

## Native reproduction sequence

The maintainer accepted the source, runner, independent oracle and each arm
receipt before the recorded native launches. Reproduction follows this order
with new destinations and independently accepted receipt hashes. The completed
live failed mapping is retained; the fresh arm is a separate required-state
reference, not a replacement attempt.

```powershell
$seed = 'A:/nu-value-research/experiments/nu-history-b1/checkpoint/gameplay.symbol'
$checkpoint = "$artifact/runtime/checkpoint"
$v0Receipt = "$artifact/build-snapshots/v0-build-NEW/receipt.json"
$v0ReceiptHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $v0Receipt).Hash.ToLowerInvariant()

python "$package/run.py" live $probe $application $seed $checkpoint `
  "$artifact/runtime/live" `
  --gameplay-source $gameplay `
  --arm-receipt $v0Receipt `
  --arm-receipt-sha256 $v0ReceiptHash
```

The live runner requires seed SHA-256
`ffee72d91c6e4a32b650d45e9addd9e02e179163d0c8bbaaa8cddb9c92bc783a`.
At the ready boundary it checks every checkpoint file from `ready.json`, checks
`model-seven.json` against the public independent oracle, and writes an atomic
`checkpoint-binding.json` before installing the exact V1 source and sending
`go.signal`.

Only after the live edit completes, rebuild the now-V1 project and probe into
the same project-local paths, then create a new V1 snapshot. The sealer refuses
snapshot reuse and requires exact V1 source SHA-256
`b8a2cac2c5731407c7126ae2121d28cbceffed2e065cb18488e3379282feccb8`.

```powershell
dotnet build "$package/SchemaReload.fsproj" `
  --configuration Release --no-restore `
  -p:NuSource="$source" `
  -p:SourceRevisionId=064f7ae92a8506689cd91aff5e6804a375d6ef3d `
  *> "$artifact/build-v1-NEW.log"

python "$package/seal_build.py" v1 `
  "$artifact/build-snapshots/v1-build-NEW" `
  --archive $archive `
  --source-root $source `
  --probe $probe `
  --application $application `
  --gameplay-source $gameplay `
  --build-log "$artifact/build-v1-NEW.log"

$v1Receipt = "$artifact/build-snapshots/v1-build-NEW/receipt.json"
$v1ReceiptHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $v1Receipt).Hash.ToLowerInvariant()
$binding = "$checkpoint/checkpoint-binding.json"
$bindingHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $binding).Hash.ToLowerInvariant()

python "$package/run.py" fresh $probe $application $seed $checkpoint `
  "$artifact/runtime/fresh" `
  --gameplay-source $gameplay `
  --arm-receipt $v1Receipt `
  --arm-receipt-sha256 $v1ReceiptHash `
  --live-binding-receipt $binding `
  --live-binding-sha256 $bindingHash

python "$package/compare.py" `
  "$artifact/runtime/live/probe/trace.jsonl" `
  "$artifact/runtime/fresh/probe/trace.jsonl" `
  "$artifact/runtime/comparison-NEW"
```

The fresh runner accepts only the exact live binding receipt and checkpoint it
describes. The comparator checks exact mode schemas, identity-event counts and
order, zero held-input samples, the precomputed zero/200 oracle templates,
complete post-state and projection, and stable halt. Live mapping passes only
when reward 200 and all inherited fields/projection are both preserved.
Both arms launch through `dotnet --fx-version 10.0.10`; the retained
configuration event must report `.NET 10.0.10`, Windows, and X64.

Runtime deadlines are 900 seconds overall, 420 seconds to the live checkpoint,
and 3,600 postprocess callbacks. Handled exceptions and `KeyboardInterrupt`
trigger bounded full-process-tree cleanup and an atomic receipt. A failed
primary tree cleanup still attempts bounded direct root-process kill and wait,
but it retains unconfirmed descendant cleanup and forbids further native work.
An external termination that prevents the runner's `finally` block remains a
supervisor unknown. Five unresolved failures at an unchanged preparation, build,
objective-check, or runtime gate require return to the maintainer.

## Scope

The independent oracle covers gameplay state and time, paddle fields, ball
geometry/speed/position/direction, lives, score, reward, every remaining brick
key/geometry/color, entity projection, and zero sampled Left/Right-held input.
Its reset, altered-old-field, wrong-brick, wrong-score, and zero-versus-200
controls were frozen before reload. Fresh agreement cannot establish live
mapping correctness by itself. This package makes no claim about host-input
capture, audio, framebuffer restoration, application migration repair, a
general schema-migration mechanism, ordinary agent access, or benefit.
