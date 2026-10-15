# R04 source-integrated pause runtime contract

**Frozen 2026-10-15 before implementation, builds, or runtime launch.** Pre-launch source reviews clarified failure receipts, randomized initialization invariants, exact entity sets, per-handler deltas, the fresh-play halt boundary, and the five fixed source mutants before any runtime observation. Local construction is already authorized. First launch remains gated only on maintainer acceptance of the amended scientific preflight.

## Scope and arms

Use Nu `064f7ae92a8506689cd91aff5e6804a375d6ef3d`, archive SHA-256 `EB0AA77197DE1971D79AA0657C2AF5CF33B99BA8302A24BA44F3306CCA4BF92B`, .NET SDK 10.0.302, functional accompanied Gaia, Gameplay edit mode, and the static 60-update clock. Every arm gets a fresh archive extraction, private package/build outputs, the same research Gaia callback, and the same audio-request observer.

The four reference arms are:

1. `baseline-explicit`: unchanged application except the existing `| Playing | Quit -> gameplay` terminal clause is retained.
2. `baseline-wildcard`: unchanged application except that clause is `| _ -> gameplay`.
3. `pause-explicit`: the completed common pause application plus `| Playing | Quit | Paused -> gameplay`.
4. `pause-wildcard`: the same completed pause application plus `| _ -> gameplay`.

The two baseline application trees differ only at the selected clause. The two completed pause application trees also differ only there. Nu-core and Gaia instrumentation is byte-identical across all arms. No runtime output may feed a source correction without being retained as a new attempt and protocol amendment.

Five sensitivity variants each start from `pause-explicit` and apply exactly one source fault from [fault-gates.md](fault-gates.md): missing TogglePause binding, Playing-only content, advancing paused time, reset-on-resume, or stale-on-Quit. They are oracle-sensitivity runs, not additional comparison treatments. Preparation emits and hashes the exact single-file patch for each, requires every other application/instrumentation/probe source hash to match `pause-explicit`, and each variant must compile successfully before its own launch.

This is a bounded feasibility/oracle check. It cannot prove whole-application equivalence, physical clicking, native input behavior, audio playback absence, ordinary agent access, pause value, or a source-convention benefit.

## 2026-10-15 prospective reconstruction amendment

The first pause reference attempt and its observation-only rerun are retained as adverse evidence. Both stopped at the unchanged B0 projection oracle. The observation-only rerun showed that two reconstructed B0 brick values had the right keys, sizes, and colors but retained fresh-initial positions. Pinned content reconciliation makes a prior generated-key collision a source-grounded explanation, but the fresh initial key set was not recorded, so collision remains an inference rather than a directly observed fact.

Before the first B0 installation in every reference and sensitivity arm, use the one already-existing fresh Gameplay model and change only its `GameplayState` to `Quit`. Do not publish Quit, call `Gameplay.empty`, or cause another random draw. At the next halted post-content callback, record the actual cleared model, projection, screen, event totals, interval counts, and order. Require exact equality with that one derived model, zero Gameplay Update and TimeUpdate events in the clearing interval, the same selected and idling Gameplay screen, and an absent GameplayScene. Then install the unchanged exact B0 and apply the existing complete B0 model and projection oracle.

This common setup amendment applies prospectively to all four reference arms and all five fixed fault controls. The two already-passing baseline traces remain historical evidence, but both baselines are rerun under this common setup. Application sources, treatment clauses, fault patches, later phase gates, and predicted outcomes are unchanged. The setup is falsified by any Gameplay Update or TimeUpdate event during the halted clearing interval, a screen transition, retained scene, cleared-model mismatch, or a later B0 oracle failure. The amendment and probe-only builds must be frozen and reviewed before another runtime attempt.

## Fixed represented state and baseline fixtures

Use the byte-identical B0 `history-04` symbol already published at `experiments/nu-history-b1/checkpoint/gameplay.symbol`, SHA-256 `FFEE72D91C6E4A32B650D45E9ADDD9E02E179163D0C8BBAAA8CDDB9C92BC783A`. It represents `GameplayTime=149`, score 100, 29 bricks, five lives, a nonterminal `Playing` state, and the complete recorded paddle, ball, brick, and color values. The original process and native world do not survive.

After actual selection and `StartPlaying` settle, reconstruct four fixtures through `SetGameplay`:

- `active`: the exact B0 symbol;
- `lives0`: B0 with only `Lives=0`;
- `empty-bricks`: B0 with only `Bricks=Map.empty`;
- `quit`: B0 with only `GameplayState=Quit`.

For each fixture, observe a halted post-content boundary, then leave the engine advancing until exactly one actual TimeUpdate/Update pair has occurred. The source-bound order is `TimeUpdate`, then `Update`; the Update observer requests halt. Require one event of each kind, `GameDelta.Updates=1` recorded at both handlers, positive advancement evidence at both handlers, and a halted post-content observation.

Expected model outcomes are:

- active: `GameplayTime+1`, ball position advanced once by the recorded velocity, and every other represented value unchanged;
- lives0, empty-bricks, and Quit: only `GameplayTime+1`; the selected update match returns identity.

Expected projections are the complete declared model-derived scene properties. Active and terminal `Playing` retain the scene; lives0 displays `Game over!`; empty-bricks displays `You win!`; Quit removes the scene. The check includes exact entity names, paddle/ball position and size, brick names/values/colors, score, life icons, message, and time-derived rotation. No framebuffer identity is claimed.

Baseline explicit and wildcard traces must agree on these semantic observations and request traces. Independent fresh initialization is checked only by invariants because its ball direction, brick names, and colors are random.

## Completed pause application

Apply these common edits to `Gameplay.fs` and `Simulants.fs` only:

- add `Paused` to `GameplayState`;
- add `TogglePause` to `GameplayMessage`;
- handle it with equality tests: `Playing -> Paused`, `Paused -> Playing`, otherwise identity;
- during `TimeUpdate`, return identity only for `Paused` and retain the existing increment for `Playing` and `Quit`;
- project the scene when state is `Playing || Paused`;
- add `GameplayPause = GameplayScene / "Pause"`;
- add the Pause button at `(232,-112,0)`, elevation 10, with dynamic `Pause`/`Resume` text and `ClickEvent => TogglePause`.

The existing Quit event, top-level `ShowTitle`, deselection reset, and later `StartPlaying` initialization remain unchanged.

## Trigger and phase boundary

Publish the actual unit-valued entity events synthetically:

- `Simulants.GameplayPause.ClickEvent` with publisher `Simulants.GameplayPause` for Pause and Resume;
- `Simulants.GameplayQuit.ClickEvent` with publisher `Simulants.GameplayQuit` for Quit;
- `Simulants.TitlePlay.ClickEvent` with publisher `Simulants.TitlePlay` for fresh play.

Install independent event-count subscriptions before publication. Require the exact counts 3 Pause/Resume clicks, 1 Quit click, and 1 TitlePlay click in that scenario, plus the corresponding state and screen transitions. This exercises real dispatcher subscriptions at the published event boundary. It skips pointer position, Down/Up, perimeter, physical one-shot delivery, and ButtonFacet click sound, so none of those are claimed.

At every scored control boundary, observe button existence, center position, size `(128,32,0)`, visible/enabled state, and text. Pause and Quit share a geometric boundary under their default size; synthetic publication does not test overlap or usability.

## Paused and resumed observations

Reconstruct B0 while halted, verify the normal projection, then publish Pause once. The pause interval begins only after `GameplayState=Paused`, complete retained-model equality apart from that state, scene visibility, Pause text `Resume`, and both controls are observed.

Keep the engine advancing for ten positive TimeUpdate/Update pairs. Require the exact repeated order, `GameDelta.Updates=1` at each of the twenty handlers, twenty handlers that observe engine advancement, and bit/value equality of GameplayTime, paddle, ball, bricks, score, and lives at every post-content observation. Require the declared projection to remain equal and no new `PlaySoundMessage` request during this interval.

Publish Resume once. Before advancement, require `Playing`, retained values rather than `Gameplay.initial`, and button text `Pause`. Advance exactly one no-input TimeUpdate/Update pair with `GameDelta.Updates=1` at both handlers. Require the B0 source-predicted one-step model and projection. Record that Left and Right were both up at this Update; make no held-input or replay claim.

Publish Pause again, then Quit. Advance only as needed for the real transition. Require actual Title selection and idling, the deterministic vacant invariants of `Gameplay.empty`, and scene removal. Do not reevaluate `Gameplay.empty` for exact equality because its `Ball.initial` direction is randomized on every property evaluation. The vacant check binds time zero, `Quit`, initial paddle position/size, initial ball position/size/speed and source-constrained normalized negative-Y direction, empty bricks, score zero, and lives zero. Publish TitlePlay from the halted Title boundary, then resume engine advancement. The Gameplay Update observer halts after the first actual Gameplay Update. At the first selected/idling post-content boundary require exactly one TimeUpdate/Update pair, source-bound order, `GameDelta.Updates=1` at both handlers, and both handlers observing advancement. Require the source-predicted one-step fresh invariants: time one, `Playing`, initial paddle, initial ball size/speed/direction and position advanced once by its sampled velocity, score 0, the 5x6 brick geometry with valid source color ranges, 30 bricks, five lives, exact entity names, and visible Pause/Quit controls. Compare invariants rather than random model identity.

## Audio request observer

Install one opt-in callback in `Nu/Nu/World/WorldAudio.fs` at both `enqueueAudioMessage` and `enqueueAudioMessages`. Each original message is passed to the original `AudioPlayer.EnqueueMessage` exactly once. The plural input is enumerated exactly once. The callback receives the same message after enqueue and only appends an observation; it never drains, filters, reinserts, or mutates World.

Before scored intervals and while halted, validate:

1. a single `World.playSound` produces one observed `PlaySoundMessage`; and
2. a custom plural sequence is enumerated once and its two yielded messages are observed in order.

Do not clear or inspect the audio player's queue. Initialization paths that call `AudioPlayer.EnqueueMessage` directly are outside the hook. Classify requests by observer phase. Control-phase requests and ending triggers are excluded from the paused interval. The scored audio statement is only that no new `PlaySoundMessage` request crossed this hook during the quiescent ten-pair paused interval; native playback is unobserved.

## Scheduling, attempts, and comparison

Count actual Gameplay Update and TimeUpdate events independently. Record their `GameDelta.Updates`, order, callback count, World advancing/halted state, selected and desired screens where available, selected-screen idling, model bits, projection, event counts, and phase-labelled audio requests. Before assertions at pause entry, every paused post-content boundary, resume, halted Title, and fresh one-step completion, emit the actual model and counters plus a non-throwing projection/error capture. A missing projection is recorded as unavailable so observation cannot replace the intended behavioral gate with a logging exception. A missing trigger, absent event pair, wrong order, excess event, watchdog exit, infrastructure failure, or unobserved boundary is not a pass.

Each runtime attempt uses a new immutable receipt directory and a process deadline. Preserve stdout, stderr, trace, process metadata, source hashes, binary hashes, and failed attempts. Compare explicit and wildcard arms only after both complete; do not rescue one arm from the other's output.

## Predicted outcome and falsifiers

Both baselines should pass and agree on the four fixtures. Both completed pause arms should pass the same pause/lifecycle oracle. The wildcard is an intended correct paused-update implementation.

The result is falsified or limited by any unintended application delta; nonidentical instrumentation; failed source/build identity; wrong compiler policy; missing callback positive control; unexpected diagnostic/build failure; wrong event count/order; mutation during pause; hidden board/control; GameplayTime or rotation advance during pause; a PlaySound request during the scored pause interval; reset-to-initial resume; stale model after Quit; nonfresh new play; arm disagreement; or an unavailable observation.

