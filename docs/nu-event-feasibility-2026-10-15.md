# Nu R05 event-delivery feasibility

**Decision, 2026-10-15:** a small isolated harness can observe Nu's actual
compiled event graph through `World.makeStub`. At source pin
`064f7ae92a8506689cd91aff5e6804a375d6ef3d`, the bounded checks observed
descending simulant priority, `Resolve` stopping later delivery, delivery from a
never-created publisher handle, and explicit plain-subscription removal. This is
a mechanism-feasibility result for R05 support. It is not a full-game trace,
event-sourcing result, benefit estimate, or general correctness validation.

## Contract fixed before execution

The private pre-execution record selected three observations using Nu's public
`World.subscribePlus` and `World.publishPlus` APIs. The harness contains no fake
event system.

1. A hierarchical publication had exact-address subscribers at Group, Screen
   and Game priorities. Every handler returned `Cascade`; the trace had to
   contain each label once in the declared priority order.
2. A second publication used the same subscribers but returned `Resolve` from
   Screen. Delivery after the resolving handler was the falsifier.
3. A plain subscription named a Screen publisher handle that was never created
   in the stub world. `before` had to deliver once, and the same publication
   after calling the exact unsubscription callback returned by `subscribePlus`
   had to deliver zero times. Failure of the first delivery would falsify this
   bounded publisher-neutral case; a second delivery would falsify explicit
   removal.

The first declaration incorrectly inferred ascending order from the numeric
priorities: `group,screen,game`, then `group,screen`. The first actual trace was
`game,screen,group`, then `game,screen`; the lifetime check returned only
`plain:before`. The process exited 1. Inspection then found that pinned
`SortPriority.compare` deliberately orders larger elevation first
(`WorldTypes.fs:225-230`). Thus the run falsified the observer's assumed order,
not Nu's source-defined priority relation. This adverse attempt is retained; the
source-bound expectations were corrected to `game,screen,group` and
`game,screen` before the final run.

## Source and binary identity

The source came from the existing authorized archive. Its integrity receipt
identifies the requested pin, archive SHA-256
`EB0AA77197DE1971D79AA0657C2AF5CF33B99BA8302A24BA44F3306CCA4BF92B`,
3,240 checked files and zero mismatches. The final runner additionally verified
hashes for `EventGraph.fs`, `WorldTypes.fs`, `WorldModule.fs`, `World.fs` and
`Nu.fsproj` before compiling the harness.

The first Release Nu build used those verified sources but inherited the
enclosing research repository's Git revision in its ProductVersion. Its SHA-256
was `34333D868469A76E686B4651E0329BE810505FB2EEB6FC6576E0AD68EE239DE5`
and its misleading ProductVersion ended in `49ff4d9...`. That provenance defect
is retained rather than treated as evidence of different source contents. Nu
was rebuilt with an explicit `SourceRevisionId`; the final input and loaded copy
both had SHA-256
`E96CD61D188C689F7E39E2670B4D8582E26B9EA2DC95E1A15056891B7C99CD68`
and ProductVersion
`1.0.0+064f7ae92a8506689cd91aff5e6804a375d6ef3d`.

## Actual final observations

The isolated final and publication-check runs used .NET SDK 10.0.302 and .NET
runtime 10.0.10. The loaded Prime assembly was 11.5.1.0, informational version
`11.5.1+4026f3156865d536d0c4d36f1dc361485df8117a`. Restore, Release build and
execution all exited 0; the publication build had zero warnings and errors.

```text
RESULT cascade-priority expected=[game,screen,group] actual=[game,screen,group] pass=true
RESULT resolve-stop expected=[game,screen] actual=[game,screen] pass=true
RESULT publisher-neutral-explicit-unsubscribe expected=[plain:before] actual=[plain:before] pass=true
SUMMARY pass=true stubWorld=true fullGameLoop=false hostInput=false nativeBehavior=false
```

The first trace observes descending subscriber elevation across exact-address
subscriptions under hierarchical publication. It does not isolate wildcard
address specificity or establish a context-free order for every publication.
The second trace observes that Screen's `Resolve` prevents the later Group
callback in this ordering. The third trace supports the narrower source claim
that a plain subscription does not require the publisher to exist and remains
until explicitly removed. It does not exercise `monitorPlus`, subscriber
unregistration, publisher destruction, identity reuse, or ImSim sweeping.

## Attempts, reproduction and limits

Two compile-only harness errors were retained: an initially unqualified static
`Game.Handle`, then missing parentheses in assembly-report arguments. The first
restore also surfaced NuGet audit warnings from Nu's pinned dependency set; no
dependency was changed. The tracked runner's first wrapper invocation used the
unavailable `pwsh` executable, and its next PowerShell 5.1 attempt treated
captured native stderr as terminating. The runner was made compatible with
Windows PowerShell 5.1 by using explicit process capture. A fresh publication
directory then passed, and rerunning against that nonempty directory was
rejected as designed. All private attempts remain under
`.artifacts/r05-events-20261015/`.

The reviewable package is
[`experiments/nu-r05-events`](../experiments/nu-r05-events/README.md). It accepts
explicit Nu-source and output paths, verifies the source identity and relevant
file hashes, refuses a Nu DLL whose ProductVersion does not identify the pin,
writes build products only below the requested output, verifies that the input
DLL did not change, and rejects nonempty output directories. Its compact
[`result-receipt.json`](../experiments/nu-r05-events/result-receipt.json)
preserves the first assumption failure and final observations.

`World.makeStub` initializes the compiled Nu World/EventGraph with stubbed
subsystems. It does not run an application frame or prove screen transition,
input-capture, selected-only, entity-lifetime, effects, or native behavior. It
also provides no multiplicity result for physical clicks and no universal
exactly-once guarantee. A consequential next runtime case should use an actual
application lifecycle only when its phase, owner identity, trigger, horizon and
effect observations are separately fixed. This probe does not by itself promote
R05 or R13, and it did not construct an agent adapter or run a candidate model.

## Fuller coordination method, 2026-10-15

The completed [S205 dissertation](literature/full-reading/S205-jescala-dissertation-access.md) distinguishes event-graph propagation from per-group queue consumption, occurrence-dependent caller blocking and actor-backed serialization of proxy handlers. Its specialized FSM and monitor cases supply useful scoped performance evidence, not a Nu oracle or maintenance effect. The current probe does not test those contracts. A later practical comparison promising them must observe queue/group identity, actual order, sender/reaction thread, blocking/completion, registration/removal and failure behavior, and count instrumentation/synchronization/verification work. Do not add those mechanisms merely to enlarge this feasibility case.
