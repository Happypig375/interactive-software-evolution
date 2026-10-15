# R10 behavior-only live-reload pre-execution contract

Frozen before source extraction, build, or runtime execution on 2026-10-15.

## Scope

This gate calls the pinned Gaia `tryReloadCode false` core through one named,
guarded research bridge. It bypasses the F9/menu invocation phase. It tests one
unchanged-model edit, actual FSI type/dispatcher installation, complete
represented model and selected projection preservation, one declared future
brick hit, and a matched fresh reconstruction.

No audio request/playback, framebuffer, native-host resource, arbitrary schema,
atomic rollback, cost, productivity, or benefit claim can pass this gate.
Those effects remain pending even if source state and behavior pass.

## Frozen source edit and checkpoint

Use Nu commit `064f7ae92a8506689cd91aff5e6804a375d6ef3d` in a fresh archive extraction.
Add the reflectable, non-model seam `static member BrickReward = 100`; replace
the scoring literal with `Gameplay.BrickReward`; build and launch that old-code
baseline. Only after the old checkpoint is halted and written, change the
single member literal from 100 to 200. Do not change the seven Gameplay fields.

Seed the published B0 represented state (time 149, score 100, lives 5, 29
bricks), changing only the ball to position `(-64,53,0)`, size `(8,8,0)`, speed
3 and direction `(0,1,0)`. No input or RNG is used after seeding. The existing
brick `@455` is centered at `(-64,64,0)`, size `(64,16,0)`.

The one fixed schedule is `TimeUpdate` then `Update`, with `GameDelta.Updates =
1`. Motion stores ball position `(-64,56,0)`; collision tests its next point
`(-64,59,0)`, inside only `@455`. Expected new-code state is time 150, score
300, lives 5, 28 bricks with only `@455` removed, and ball direction `(0,-1,0)`.
Old code would produce score 200. A second halted callback must be stable.

## Before-advance live acceptance

Before reload record old complete symbol/projection, raw model type and assembly,
dispatcher identity, and reflected reward 100. Capture the exact generated FSI
script from the core path. After the bridge returns and before advancing:

- complete raw-object symbol and projection equal the checkpoint exactly;
- no update/time-update/input count changed;
- returned FSI assemblies have recorded FullNames and MVIDs;
- exactly one returned FSI record type has `Name = Gameplay`, the exact seven
  Gameplay record fields, and public static reward 200;
- the raw model's `Type` equals that actual type by reference;
- the installed GameplayDispatcher's generic model argument equals that type;
- model and dispatcher assemblies are members of the returned assembly set.

FSI may prefix generated full names. Record them; do not require the literal
FullName `Breakout.Gameplay`. Name/schema matching alone is insufficient.
`CodeReloadEvent`, compiler output, or loading reward 200 without installing
the actual type cannot pass.

After reload, never call an old statically typed `GetGameplay`, `SetGameplay`,
model serializer, or model projection helper. Observe the raw object through
`GetModelGeneric<obj>` and reflection/symbol conversion only.

## Fresh arm and falsifiers

Build the reward-200 source into a fresh process. Reconstruct the exact frozen
checkpoint with that process's current type before advancing, verify complete
model/projection, execute the same one-event-word schedule, and require the same
post-state and next halted stability. Fresh success cannot make a failed live
arm pass.

Intentional in-memory oracle controls must reject: (a) score 200/old reward,
(b) reset state, and (c) missing the wrong brick. These are data controls, not
runtime failure trials.

Fallback/reset, regenerated brick keys/colors, any checkpoint drift during
reload, old model/dispatcher retention, ambiguous FSI type identity, wrong
event word, input, extra update, total score other than 300, wrong ball/brick/
life/time state, next-halted drift, timeout, or unmatched fresh reconstruction
fails the relevant arm.

## Execution discipline

Record every extraction, patch, build, and runtime attempt; source/configuration
and loaded assembly identities; exact script; event word; no-input counts; and
wall times as attempt metadata only. Each retry uses a fresh process/output and
a recorded reason. Five unresolved failures at one unchanged gate stop work.
Do not patch the pinned FCS private fields, package versions, fsproj path parser,
or expected result to force success. Preserve all failures privately.
