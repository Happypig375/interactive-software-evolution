# R12: public entity propagation in a stub world

One frozen revision of a real Button/Text entity family passed through Nu's
public `World.propagateEntityStructure` operation. The observed values follow
the declared source/target reconciliation rules, including their limits:
source deletion removes a locally edited child, and returning a target value
to the previous source value does not encode an intent to keep it unchanged.
The target was destroyed and recreated, with a different root ID.

This is a bounded mechanism observation for the
[R12 authoring contract](nu-reuse-and-authoring-contract-2026-10-11.md), not a
measurement of reuse benefit, designer productivity, live-object preservation
or an ordinary agent workflow. The [frozen protocol](../experiments/nu-r12-propagation/PROTOCOL.md)
preceded construction and execution. No R02 input or R10 migration work resumed.

## Construction and comparison

The probe references the accepted R03/R05 Nu assembly built from source pin
`064f7ae92a8506689cd91aff5e6804a375d6ef3d`. It uses `Nu.init` and
`World.makeStub`, with actual functional, accompanied and halted flags checked
before the wrapper. The world provides default dispatchers and intrinsic
overlays, stub physics/audio/cursor and a renderer initialized without a window.
The probe creates real source/target entity trees, rather than constructing a
stand-in implementation of the reconciliation algorithm.

Source is a persistent, unprotected Button with four Text children. It is
duplicated through `World.writeEntity` / `World.readEntity` and linked with
`SetPropagationSourceOpt` before either side is revised. The ordinary setter
creates the source's saved previous descriptor. The probe does not inject that
history or call the private descriptor routine by reflection.

The public operation serializes the source and target, applies the engine's
actual descriptor reconciliation, destroys and reads the target back, updates
its affine structure, and advances the saved source descriptor. The source
route is [WorldModule2.fs](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu/World/WorldModule2.fs#L722),
with the ordinary link/index behavior in
[WorldModuleEntity.fs](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu/World/WorldModuleEntity.fs#L678).
The worker's source audit was checked by the parent before construction; this
is maintainer assistance, not an experimental candidate or human review.

## Actual observations

The bootstrap and pre-call observations matched their required trees, values,
mode, persistence/protection, target link and saved v0 descriptor. The single
call then produced these results:

| Revision | Actual target after propagation |
| --- | --- |
| Root source text changes; target has a different local text | `Target override` remains. |
| Shared child matches the previous source value | `Shared v0` becomes `Shared v1`. |
| Target EqualValue is changed to Temporary and then returned to Equal v0 | Both intermediate values are observed before propagation; the final value becomes `Equal v1`. |
| Target locally deletes LocalDeleted while Source retains it | The target child remains absent. |
| Target locally edits SourceDeleted, then Source deletes that child | The target child is removed despite the local edit. |
| Source adds Added | Target receives `Added` with `Added v1`. |
| Target adds TargetOnly | `TargetOnly` remains with `Target only`. |

The target's exact child set is `Added`, `EqualValue`, `Shared`, `TargetOnly`.
Source retains its exact v1 tree, including its own `LocalDeleted` child. The
target stays linked to Source and the saved source descriptor advances to v1.
Complete Nu-written descriptors and actual getter observations are retained;
comparison uses the declared dispatcher/name/text/tree fields, rather than
object-reference equality or a recursive history property.

The target root ID changes from `119` to `324`. This agrees with the executed
destroy/read path; the address-valued Entity handle is reused. No tasklet,
native resource, rendering, pending interaction or external effect was tested
for preservation. The root/child mount choices and other serialized fields
remain visible in the retained descriptors; the oracle does not score their
rendered behavior.

There were 13 bootstrap, 26 pre-call and 14 post-call predicates, all passing.
These include overlapping preconditions and are **not independent cases or
replications**. There is one family, one revision and one propagation call.

## Build, runtime and retained preparation

The first build passed using .NET SDK 10.0.302, with 60 reported NU1901/NU1902
dependency-audit warnings and no errors. Package versions were retained; no
audit override, Nu source modification or engine rebuild was used. The input
host has 189 files totaling 621,372,362 bytes. Its complete copy matched, and
the source host remained unchanged. The actual Nu assembly SHA-256 is
`e96cd61d188c689f7e39e2670b4d8582e26b9ea2dc95e1a15056891b7c99cd68`.

After parent source/build acceptance, one process ran with the frozen
120-second deadline. It returned exit 0 on .NET 10.0.10, called the public
wrapper once, completed the observations and cleanup, and did not time out.
All sealed files remained unchanged. The probe assembly SHA-256 is
`ac247d3141fb8e7116a62955272f881eb102a040efab20b8fc0fb98729d7f999`;
the raw output SHA-256 is
`74f884c10c31ff558d4c25fbbb60d53f2deacc47892f44cd781e503fa7bf2180`.
There was no corrective runtime attempt or replacement fixture.

Before the build, parent source review rejected an observer that would throw
on an absent target and classify a semantic failure as incomplete. The
correction records explicit absence after a completed call as adverse, while
unrelated getter/cleanup exceptions remain incomplete. It also verifies the
actual world mode. The rejected source history and corrected source acceptance
are retained; this correction changed no fixture or expected semantic result.
No compiler or runtime failure belongs to that review rejection.

The [reproduction package](../experiments/nu-r12-propagation/README.md) and
[compact receipt](../experiments/nu-r12-propagation/result-receipt.json) bind
the protocol, source/project/runner, DLL/PDB, original dependency/runtime files,
actual commands, process results, complete manifests and parent verification.
Private source/build/runtime records remain under
`.artifacts/r12-propagation-20261018/`. The reproduction is bound to an existing
sealed host; another build's provenance must be established separately. CI
does not reproduce this private binary-dependent execution.

## Consequence and next work

The quiescent family-revision mechanism is now executable through an ordinary
public engine API. Gaia menu/undo access, save/reopen history and actual button
interaction remain separate. Serialization still calls SDL polling, so this
does not claim that no native library was called.

A useful authoring comparison must choose which local edits should survive a
family change. This run confirms value-based correspondence, local deletion
and source-authoritative deletion for the selected case; it does not infer
user intent from an equal value or preserve runtime lifetime. Contrast those
requirements explicitly when selecting tasks. An ordinary helper/composition
implementation remains a valid comparator and may encode different override
intent; require the same selected behavior rather than penalizing its internal
organization. Count initial construction, per-instance configuration,
revision, extension and verification before claiming less total work. Deeper
trees, rename, deletion/reintroduction and overlay changes need their own
declared obligations if consequential; another passing supported variant alone
would not establish practical benefit.
