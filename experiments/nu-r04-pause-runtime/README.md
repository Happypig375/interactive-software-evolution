# Nu R04 pause runtime feasibility

This package reproduces a bounded source-integrated comparison in pinned MMCC Breakout. It contains four reference arms—explicit and wildcard current baselines, then explicit and wildcard completed pause implementations—and five pause-explicit source faults. The reference observations passed, and every fault was detected at its prospectively named first gate. See the compact [result receipt](result-receipt.json) and the narrative [feasibility record](../../docs/nu-pause-runtime-feasibility-2026-10-15.md).

The [pre-execution contract](pre-execution-contract.md) fixes the fixtures, phases, expected outcomes, and limits. [fault-gates.md](fault-gates.md) fixes the five source-fault checks. [variant-manifest.md](variant-manifest.md) records the source correspondence, and [audio-instrumentation.patch](audio-instrumentation.patch) preserves the passive request observer. No candidate or model execution was involved.

## Reproduction

Preparation and full builds use fresh private source trees. Supply the verified archive rather than a mutable source checkout:

```powershell
python experiments/nu-r04-pause-runtime/prepare.py `
    .artifacts/r03-feasibility-20261015/nu-064f7ae.tar `
    experiments/nu-history-b1/checkpoint/gameplay.symbol `
    .artifacts/r04-pause-runtime-20261015/reproduction-preflight

python experiments/nu-r04-pause-runtime/build.py `
    .artifacts/r04-pause-runtime-20261015/reproduction-preflight
```

`prepare.py` verifies Nu commit `064f7ae92a8506689cd91aff5e6804a375d6ef3d`, archive SHA-256 `EB0AA77197DE1971D79AA0657C2AF5CF33B99BA8302A24BA44F3306CCA4BF92B`, and the fixed B0 symbol. It creates nine extractions, applies identical Gaia/audio instrumentation, emits exact fault patches, and records all modified-source hashes. `build.py` requires SDK 10.0.302, uses a task-private package cache, builds every complete application/probe graph, and records arm-specific binaries. Neither command launches Gaia.

After reviewing the new prepare/build receipts, run an arm once into a new directory:

```powershell
python experiments/nu-r04-pause-runtime/run.py `
    .artifacts/r04-pause-runtime-20261015/reproduction-preflight `
    pause-explicit `
    experiments/nu-history-b1/checkpoint/gameplay.symbol `
    .artifacts/r04-pause-runtime-20261015/reproduction-pause-explicit-01 `
    --timeout 600
```

The published experiment used the same tracked probe sources but avoided rebuilding unchanged accepted engines after a prospective setup amendment. Each amended probe was compiled against its frozen preflight-08 arm. The private launcher used `dotnet exec` with that arm's original `Probe.deps.json` and `Probe.runtimeconfig.json`, verified the external application hash and complete copied runtime manifest, and enforced exactly 600 seconds. The original host graph contains 44 libraries; the probe-only package added five `AmendedProbe` files. These performed wrapper/hosting differences and all loaded hashes are in [result-receipt.json](result-receipt.json).

## What was observed

The baseline explicit and wildcard arms passed active B0, lives-zero, empty-bricks, and Quit fixtures. Their 13 fixed B0 records were exact canonical JSON matches after excluding configuration and the independent generated initial clear.

Both pause references passed B0 reconstruction, Pause/Resume control projection, ten advancing TimeUpdate/Update pairs with frozen model and projection, one retained resumed pair, Quit reset, and fresh play. Their 22 fixed records through the resumed pair were exact canonical JSON matches. At the resumed Update, the probe sampled Left and Right as both up; it did not observe all possible input or replay state. Later vacant/fresh values use randomized initialization and were checked by frozen structural invariants.

The five source faults failed at `pause-reached`, `pause-projection`, `pause-frozen-model` after the first pair, `resume-retained`, and `quit-reset`, respectively. Probe exit 1 is the expected detection outcome for those controls; the engine exited 0 and none timed out.

An earlier direct B0 installation failed before pause: the diagnostic rerun exposed two same-key bricks with updated B0 colors but retained fresh positions. Pinned content reconciliation makes a generated-key collision a supported explanation, but the initial key set was not logged, so collision remains an inference. The final protocol first projects the already-existing initial model with state `Quit`, observes the halted empty-content boundary with zero Gameplay Update/TimeUpdate events, and then installs unchanged B0. This is explicit reconstruction alignment work. It does not establish a general live-replacement identity guarantee.

## Boundary

The trigger is synthetic publication of the real entity ClickEvents. It does not validate pointer hit testing, ButtonFacet Down/Up, physical click delivery, or click-sound behavior. The audio hook observes requests crossing the two World enqueue helpers; it does not observe native playback or direct initialization enqueue calls. The result is limited to this pin, application, functional accompanied Gaia mode, fixtures, and phase boundaries. It does not establish whole-Nu equivalence, ordinary agent access, diagnostic attention, maintenance benefit, or pause value.

Extracted sources, packages, objects, binaries, logs, and raw traces remain under ignored `.artifacts/`. The tracked package contains contracts, transformations, probe/driver source, and compact receipts only.
