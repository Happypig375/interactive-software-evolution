# R02 standalone lifecycle pre-execution contract

Frozen before the first build on 2026-10-15. This contract implements the
accepted private proposal at SHA-256
`b50a4c281bde27cb330de7cdba14f196a53d1a4772e8a2e91e8d39fc480d3b55`
and its accepted independent review at SHA-256
`a52297fb0802590d869b78f95fe74797cbdf71171816f9132a28c3378eb2f152`.

## Decision and fixed inputs

The probe asks whether the unchanged MMCC and ImSim Breakout applications at
Nu commit `064f7ae92a8506689cd91aff5e6804a375d6ef3d` can each expose one complete
standalone Play / Gameplay / Quit / Title / fresh-Play lifecycle through public
Nu observation and publication APIs. It is a lifecycle and observer
feasibility check before any pause implementation.

The source archive must have SHA-256
`eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b`
and identify the exact commit in its archive comment. Preparation extracts it
once into a new private directory. Nu engine sources, both application bodies,
plugins, project files, and assets remain byte-identical. The only compiled
addition is a separate arm-specific probe entry point. The build uses .NET SDK
10.0.302, a task-private CLI home and package cache, sequential compilation,
and records every warning and error without filtering or package changes.

## Execution order and limits

There is one assigned runtime per arm, sequentially in `mmcc`, then `imsim`
order. There are no retries, arm replacements, or extensions. Each process has
an external wall deadline of exactly 600 monotonic seconds and an internal cap
of 600 completed `postProcess` callbacks. Natural startup must reach selected,
idling Title by post callback 200. Each counted Play or Quit action must reach
its selected, idling destination within 100 post-callback index increments.
The source-derived nominal destinations at injection callback `c` are MMCC
Play/Quit `c+95`, ImSim Play `c+96`, and ImSim Quit `c+97`; these predictions
are recorded but are not equality requirements and never alter the fixed caps.

The runner must reject any wall deadline other than 600, require the explicit
SHA-256 of a reviewed successful SDK-10.0.302 build receipt, verify the bound
runner and every selected host/probe identity, use a new output directory, and
preserve stdout, stderr, process metadata, the JSONL trace, and result receipt.
Timeout cleanup records all failures and the owned process's terminal state.
Five unresolved failures at one unchanged gate stop further repair. Runtime
remains held until root and an independent reviewer accept the public source,
this contract, and the build receipt.

## Observation boundary

The probe calls public `World.runPlus` with the applications' ordinary
`WorldConfig.defaultConfig` adjusted only for their original window titles. It
sets and reads back `Constants.GameTime.DesiredFrameRate = StaticFrameRate 60L`
and `Constants.Engine.TickDeltaAveraging = false` before world creation. The
first scored callback must observe imperative, unaccompanied, advancing mode.
It also reads the initialized Splash, Title, and Gameplay incoming and outgoing
transition lifetimes and the Splash slide idling time. The required actual
values are `UpdateTime 30`, `UpdateTime 60`, and, for the slide, `UpdateTime
60`; unavailable reads are missingness and complete mismatches are failures.
These effective values, rather than constants alone, support the nominal
transition calculations.

The first `preProcess` installs persistent `World.subscribePlus` observers
with fixed, distinct subscription IDs and `Cascade` handling. They count the
two published ClickEvents and Splash, Title, and Gameplay lifecycle events;
the MMCC arm also counts its application-owned Gameplay QuitEvent. Every
`preProcess` writes only an outer-entry ordinal, a probe-monotonic elapsed
timestamp, and the current update, tick, and game times. The monotonic value
continues to distinguish entries if the game clocks stop. This heartbeat
distinguishes no loop entry from an entry that never reaches `postProcess`.

All phase advancement, projection, assertions, and synthetic action
publication occur in `postProcess`, after application updates, tasklets, ImSim
sweeping, and destruction and before render, audio processing, and the
end-of-loop time update. Every completed callback records a safe, phase-rich
projection before any action. An action callback additionally records complete
before-publication and after-publication projections and the counter delta.
It checks application-owned request boundaries both on entry to a callback and
immediately after publication. Thus a synchronous request can first appear in
the after-publication record while a deferred request can first appear in a
later callback. The probe does not require same-callback consumption. A zero
publication-counter delta is observer missingness; any complete delta other
than zero or one is a behavior contradiction.

The trace records the selected screen, transition state, top-level application
state, effective mode and clock, sampled Left/Right/P held states, persistent
counters and event order, and the arm-specific Gameplay projection. At a
selected Gameplay boundary MMCC records its model time, state, score, lives,
brick count, paddle and ball positions. ImSim records its retained screen
properties plus the existence, positions, and ball velocity of the derived
`Game/Gameplay/Scene/Paddle` and `Ball` entities. The first `postProcess` after
each counted Gameplay Select must show exactly Playing, score 0, lives 5, and
30 bricks. This is a post-step scalar witness after possible update or physics;
it is not an exact pre-first-update initializer observation.

Synthetic publication targets the already existing
`Game/Title/Gui/Play` and `Game/Gameplay/Scene/Quit` ClickEvents. It bypasses
pointer hit testing, ButtonFacet down/up, click sound, SDL delivery, and ImGui
capture. The probe makes no physical-input, full-input, replay, audio playback,
or framebuffer claim.

The probe reproduces `World.run`'s viewport construction exactly: window size
is `Constants.Render.DisplayVirtualResolution * Globals.Render.DisplayScalar`,
`Viewport.makeWindow1` constructs the window viewport, and
`Viewport.makeGeometry windowViewport.Bounds.Size` constructs the geometry
viewport. Before launch it records the virtual resolution, display scalar,
computed window size, and every inner/bounds/outer minimum and size plus the
display scalar for both viewport records. Only the original arm-specific
window title differs between the two unchanged applications.

## Frozen lifecycle oracle

1. Let Splash transition naturally. At selected, idling Title, require the
   installed Title Select and IncomingFinish counters to establish that the
   observer was live, then publish exactly one Play ClickEvent.
2. Record the before/after action states and later first application-owned
   Gameplay request. Require one logical Gameplay Select generation and the
   first-post-Select scalar witness, followed by selected, idling Gameplay.
3. Starting after that idling boundary, take three consecutive post-process
   projections with no injected action. Require sampled Left, Right, and P to
   remain up, selected Playing Gameplay to remain stable, and the arm's ball
   position to change at least once. This is bounded progression evidence, not
   trajectory, collision, backend, solver, or all-input equivalence.
4. After the third projection, publish exactly one Quit ClickEvent. Record the
   MMCC QuitEvent or the ImSim GameplayState=Quit boundary when observed, the
   later top-level Title request, outgoing lifecycle, destination selection,
   and selected, idling Title.
5. At stable Title, MMCC must expose its vacant Gameplay model: time 0, Quit,
   score 0, lives 0, zero bricks, and absent Gameplay scene. ImSim must retain
   the unselected `Game/Gameplay` screen, may retain its screen properties, and
   must have swept the Scene group and its Paddle, Ball, Quit, retained-brick,
   and retained-life descendants. The probe never resets those properties.
6. Hold idling Title for three further callbacks without injection. Require no
   extra click, Gameplay Select, or top-level transition. Publish a second Play
   ClickEvent, require logical Gameplay Select generation two, repeat the exact
   first-post-Select scalar witness, and reach selected, idling Gameplay within
   the fixed action cap.
7. Observe five further callbacks with no injected action. Require no
   unsolicited Quit or Title transition. Final counts must be two Play clicks,
   one Quit click, two Gameplay Select/IncomingFinish events, one Gameplay
   Deselecting/OutgoingFinish pair, two Title Select/IncomingFinish events,
   and two Title Deselecting/OutgoingFinish pairs.

The two arms are compared only on this semantic lifecycle: screen and phase,
application request, logical session generations, common scalar witnesses,
action counts, stable Title behavior, and arm-specific progression. Random
directions, brick names/colors, movement units, physics contacts and identity,
audio requests, and exact callback timing remain outside cross-arm equality.

## Outcomes and falsifiers

A complete contradictory value is a feasibility **failure** and is preserved
with all observed values. Failures include a wrong effective mode or clock; a
live transition exceeding its bound; a counted ClickEvent that does not yield
the application's request; contradictory post-Select scalars; a missing second
logical Select generation; no movement in the three-sample witness; an
incorrect stable-Title lifetime projection; immediate stale Quit/Title in the
second session; a live wrong phase at callback 600; or contradictory final
event counts.

An unavailable, exceptional, or unbound observation is **missingness**, not a
behavior contradiction. Missingness includes no heartbeat before process end
or wall timeout; a heartbeat that never reaches enough post callbacks to apply
the bound; a required public handle/property query that throws or cannot be
bound at its declared phase; an incomplete trace; or inability to prove the
publication counter was installed before injection. Zero lifecycle events at a
known stable destination indicate observer inadequacy; extra completely
observed events are behavior contradictions. No result can revise a bound,
reset application state, or select a favorable random lifecycle.

An engine or cleanup exception after a primary result is emitted is recorded as
an incomplete engine termination and does not overwrite that result. Before a
primary result, an exception is missingness and is distinguished as occurring
before the first loop entry or during the entered loop, with the actual phase
and available observations preserved.

A two-arm pass establishes only bounded standalone launch, lifecycle, and
observer feasibility for these unchanged applications. It does not establish
package equivalence, MMCC-versus-ImSim causality, pause correctness, C-exit's
practical value or frequency, maintenance benefit, standalone agent access, or
the later exact pre-first-step obligation. No pause reference or candidate run
is part of this execution.
