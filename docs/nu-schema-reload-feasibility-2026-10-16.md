# R10: adding a model field during live reload

**The live arm preserved the old state but failed the required new-field mapping.**
It observed reward zero despite the new initializer of 200. The fresh process
observed initial reward 200 and its required-state reconstruction passed. This extends the
[unchanged-schema reload](nu-live-reload-feasibility-2026-10-15.md) with a
different, prospectively specified question. It does not replace that result
or establish maintenance benefit.

## Question and fixed comparison

The existing halted functional Gaia/MMCC Breakout game has seven represented
model fields. The application edit adds `BrickReward : int`, initializes it to
200 in `Gameplay.empty`, and uses it in subsequent brick scoring. The intended
mapping retains all seven old fields and introduces reward 200. The isolated
[Prime conversion probe](nu-conversion-feasibility-2026-10-15.md) predicts that
successful conversion may instead supply zero; that prediction is not treated
as an observation of this application.

The live arm uses the ordinary initializer-only edit. It has no migration
override, pre-conversion setter, post-reload repair or modified fallback. The
fresh reference starts the edited application, observes its initial reward,
then reconstructs the same seven checkpoint fields with an explicit reward
200. That reconstruction is a declared reference operation. It cannot establish
that live conversion supplied 200 or rescue a failed live mapping.

The [frozen contract](../experiments/nu-r10-schema-reload/pre-execution-contract.md)
and [pre-execution clarification](../experiments/nu-r10-schema-reload/protocol-amendment-01.md)
fix the application treatment, independent model/projection observations,
continuation, failure rules and process bounds. Both precede source preparation
and native execution. The clarification followed protocol review and preceded
the first preparation attempt. The
[source-boundary audit](nu-live-edit-contract-2026-10-11.md#2026-10-16-source-boundary-for-an-explicit-migration)
explains why successful conversion and an application fallback are distinct;
its proposed explicit migration composition is not implemented in this arm.

## State and observation boundary

The source pin is Nu `064f7ae92a8506689cd91aff5e6804a375d6ef3d`. The V0
application source is unchanged. Only the previously used Gaia reload bridge
and postprocess observation seams are instrumented. Separate immutable build
snapshots preserve the binaries and source identities used for each arm while
launches retain Gaia's required project paths.

The fixed checkpoint has gameplay time 149, score 100, lives 5 and 29 bricks.
Only the ball is placed at `(-64,53,0)`, with size `(8,8,0)`, speed 3 and direction
`(0,1,0)`. Independent geometry predicts that one `TimeUpdate, Update` pair with
delta 1 removes only brick `@455`, stores the ball at `(-64,56,0)`, reverses its
vertical direction, advances time to 150, and preserves every other represented
value. The expected score is `100 + observed reward`: 100 for reward zero and
300 for the required reward 200. The complete model and selected scene
projection must remain stable at the next halted observation.

The parent independently reconstructed the checkpoint and both reward-specific
post-models in the frozen
[oracle](../experiments/nu-r10-schema-reload/oracle.json). The probe's complete
expected model/projection data are prepared before reload. After reload, raw
object access and reflection observe the installed FSI model and dispatcher;
the old static model getter, setter and typed projection helper are excluded
from that observation path. Exact type identity and returned-assembly membership
are required. A reload notification alone is insufficient.

Observation validity, old-state preservation, required reward installation and
continuation are separate outcomes. Mapping success requires both preservation
and reward 200. A valid observation of zero is a failed application requirement,
even when its observed continuation correctly uses zero and the process exits
successfully. Fresh/live equality is secondary to the independent oracle; two
identically wrong arms cannot pass by agreeing.

## Observations and construction accounting

The first assigned live process completed without timeout. Its actual model and
dispatcher were `FSI_0005.Breakout.Gameplay` and
`FSI_0005.Breakout.GameplayDispatcher`, belonging to the assembly returned by
reload (MVID `6ad11aae-3b31-4c1a-a745-0383ae1ad16a`). Reflection observed all eight
fields and `BrickReward = 0`. The seven inherited fields and complete declared
projection were preserved. One prescribed update removed `@455`, reversed the
ball, advanced time to 150 and retained score 100. The next halted observation
was stable. This is a valid failed mapping, not an engineering failure to retry.

The independent trace validator accepted observation validity, preservation and
the reward-zero continuation, while rejecting required-reward installation and
mapping success. It recomputes these verdicts from complete observations rather
than trusting the probe's result flags or exit code. The fresh reference observed
initial reward 200 before reconstruction, then reproduced the old seven-field
checkpoint with explicit reward 200. Its prescribed hit reached score 300, with
the same removal, motion, time and stable-halt obligations satisfied. The fresh
reference did not repair the completed live arm.

| Observation | Live initializer-only reload | Fresh required-state reference |
| --- | --- | --- |
| Valid observation process | Passed | Passed |
| Old seven fields and selected checkpoint projection | Preserved | Matched |
| Reward before the hit | 0 | 200; initial value also observed before reconstruction |
| Score after the hit | 100 | 300 |
| Full reward-specific continuation oracle and stable halt | Passed | Passed |
| Required live mapping | Failed | Not a live-conversion test |

The two post-models/projections differ, so this is **not** a matched successful
preservation pair. Complete selected [observations](../experiments/nu-r10-schema-reload/observations.json)
are published with the [result receipt](../experiments/nu-r10-schema-reload/result-receipt.json)
and [reproduction instructions](../experiments/nu-r10-schema-reload/README.md).
Both assigned native attempts are reported; neither was replaced or rerun.
Both processes exited zero without timeout or required cleanup. Their recorded
121.313 and 154.469 seconds include prelaunch file checks and are attempt
bookkeeping, not a performance comparison.

The
[attempt ledger](../experiments/nu-r10-schema-reload/attempt-ledger.json)
retains the construction outcomes and native assignments:

| Gate | Retained outcomes |
| --- | --- |
| Source preparation | Attempt 01 failed with `MemoryError` while hashing the archive before destination creation; streamed hashing allowed attempt 02 to pass. |
| Compilation | Build 01 ended interrupted with unknown completion. Build 02 passed with 334 warnings and zero errors. Corrected probe-only builds 03 and 04 passed with 122 warnings and zero errors each. The subsequent V1 reference build passed with 212 warnings and zero errors. Different incremental scopes do not establish a warning reduction. |
| Objective checks | Fifteen invocations: twelve passed and three failed. One caller invocation split a spaced path; two later fixture failures exposed missing or incorrectly coupled reward-range flags. Final invocation 15 passed 29 checks, including valid failed-mapping observations, contradictory/shared-wrong-result rejection, exact source/seed/oracle bytes, complete build verification, runtime/OS/architecture mismatches, and bounded cleanup including a failed primary cleanup command. |
| Build preservation | Four V0 snapshot attempts and one V1 snapshot passed; superseded copies and the original build 02 outputs remain preserved. The final V0 receipt binds 1,145 independent copies and the V1 receipt 1,148, including all files in four output roots and the exact archive-derived 3,240-file source manifest. No hardlinks substitute for copies. |
| Independent source review | Review 01 found four blockers in seed/oracle binding, build lineage, cleanup and evidence-derived classification. Review 02 found remaining gaps in full reload/content inputs, cleanup fallback and actual runtime enforcement. Review 03 accepted the corrections before native execution. These are two failed review gates followed by a passing review, not seven runtime attempts or human approval. |
| Native observations | live-01 validly failed the required new-field mapping while preserving old state; fresh-01 passed its distinct initialization/reconstruction/continuation contract. Paired validation accepted both observations and rejected matched successful preservation. |

Construction/checker outcomes are distinct from application trials and
independent replications. Parent acceptance and the runner each check the
accepted complete source/build receipt before launch. Successful later checks
do not erase earlier failures or interrupted attempts. The final handoff has a
clerical reference to objective check 14 in one verification sentence; its
explicit check-15 receipt, hash and final snapshot identify the accepted inputs.

The generated reload script has eight local assembly references. Seven exact
paths have retained prelaunch identity coverage. `Nu.Spine.dll` has a narrower
provenance limit: four presealed copies and its explicitly post-live/pre-V1-build
project-local capture are byte-identical, but that exact local path was not
hashed immediately before/during reload and its resolved FSI load was not
observed. There is no mismatch evidence. Retain this timing limit without
claiming either complete loaded-dependency attestation or a different binary.

## Interpretation limits and next action

The selected observation covers represented gameplay and a declared scene
projection. It does not observe audio requests or playback, native input replay,
framebuffer equivalence, external-resource preservation, atomic rollback,
ordinary agent access, repair effort or comparative benefit. The Gaia bridge
bypasses the F9/menu invocation path. Retained zero/75 across later reloads,
repeated migration, explicit mapping work and other schemas remain separate
questions.

The FSI reload uses Gaia's pinned debug/nonoptimized settings, whereas the fresh
reference uses a prebuilt Release application. This is not a controlled
compile-mode or timing comparison. The authored 200-point requirement provides
a falsifiable application correspondence; it does not establish population-level
task importance.

The next consequential R10 construction would separately freeze an explicit
application migration, preserving absence versus legitimate zero and nondefault
values across repeated reloads. The source-bound witness/setter composition has
ordering and intermediate-content obligations, so its correctness and total work
must be observed rather than inferred from this result. Avoid repeating another
initializer-only variation as evidence of practical benefit. R03 same-code
recovery, native effects and ordinary agent access retain their separate limits.
