# R06: one-checkpoint recovery component costs

**Prospective contract, 2026-10-15, before implementation or execution.** Local
construction is authorized. This selects the smallest component comparison
identified from the completed R03 B0/B1 probes. It estimates the work needed to
produce one declared B0 output through two supported routes; it cannot estimate
debugging, maintenance or human-steering benefit.

## Fixed comparison

Use Nu `064f7ae92a8506689cd91aff5e6804a375d6ef3d`, the already verified source
archive SHA-256
`eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b`,
SDK 10.0.302, unchanged MMCC Breakout and functional accompanied Gaia with
the static 60-update clock. Reuse the reviewed B0 snapshot/undo bridge and B1
event scheduling. Both routes use the same instrumented binaries and observer;
a process argument selects the recovery route. Native Gaia processes run
serially after the R04 runtime reservation is released.

Start each process by seeding the complete fixed B0 model from
[`gameplay.symbol`](../nu-history-b1/checkpoint/gameplay.symbol), SHA-256
`ffee72d91c6e4a32b650d45e9addd9e02e179163d0c8bbaaa8cddb9c92bc783a`.
Verify the halted, selected/idling Gameplay boundary and complete model and
projection. The saved file is common initialization material, not free
reconstruction data. Only a canonical output oracle remains common after
setup; do not deliberately retain an extra model/world root solely for checking.

| Phase | History route | Reconstruction route |
| --- | --- | --- |
| Acquire recovery material | Call the real guarded Gaia snapshot operation at the settled boundary. | Read the live Gameplay value and serialize it to an in-memory `scstring` payload at the same boundary. |
| Common drift | Advance exactly ten actual TimeUpdate/Update pairs with no observed Left/Right input, then halt inside the final Update as in B1. | Same logical word and source-predicted drift state. |
| Recover | Call the real guarded Gaia undo operation. | Deserialize the newly acquired payload and call `Simulants.Gameplay.SetGameplay`. |
| Validate readiness | At the next halted post-content callback, require complete B0 model and declared projection equality, selected/idling Gameplay and no advancing event since recovery. | Identical output and phase requirements. |

The ten drift pairs must have source-bound order and `GameDelta.Updates=1` at both
handlers. Require the same complete drift model/projection before recovery.
Both routes must actually acquire their recovery material before drift. The
serialization payload is narrower than a Gaia world root; the result concerns
the declared B0 service, not equivalent whole-world snapshots. Pending work,
external effects, native contacts, framebuffer, input/RNG state, editor history
and other unrepresented state are outside the output contract. The existing
B0 and B1 records remain separate evidence and are not reused as cost samples.

## Outcomes and timing

Use monotonic `Stopwatch.GetTimestamp` and retain frequency and raw ticks.
Gameplay time and whole-process elapsed time are not component clocks.
Measure separately:

1. Recovery-material acquisition, including live model read/serialization in
   reconstruction and the real snapshot call in history.
2. The direct recovery operation, including deserialization and setter work
   in reconstruction and the complete guarded undo call in history.
3. Recovery request to the next post-content callback entry. Stop this timer
   before equality checks or trace output, then validate the boundary. A failed
   or unavailable boundary is not a successful recovery time.
4. Oracle/trace work and process setup/total duration as separate accounting.

Start request-to-ready timing immediately before the recovery call. After its
direct-call stop timestamp, defer oracle scans, JSON serialization and file
writes until the next callback-entry timestamp has stopped readiness timing.
Retain necessary scalar counters in memory. Thus ordinary intervening engine
work stays in readiness time, while discretionary observation does not silently
occupy one route's readiness interval.

Record a paired empty timestamp-call observation as clock-overhead context;
do not subtract a guessed constant from measurements. Record collection counts
for generations 0–2 and total managed allocated bytes at declared phase
boundaries outside the primary timed calls. These process-wide counters can
include concurrent engine/runtime work and are not exclusive allocation
attribution. Do not force collection or change the GC policy.

Different GC outcomes remain part of the observed route result. Do not remove,
condition on or adjust away a collection to present a cleaner mechanism effect.
Report the full observations and the ambiguity of attribution. Managed live
heap/process memory, if recorded, are secondary snapshots: they do not measure
retained-root size, release, native-subsystem cost or a bounded-history policy.
No new clear/eviction or `World.switch` subsystem instrumentation is needed for
this comparison.

The common oracle must compare all declared model fields and nested values,
brick identities, exact entity-name set and selected projected properties,
using the existing bit/value encoding. Preserve actual pre/post models,
projection, callback and event counts, event order, observed deltas, host-input
observations, mode/clock and phase. Log outside primary operation timers. Retain
the actual state and error if an assertion fails. Readiness cannot be inferred
from a successful return or an internally consistent but wrong target.

## Assigned attempts

First perform one unscored feasibility process per route. These observations
are retained and labeled feasibility, with no performance claim or addition
to the measured set. Before measured execution, freeze and hash the accepted
implementation, binaries, setup and observation policy. A failed feasibility
gate permits a documented instrumentation correction; it does not disappear
from the attempt record.

Then assign six fresh-process pairs, twelve measured processes, in this fixed
balanced order:

```text
H1 R1  R2 H2  H3 R3  R4 H4  H5 R5  R6 H6
```

Each process makes its first measured acquisition and recovery after the same
seeded setup. There is no hidden warm-up for a preferred route. These are local
first-use observations with possible JIT, OS-cache and temporal effects, not
steady-state or independent-application samples. The six pairs are a bounded
descriptive feasibility sample, not a powered efficacy study. Keep every
assigned process, including timeouts, failures and missing observations.

Use a 600-second process deadline and the existing 1,200-callback watchdog.
Each attempt receives a new immutable directory. Retain configuration, source
and binary hashes, stdout/stderr, raw trace, process metadata and decision.
No favorable outlier filtering, replacement process or post-observation sample
extension is allowed. Stop and investigate an unexpected semantic or
infrastructure failure before further measured processes; preserve the
interruption and require a dated amendment before a new measured series.
The general five-unresolved-failures-at-one-unchanged-gate rule still applies.

## Interpretation and falsifiers

Report all assigned outcomes and per-attempt raw durations/counters. For valid
completed outputs, provide route medians/ranges and paired differences without
an inferential significance or population-benefit claim; retain failed/unknown
outcomes alongside those summaries. A fast failed restoration is not a fast
successful service. Any missing/different target, input, event word, phase,
clock, instrumentation or binary identity invalidates the proposed matched
component interpretation for that pair.

History may cost more, allocate more or show worse variability; reconstruction
may cost more because serialization/conversion/content reconciliation is
expensive. Both are legitimate outcomes. This case does not isolate retention
overhead, establish a memory-reclamation policy or supply a native physics
estimate. Construction, integration, ordinary workflow access and practical
repair outcomes remain required for a later total-maintenance-value claim.

## Pre-build clarification, 2026-10-15

Source review found that the reused B0 bridge retains a second strong
`WorldState` reference solely to verify the next undo target. For this cost
comparison, use a weak identity witness in an isolated R06 Gaia source tree,
preserving the same reference-identity guard against the next RestorePoint.
Do not change the published B0 bridge or its historical executable source.
The weak witness's allocation and guard work remain inside the measured
supported history route; this is instrumented access, not a subtraction or an
estimate of an uninstrumented UI operation. Other snapshot/undo behavior and
the declared output contract are unchanged.

Capture an unconditional callback-entry timestamp as the literal first
callback operation, then use that captured value if recovery is awaiting
readiness. This realizes the specified entry boundary without including the
phase-selection branch. These corrections precede every R06 build and runtime
observation. Retain the original contract hash and source-review receipts as
prospective design history; the accepted build and measured-series freeze must
identify this clarified contract and the exact isolated bridge bytes.

The selected `GC.GetTotalAllocatedBytes(false)` counter is approximate and
excludes native allocations; label it accordingly and do not infer zero
allocation from a zero difference. A precise call has additional overhead.
`GC.GetTotalMemory(false)` supplies a secondary heap-size observation excluding
fragmentation, not retained checkpoint size or proven reachable payload. These
API meanings are verified against the .NET 10 documentation for
[allocated bytes](https://learn.microsoft.com/en-us/dotnet/api/system.gc.gettotalallocatedbytes?view=net-10.0)
and [heap size](https://learn.microsoft.com/en-us/dotnet/api/system.gc.gettotalmemory?view=net-10.0).
Keep both calls outside the primary timers and retain the chosen non-forcing
policy. Phase-boundary counter differences include observation work between
samples as well as engine/runtime activity; they are descriptive context.
