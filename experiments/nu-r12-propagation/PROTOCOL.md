# R12 public entity propagation: first stub-world exercise

Frozen comparison and oracle, 2026-10-18, before construction or execution.
The parent accepts the source route in the private
`.artifacts/r12-propagation-20261018/source-feasibility.md`; this protocol owns
the narrower first execution. The user has authorized confident local
construction and experiments. R02 input and R10 migration remain stopped.

## Question and boundary

Does the public `World.propagateEntityStructure` operation apply the declared
source/target revision rules to real serialized entity trees in the pinned
Nu implementation? Compare the observed target before and after one declared
source revision with the explicit value/name obligations below. This is a
mechanism check, not an alternative-engine, authoring-effort, or benefit
comparison. There are no task-solving candidates or human participants.

Use Nu `064f7ae92a8506689cd91aff5e6804a375d6ef3d`, .NET SDK 10.0.302, and
an isolated console host. Call `Nu.init`, then `World.makeStub` with an empty
plugin, functional execution (`Imperative=false`), `Accompanied=true`, and
`Advancing=false`. Use real default dispatchers and intrinsic overlays.
Create one screen and group through public APIs. Clean up the world in a
`finally` block. Do not run a game loop or initialize a window, control input,
load Gaia, invoke private methods, or copy the reconciliation algorithm.
Nu's serialization traversals can poll SDL; a stub world does not prove the
absence of all native library calls. Any initialization/polling failure is
retained as a feasibility failure, not worked around with a copied algorithm.

The core source and public signature were checked against the original
archive, SHA-256
`eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b`.
Reuse the accepted R03 `Nu.dll` only if its loaded SHA-256 is
`e96cd61d188c689f7e39e2670b4d8582e26b9ea2dc95e1a15056891b7c99cd68`.
Identify the actual host, managed/native dependencies, probe source/project,
build command, output and loaded assembly hashes. A different local binary
requires an explicit provenance amendment before execution. Do not build or
modify the shared Nu tree. Parent acceptance of the host and compiled probe
precedes the runtime attempt.

## Fixed fixture and operations

Create `Game/R12/Scene/Source` as a persistent, unprotected
`ButtonDispatcher` with `Text = "Family v0"`. Create four named persistent,
unprotected `TextDispatcher` children, mounted to their parent:

| Name | Initial text |
| --- | --- |
| Shared | Shared v0 |
| EqualValue | Equal v0 |
| LocalDeleted | Local v0 |
| SourceDeleted | Deleted v0 |

Use nonempty text to avoid an accidental missing/default property test.
Duplicate the source using `World.writeEntity false false` and
`World.readEntity false false` with name `Target`. Link the target with
`target.SetPropagationSourceOpt (Some source)` **before** any revision.
Nu must create the saved source descriptor through this ordinary setter;
the probe must not assign it. Check the initial source/target text, exact
child names, persistence/protection, link, and saved descriptor presence.
An invalid bootstrap is not an adverse propagation result.

Perform these operations in the specified order:

1. On Target, change root text to `Target override`; change
   `EqualValue.Text` to `Temporary`, then back to `Equal v0`; change
   `SourceDeleted.Text` to `Local edited deletion`; immediately destroy
   `LocalDeleted`; create `TargetOnly` with text `Target only`.
2. On Source, change root text to `Family v1`, `Shared.Text` to `Shared v1`,
   and `EqualValue.Text` to `Equal v1`; immediately destroy `SourceDeleted`;
   create `Added` with text `Added v1`.
3. Record both actual trees and the saved previous source descriptor. Require
   the old descriptor still to describe the v0 tree. Record the target root
   ID as descriptive evidence, not an identity-preservation requirement.
4. Call `World.propagateEntityStructure source world` exactly once.
5. Observe both actual trees using public getters and Nu-written descriptors.
   Inspect the complete direct-child name set and values, the saved source
   descriptor, propagation link, and target root ID.

Do not re-create a missing target or manually apply the expected values after
the call. The `Entity` handle denotes an address; reusing it does not prove
the old runtime entity survived. The public operation itself destroys and
recreates targets.

## Declared observations and falsifiers

The target after the single call must have root text `Target override` and
exactly these children:

| Name | Required text | Rule under examination |
| --- | --- | --- |
| Shared | Shared v1 | Value matching the prior source follows the revision. |
| EqualValue | Equal v1 | Returning to the prior value does not encode pinned intent. |
| Added | Added v1 | A new source child is introduced. |
| TargetOnly | Target only | A target-only child survives. |

`LocalDeleted` must remain absent even though it remains on Source.
`SourceDeleted` must be absent despite the target's local text change.
The target must remain linked to Source. Source must retain its own v1
values and exact children `Shared`, `EqualValue`, `LocalDeleted`, `Added`.
Its saved descriptor must advance to that current tree after the call;
compare the pertinent dispatcher/name/text/child structure, excluding the
recursive saved-descriptor property itself. Preserve complete emitted
descriptors for inspection rather than silently discarding other fields.

A missing trigger, wrong bootstrap, loaded-assembly mismatch, missing output,
exception, cleanup failure, or deadline failure is an invalid/incomplete
exercise with its exact phase recorded. A completed call from the valid
declared precondition whose target violates an obligation is a valid adverse
mechanism result. Preserve all actual post-call observations even when one
obligation fails. Do not change the fixture to obtain a favorable result.

Use a 120-second process deadline for this small stub-world exercise. One
initial runtime attempt is assigned after source/build acceptance. A later
diagnostic or correction must be separately labeled and retain the original
attempt. Keep every construction/build attempt; five unresolved failures at
one unchanged gate trigger return. Build/source corrections must not change
the scientific fixture without a prospective amendment.

## Scope and next decision

This can establish only the executed descriptor/property policy for one
button/text family. It does not measure button rendering/input, Gaia menu or
undo access, authoring cost, save/reopen history, native resource lifetime,
causal diagnosis, agent access, designer productivity, or comparative benefit.
Root ID observations cannot establish preservation of tasks or external
effects. Source deletion/reintroduction, renaming, overlay changes and deeper
trees require their own declared cases; they are not automatic extra runs.

If the public route works, use its precise local-override/deletion rules to
decide whether an ordinary helper/composition comparison serves a practical
family-change question. Do not promote an expected mechanism result to an
empirical advantage or reopen a stopped gate.
