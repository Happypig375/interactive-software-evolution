# R10 added-field reload: prospective contract

Frozen on 2026-10-16 before this package's source preparation, build or native
execution. This is independent of the stopped R02 input construction.

## Question and outcomes

Does adding a `BrickReward : int` field, initializing it to 200 in
`Gameplay.empty`, and using it for future hits install the intended value while
preserving an existing halted game? The existing behavior-only reload did not
change the model schema. The separate Prime conversion probe predicts that
successful conversion can instead supply zero. This prediction is not an
acceptance criterion: record the actual value.

Keep observation validity, the intended mapping, and continuation behavior
separate. A fully observed live conversion to zero is evidence of a failed
first-installation requirement, even if the probe exits successfully after
recording it. A fresh reference cannot make that live requirement pass.

The application mapping requirement is the October 11 live-edit contract:
retain all seven old fields and introduce reward 200 on first installation.
This gate examines the initializer-only route. It adds no migration override,
pre-conversion setter, post-reload repair or fallback modification. Retained
zero/75 across later reloads, repeated migration, arbitrary schemas and the
cost of an explicit migration remain later questions.

## Source and controlled edit

Use Nu commit `064f7ae92a8506689cd91aff5e6804a375d6ef3d`, extracted into a new
private directory from the exact archive with SHA-256
`eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b`.
The V0 `Projects/Breakout Mmcc/Gameplay.fs` is unmodified pinned source: seven
fields and the existing scoring literal 100. Reuse only the previously
published Gaia research bridge and postprocess observation instrumentation,
with exact source hashes. Do not alter the engine conversion route, FCS private
fields, dependencies, project parser or execution mode.

Build the V0 baseline and launch a functional, accompanied, halted Gaia world
using the Gameplay edit mode. Only after a durable checkpoint handshake:

1. append `BrickReward : int` after `Lives` in the Gameplay record;
2. add `BrickReward = 200` to `Gameplay.empty` (which `Gameplay.initial` uses);
3. replace `Map.count bricksIntersected * 100` with
   `Map.count bricksIntersected * gameplay.BrickReward`.

Preserve the exact before/after files and require each edit anchor exactly
once. No other application edit belongs to this arm. Invoke the existing
guarded `Gaia.tryReloadCode false` bridge and preserve its generated FSI script.
This bypasses the F9/menu input path.

## Fixed state and independent observations

Use the existing B0 seed at time 149, score 100, lives 5 and 29 bricks. Set only
the ball to position `(-64,53,0)`, size `(8,8,0)`, speed 3, direction `(0,1,0)`.
Brick `@455` has center `(-64,64,0)` and size `(64,16,0)`. Capture the complete
seven-field symbol, every represented field (including brick keys/colors),
selected scene projection, actual raw model/dispatcher types and assemblies,
and the explicit absence of `BrickReward` before source replacement.

After reload, use raw-object access and reflection. Never call the old static
Gameplay getter, setter, serializer or projection helper on the live model.
Require exactly one returned FSI Gameplay record with the exact eight-field
schema, actual reference identity of its type with the installed raw model,
matching dispatcher generic model type, and membership of both assemblies in
the returned FSI set. Record the actual field value; names or CodeReloadEvent
alone do not establish installation. The event also occurs after compilation
failure in this engine path.

Check the seven retained fields and selected projection independently of the
new field. Observe before advancing, with zero Update/TimeUpdate and zero
sampled Left/Right input. If retained state or projection differs, preserve the
observations, classify preservation as failed, and do not claim the prescribed
continuation was reached. No repair may make this assigned live attempt pass.

If preservation holds and the observed reward is in the bounded integer range
0 through 1000, continue once. The frozen event word is `TimeUpdate`, `Update`,
with `GameDelta.Updates = 1`. Geometry independently predicts one hit on
`@455`: stored ball position `(-64,56,0)`, collision next point `(-64,59,0)`,
direction `(0,-1,0)`, time 150, lives 5, and 28 bricks with only `@455` removed.
Expected score is `100 + observed reward`; the intended mapped result is 300.
Reward zero must still remove the brick and reverse the ball. Require the next
halted callback to have the identical complete model and projection and no
additional update. Out-of-range reward is retained as an unexpected result,
with continuation withheld rather than silently changing the bounds.

No audio request/playback instrumentation is added. The source's sound call is
not an observed effect; this gate cannot satisfy the separate effect obligation.
No framebuffer, native input replay, host-resource preservation, atomic rollback,
general schema guarantee, practical benefit or timing comparison is measured.

## Fresh required-state reference

After the live attempt, build V1 and start a fresh process. Record the actual
fresh selected model's reward before reseeding; the initialized value must be
200. Reconstruct all seven checkpoint fields and explicitly set the current
V1 field to 200. The reconstruction is a declared reference operation, not
evidence that old-state conversion supplied 200. Verify the complete retained
state/projection before advance and apply the same one-hit schedule and stable
halt check. Its expected score is 300.

Compare live and fresh seven-field pre-state and projection. Compare post-state
and projection, retaining any score/reward divergence. Only call them a matched
successful preservation pair if live mapping and both continuations actually
satisfy the requirement. Otherwise report the valid observation and specific
failed requirement separately. The fresh process is not a replacement attempt.

## Falsifiers and execution discipline

Before native launch, exercise in-memory oracle data controls for a reset
checkpoint, altered retained field, wrong brick removal, wrong score, and
reward zero versus the required 200. These are checker controls, not additional
runtime trials. The continuation oracle is derived from the frozen geometry,
not by calling application update code. Its data construction occurs before
live reload; after reload it only combines that frozen data with the observed
scalar reward. Checkers must not equate process exit zero with mapping success.

Use .NET SDK 10.0.302/runtime 10.0.10 and Windows x64, with recorded identities.
Use a 900-second process deadline, a 420-second checkpoint handshake deadline,
and 3600 postprocess callbacks. Preserve all preparation, build and runtime
attempts, source/configuration/assembly hashes, output and exception logs.
Outputs must be new paths. Do not overwrite the old R10 experiment or artifacts.

Keep a single build-attempt ledger for this package; changed compiler error
classes do not create a new gate. Five unresolved failures at that unchanged
gate require return before another preparation/build/run. Preserve scientific
failure rather than searching for a favorable replacement. Source, runner and
oracle review must be accepted before native launch. Later authored migration
work needs a separately frozen treatment and observations; it cannot revise
this initializer-only result.
