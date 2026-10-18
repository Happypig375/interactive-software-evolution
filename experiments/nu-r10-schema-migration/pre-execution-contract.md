# R10 explicit schema migration: prospective contract

Prepared 2026-10-16. Construction and native execution must wait for the recorded
protocol acceptance. Freeze these bytes and their hash before source preparation;
subsequent changes require a separate dated amendment. This is a new treatment,
not a repair or rerun of the [initializer-only observation](../nu-r10-schema-reload/README.md).
The stopped R02 input gate remains stopped.

## Question and assigned comparisons

Can an application-owned, pre-conversion schema witness plus a normal reload
message install a newly introduced reward while retaining deliberately configured
values? Does that behavior survive a repeat reload and a failed-compilation
notification? This is bounded mechanism feasibility and construction accounting,
not automatic migration, atomicity, developer productivity or comparative benefit.

Assign six native processes, in this order: M0-live, M1-live, M2-live, M0-fresh,
M1-fresh, M2-fresh. Each live process performs two successful-source reload
attempts, one intentionally invalid-source reload attempt, and at most one
gameplay step followed by an explicit new-round diagnostic. The fresh processes
are required-state references; they never replace an unsuccessful live delivery.
Do not add favorable replacement trials. Retain all attempts and withheld phases.

| Case | Actual incoming schema/value | Required first value | One-hit score |
| --- | --- | --- | --- |
| M0 | Seven original fields; reward absent | 200 | 300 |
| M1 | Eight fields; reward deliberately set to 0 | 0 | 100 |
| M2 | Eight fields; reward deliberately set to 75 | 75 | 175 |

The original seven-field checkpoint and projection are the same in all cases.
M1/M2 are deliberately constructed predecessor configurations, not naturally
sampled histories. Their predecessor source is exactly the earlier three-edit
initializer-only V1 (field, default 200, scoring use), without migration code.
M0 uses pristine V0. Each repeat starts from that process's actual first-reload
result, without reseeding, rescue, a typed old-model read, or a reward repair.
Preserving a wrong first result on repeat cannot erase its failed delivery.

## Pinned source and application treatment

Use Nu `064f7ae92a8506689cd91aff5e6804a375d6ef3d`, a new private extraction of the
998,277,120-byte archive with SHA-256
`eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b`.
Reuse the accepted Gaia bridge and postprocess observer unchanged (instrumented
Gaia SHA-256 `0700ba1472a9751356ffb2d54061cd269bc4d4488e5c673858187112d2196490`).
Retain the unchanged Breakout parent declaration with empty Gameplay property
definitions. Do not modify engine conversion, fallback, FCS private fields,
project parsing, dependencies, execution mode or the old experiment package.

The target includes the same added field/default/scoring changes and this
application-owned composition, through public Nu APIs:

1. Define one uniquely named non-persistent screen Xtension integer property,
   `BrickRewardMigrationWitness`, default 0. Encoding: 0 = no pending witness,
   1 = captured old schema with reward absent, 2 = captured schema with reward
   present. Keep it outside MMCC content/Definitions property writes.
2. In the replacement `GameplayDispatcher.TrySynchronize` override, only for
   `reinitializing=true` and marker 0, read the raw `Model` property before the
   base call. Require a non-null F# record with the exact ordered seven-field
   or eight-field schema; the present reward must be `System.Int32`. Reject an
   unknown schema, missing property or incompatible marker. Store 1 or 2 through
   the ordinary scalar property setter. If a valid pending marker already
   exists, retain that first observation; never derive absence from reward zero.
3. Delegate normally to base synchronization. The expected first M0 conversion
   supplies an intermediate reward zero and reconciles content before mapping.
   A later `false,false` synchronization must not recapture the witness.
4. Declare `Game.Handle.CodeReloadEvent =|>` in the new dispatcher's Definitions,
   returning a new gameplay message. In that message, check the scalar marker.
   For marker 1 or 2, clear it to 0 before returning any model result. Marker 1
   returns the new-typed model with reward 200; marker 2 returns it unchanged.
   Marker 0 returns it unchanged. Invalid/missing state is an explicit failure.
   Use the normal MMCC message/model write; the driver must not perform mapping.

Read the marker with raw `TryGetProperty` and verify its type/value before use;
do not let a typed getter silently promote an incompatible value or lazily create
a missing slot. Check setter success and read back the exact value. The marker
is an immutable scalar in ordinary World state, not an external dictionary.

Unknown raw schema, a null model, missing/incompatible marker, failed setter or
failed readback throws `InvalidOperationException` with a specific migration
rejection reason, before any subsequent application step. Instrumentation emits
that rejection before the throw. Gaia's catch restores its saved World and can
skip the normal reload notification; record the actual returned raw state,
projection, marker, identities, exception/log evidence and event counts. Do not
assume that restoring this World makes all mutations atomic. A fully observed
rejection is an adverse treatment result; withhold its later dependent reloads,
step and reset. An observer exception is a separate validity failure.

Clearing before the model result deliberately prevents stale authorization
after consumption. An exception between clearing and committing the model can
lose pending migration; retain that failure and stop that process. This treatment
does not implement retry, rollback, nested/concurrent reload, arbitrary parent
callbacks, multiple screens, history branching or an atomic transaction.

## Observation and fixed sequence

Use functional, accompanied, halted Gaia in the Gameplay edit mode. Before
reload, bind the existing seed (SHA-256
`ffee72d91c6e4a32b650d45e9addd9e02e179163d0c8bbaaa8cddb9c92bc783a`): time 149,
score 100, lives 5, 29 bricks. Set only the ball to position (-64,53,0), size
(8,8,0), speed 3 and direction (0,1,0). M1/M2 additionally set the declared
incoming reward during initial reconstruction, before the durable checkpoint.
Verify every old field, brick key/geometry/color and the complete existing
selected projection against the independent oracle before editing source.

Retain an uninstrumented target-source derivation and an executed derivation
whose only additional application edits emit observation events. The observer
records raw state without a typed old-model getter and never writes the witness
or live reward. Observation events may record entry/exit and decision points;
their event/IO overhead is part of instrumentation, not production cost evidence.
Record complete raw model/schema and selected projection at these boundaries:

- pre-capture and post-capture, before base synchronization;
- after base synchronization, before reload-handler mapping;
- handler entry, after marker consumption, and mapping/retention decision;
- model-change notification after the ordinary write, when one occurs;
- after each reload call and at the next halted callback.

Record the screen state identity, dispatcher/model types and assemblies, marker,
Update/TimeUpdate counters, held Left/Right samples and actual observation order.
At every handler/message entry retain the actual message object/type identity,
not merely a phase label or type-name string. The exact parent predicts one
reinitializing capture and one reload-message invocation per successful reload.
Fully observed extra/missed capture, wrong order, stale marker, duplicate/missing
handler, wrong mapping/retention or unwanted reset are evaluable mechanism
failures. Missing/corrupt trace values, observer exceptions, unbound source or
assembly identity, corrupt checkpoints, deadline and cleanup failures instead
limit observation validity. Preserve these classes separately, including partial
evidence; never relabel a completely observed adverse transition as missingness.
Do not infer atomicity from equal endpoints.
Intermediate content and ModelChange observations cover this selected projection
only; audio, framebuffer, external-resource effects and transient external
observers remain unmeasured.

For each live process:

1. At the durable halted checkpoint, replace predecessor source with the exact
   target and invoke the guarded ordinary reload core. This bypasses F9/menu.
   Bind the exact source and generated script. Require runtime-reference
   membership in that call's returned FSI DynamicAssemblies for the installed
   dispatcher, raw Model property type and raw value type, dispatcher model
   argument, and actual reload message at its one handler entry. The three model
   types must be the same returned Gameplay type. Retain assembly MVIDs and
   runtime-reference comparison results; names alone cannot establish membership.
   Verify
   the original seven fields/projection and the case-specific required reward
   separately. Require marker 0 after consumption.
2. At the next halted callback, reload the identical valid target bytes again.
   Bind the actual inherited state/type as the repeat input. Require a new FSI
   installation with a different assembly object and MVID from the first,
   captured-present witness, unchanged complete state/projection,
   no second first-installation mapping and marker 0. A first-mapping failure
   remains failed even if repeat retention succeeds.
3. At the next halted callback, replace target source with a fixed intentionally
   invalid F# version (preserve its bytes/hash) and invoke the same reload core.
   Preserve the actual compiler error and generated script. Require one reload
   notification and exactly one invocation of the installed reload message. Bind
   its actual message/dispatcher/model types to the second successful FSI
   installation, using runtime-reference identity. Require the marker-0 no-op
   branch, no reinitializing capture, no new installed model/dispatcher type, no
   marker write/clear, no mapping assignment, no model-change notification and
   unchanged complete state/projection. An absent handler cannot pass this
   control merely because endpoints match.
   Restore the valid source bytes afterward without another reload or model
   change. This is an assigned negative control, not a construction failure or
   successful code installation.
4. If all seven old fields/projection remain preserved, phase observations are
   valid and the actual reward is an integer in [0,1000], advance once with
   `TimeUpdate`, `Update`, delta 1. Preserve an unexpected in-range reward and
   evaluate its continuation separately; do not repair it to the required value.
   A fully observed mechanism failure remains failed but may supply the actual
   next input when these prerequisites hold. Observation invalidity, state drift,
   an explicit application rejection or an out-of-range value withholds dependent
   phases. Preserve the reason and all earlier observations.
5. Require stable complete state/projection at the next halted callback. Then
   publish the ordinary selected screen's SelectEvent once as an explicitly
   synthetic application StartPlaying/new-round diagnostic. Require exactly one
   published SelectEvent, one StartPlaying message entry and one reset decision,
   with actual message/dispatcher types bound to the current installed assembly
   (second FSI installation for live; built target for fresh). Require reward 200,
   Playing, time/score 0, lives 5, 30 bricks and default paddle/ball position,
   size and speed. Ball direction, generated brick names and colors are random;
   preserve them but do not invent equality across processes. Check every final
   model-to-projection key, geometry, color and required entity/text value, with
   no prior brick/entity remnants, and stable next halt. Counts alone do not
   establish correspondence. This checks the
   authored reset handler, not UI selection/input delivery or retained progress.

Each fresh process uses the built target source. Observe actual selected fresh
reward 200 before reconstruction, then explicitly reconstruct the matching
live checkpoint's seven fields plus required reward 200/0/75. Bind the exact
checkpoint receipt, verify full state/projection and marker 0, and apply the same
one-step, stable halt and synthetic new-round diagnostics. It performs no reload.
Fresh references remain separately interpretable if live mapping fails. A missing
or invalid live checkpoint withholds its dependent fresh reference.

## Independent oracle and falsifiers

Reuse the previously frozen complete checkpoint and geometric continuation
oracle, with explicit pre-run 0/75/200 cases. Create a separate oracle file before
construction: copy the exact old checkpoint and zero/200 templates, derive the
75 case only by the declared score/scoreText arithmetic, and record explicit
reset constants plus model-to-projection relations for the random fields. Bind
its hash independently of the implementation. The stored ball position after the
step is (-64,56,0), collision point (-64,59,0), direction (0,-1,0), time 150,
lives 5, and 28 bricks with only @455 removed. Score is 100 plus the actual
retained reward. Predict state/projection without calling application update
code. Compare each pair's pre-state, post-state and stable halt; no aggregate
pass may conceal a failed first mapping, repeat, failure control or reset.

Before native execution, objective controls must reject: wrong old field/reset,
wrong brick removal, wrong score, absence confused with deliberate zero,
overwritten 75, repeat reseeding, stale witness, missed/extra capture, false
installation on failed compilation and reward 0 where first installation needs
200. Also reject a failed-compile notification with no marker-0 handler entry,
duplicate/stale StartPlaying delivery, and a reset projection whose counts match
but whose actual keys/geometry/colors do not. Check raw trace values/order rather
than trusting probe self-reported flags. Controls must distinguish an evaluable
mechanism failure from invalid or missing observation.
Pure controls are checker validation, not native trials or evidence of benefit.

## Execution, provenance and work accounting

Use SDK 10.0.302, runtime 10.0.10, Windows x64, static 60-update clock, zero
sampled Left/Right input, 900-second overall process limit, 420-second initial
checkpoint limit and 3,600 postprocess callbacks. Preserve all source versions,
generated scripts, compiler diagnostics, exceptions, source/output manifests and
build/runtime attempts at new paths. Retain the exact toolchain and all four
output roots through independent copied snapshots, with no hardlinks. Check
project-local dependency bytes immediately around each reload where feasible;
do not invent observed resolution or native-library provenance.

Review and accept source, driver, independent oracle and build receipts before
native launch. Use bounded full-process-tree cleanup; an unconfirmed cleanup
prohibits further native work. At five unresolved failures of one unchanged
preparation/build/check/runtime gate, return before another attempt; changing
error classes does not reset the gate. The deliberately invalid compilation
control is labeled separately and cannot excuse an unresolved construction error.

Record functional mapping/storage/subscription code, observation code, driver,
oracle, review, reconstruction and integration work separately, including failed
attempts and reused components. Elapsed wall time includes setup and observation;
FSI and fresh compilation modes differ. Neither line counts nor this single AI
maintainer construction estimates human or agent productivity. Retain narrow
positive, null and adverse observations without promoting feasibility to benefit.
