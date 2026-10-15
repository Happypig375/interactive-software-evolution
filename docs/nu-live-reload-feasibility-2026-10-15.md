# Bounded Gaia behavior-only live-reload feasibility — 2026-10-15

## Result

A prospectively specified Windows x64 construction passed the bounded first R10
gate at Nu commit `064f7ae92a8506689cd91aff5e6804a375d6ef3d`. From a halted functional MMCC
Breakout checkpoint, the ordinary Gaia `tryReloadCode false` core compiled and
installed a one-literal reward edit. The complete model and declared gameplay
projection were bit-for-bit unchanged before advance. The next single update
awarded 200 for the declared brick, producing score 300 rather than the old-rule
counterfactual 200. A fresh reward-200 reconstruction from the same serialized
checkpoint produced the same complete post-update model and projection.

This is a bounded feasibility result for one behavior-only edit and one
unchanged seven-field `Gameplay` schema. It does not establish empirical
benefit, a general insertion point, renamed-type conversion, or preservation of
observed audio, framebuffer, native-host state, or the F9/menu invocation path.
Those effects remain pending.

## Prospective gate and implementation

The [pre-execution contract](../experiments/nu-r10-live-reload/pre-execution-contract.md)
was saved before source preparation or execution (SHA-256
`558178ac939e8045bdb56c44c1567100515becfa497931c10bb52cee09e7c55b`).
It fixed the checkpoint, edit, expected and falsifying outcomes, event schedule,
identity requirements, negative data controls, matched fresh arm, watchdog, and
five-failure stop rule.

The published contract removes one trailing empty line to satisfy repository
whitespace checks. Its rules are unchanged. The exact frozen bytes are retained
privately; the result receipt distinguishes their original hash above from the
published copy's hash.

[`prepare.py`](../experiments/nu-r10-live-reload/prepare.py) archived and
extracted the exact pin, checked unique source anchors, and made four narrow
research changes:

1. capture Gaia's exact generated FSI script;
2. expose one guarded bridge that checks functional halted mode, reload
   permission, and the expected FCS private-field seams before calling the
   ordinary `tryReloadCode false` core;
3. invoke the research observer after Gaia's ordinary postprocess callback; and
4. add `Gameplay.BrickReward = 100` and route the existing scoring expression
   through it, without changing the model schema.

The executed preparer recorded the archive SHA-256 as
`eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b`.
The publication preparer additionally rejects any archive whose hash differs
before extraction. This guard was added after the accepted execution; the
private evidence retains the executed preparer and its SHA-256. A tiny incorrect
tar archive was rejected with exit code 1 before a source directory was made.
Original pinned hashes were
`0cf653d4988ceefffd45935b37d0dcbcfb72c44bfd9ed47b3eb5ebd8ebc3b22e`
for `Nu/Nu.Gaia/Gaia.fs` and
`571e2a5ce3f0630972f2fbe4e9a6a3c376bcf4d1a74589d14c882b2ee0db1423`
for `Projects/Breakout Mmcc/Gameplay.fs`. The runner changed exactly one
`static member BrickReward = 100` occurrence to `200` only after the old
checkpoint receipt was durable; the before and after source hashes were
`736132f1b5a43edb663a5ebfcf8624b6de921c9532ad7a315b30fa11fb370481`
and `86b6d9987e73fa59c5d7483e2ad9b604513eb7e7c73859c0e7a43abbebf29dbc`.

[`LiveReload.fs`](../experiments/nu-r10-live-reload/LiveReload.fs) used the old
typed model only to seed the pre-reload checkpoint. Every post-reload model read
used `GetModelGeneric<obj>` plus reflection and symbol serialization. It selected
exactly one returned FSI record with `Type.Name = Gameplay`, the exact seven
field names, and public static reward 200. It required `Object.ReferenceEquals`
between that `Type` and the raw model's actual type. The dispatcher base's
generic model argument used actual `RuntimeType` equality (`modelType = Some
actualType`). Model and dispatcher assembly membership each used
`Object.ReferenceEquals` against the returned FSI assembly set. Therefore the
result does not rely on name-only matching or on `CodeReloadEvent` as a success
witness.

Parent review independently checked all 3,240 files in the preserved source
archive against the executed extraction. Only `Gaia.fs` and `Gameplay.fs`
differed, with the recorded instrumented and reward-200 hashes. It reconstructed
the expected complete checkpoint from the published B0 symbol using a separate
parser, applied only the declared ball change, and checked the complete expected
post-state against both saved traces. Trace hashes, generated script, execution
mode, halted boundaries and successful process exits matched the receipt.
This was saved-evidence verification, not a new runtime or human review.

## Observed identities and behavior

The process loaded .NET runtime 10.0.10, `Prime, Version=11.5.1.0` with SHA-256
`61a67158910296d92e22cf4c4d7ec9edb194c55ab00098534850e281e370c787`,
and `FSharp.Compiler.Service, Version=43.12.204.0` with SHA-256
`c022989f50845e07928652aae15b1116b87ac27ede1407a46ea77c6376e875bc`.
The exact generated script had SHA-256
`e5132fd638dbd1a53adaccfeb9744e32a7051a10ece580ebef2fcf0e3963b5da`.
The valid generated prefix was observed rather than prescribed:

- raw model: `FSI_0005.Breakout.Gameplay`;
- installed dispatcher: `FSI_0005.Breakout.GameplayDispatcher`;
- dispatcher generic model argument: `FSI_0005.Breakout.Gameplay`;
- returned assembly: `FSI-ASSEMBLY-MULTI, Version=0.0.0.32762`, MVID
  `6ad09199-e181-34de-a745-03839991d06a`.

The halted checkpoint contained time 149, score 100, five lives, 29 bricks, and
ball position `(-64,53,0)` with positive Y direction. At each gameplay `Update`,
the probe sampled `World.isKeyboardKeyDown` for Left and Right; neither key was
held on any sampled update. Native input event publication, capture, and replay
were not observed. Before advance, live reload preserved the complete model and
declared projection hashes. Exactly one `GameDelta.Updates = 1` schedule
observed the event word `TimeUpdate → Update`. The next halted state contained
time 150,
score 300, five lives, 28 bricks, no `@455`, ball position `(-64,56,0)`, and
negative Y direction. A following observation was stable.

[`compare.py`](../experiments/nu-r10-live-reload/compare.py) required equality of
the full checkpoint live/fresh models and projections, equality of the full
post-update and next-halted live/fresh models and projections, the recorded type
names and reward, zero sampled Left/Right-held updates, the event word, and the declared
scalar consequences. It passed. The compact [result receipt](../experiments/nu-r10-live-reload/result-receipt.json)
contains all hashes and observed identities; the runtime identity guards above
are enforced inside the probe. The separately executed intentional
score-100, reset, and missing-`@455` data controls were each rejected by the
oracle; they were not runtime failure trials.

## Attempts and interpretation limits

All attempts were retained under the private
`.artifacts/r10-live-reload-20261015/` tree. Three initial harness builds failed
with eight, four, and two F# errors respectively before the first successful
build. Two fresh-arm runtime attempts then failed while decoding an incorrectly
wrapped symbol; an isolated actual-Prime check showed that `scstring` on the raw
record already returns the directly decodable record symbol. Correcting only
the harness serialization produced a passing pair. A final trace-only event
schedule receipt changed the probe hash, so the accepted pair was rerun from a
fresh checkpoint and new attempt directories. Both accepted processes exited
zero: live in 24.907 seconds and fresh in 28.031 seconds. These wall times are
attempt records, not comparative cost estimates.

The build used SDK 10.0.302 and completed with 334 dependency warnings
and zero errors in each accepted build. The warnings were pinned package
advisories and an FCS/FSharp.Core version-constraint warning; neither package,
compiler source, private field, or path parser was changed to obtain the result.
Gaia's pinned FSI session explicitly used `--define:DEBUG`, `--optimize-`, and
`--tailcalls-`. The matched fresh arm used the prebuilt Release application
assembly; it was ahead-of-reload compiled, not a NativeAOT publication. The
selected reward expression is outside conditional-compilation directives, but
this construction does not isolate compile mode and supports no compile-mode or
cost inference.
The portable [reproduction instructions](../experiments/nu-r10-live-reload/README.md)
retain the real extracted project-local `bin/Release/net10.0` layout required by
Gaia's `TargetDir/../../..` project discovery. They deliberately exclude the
large Nu archive, extracted source, binaries, caches, and private traces.

Successful reload here shows that this source-bound case can preserve the
declared model/projection state and install the new reward behavior. It does not
show that every successful Prime conversion preserves intended state, that
renamed schemas work, that a fallback/reset is preservation, or that live reload
improves total work. Those remain separate R10 questions.
