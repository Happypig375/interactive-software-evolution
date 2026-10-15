# Functional Gaia: bounded represented-state continuation

**Executed 2026-10-15.** One fixed, twenty-update MMCC Breakout continuation agrees after actual Gaia history restoration and fresh reconstruction. Complete gameplay values and the selected scene projection match at every observed step. Both arms also satisfy the prospectively predicted wall bounce, unchanged non-ball values and exact logical-event schedule. This extends the [B0 witness](nu-history-feasibility-2026-10-15.md) to one B1 prefix; it does not measure debugging benefit, comparative cost, ordinary agent access or native-physics replay.

## Prospective choice and source identity

The [contract](../experiments/nu-history-b1/README.md) was written before implementation and execution, and an independent maintainer checked its source scheduling and geometric bounds before either run. The parent implemented and accepted the observation/comparison. Neither review is human scientific sign-off or independent implementation replication.

B0 `history-04` had exited. The [fixed input](../experiments/nu-history-b1/checkpoint/provenance.json) therefore carries only its serialized model and selected projection: time149, score100,29bricks,5lives, and the complete realized values/names. Both new processes reconstruct that input after Gameplay selection settles. In the history arm, a **new live Gaia snapshot** is retained, followed by ten Updates, an effective halt and real Gaia undo. The fresh arm omits this drift/undo. This seeded experiment does not resume the old process or preserve its native state.

The isolated source remains Nu `064f7ae92a8506689cd91aff5e6804a375d6ef3d`. A second archive comparison checked all **3,240 original files**: only `Nu/Nu.Gaia/Gaia.fs` differs, exactly the existing B0 bridge with SHA256 `98e8c470c2795472f13a9ccf8f2c002b56be8235db40ca95c4a9fd3b07462012`. No Nu core or application source was changed. The development checkout at `A:/Nu` was untouched.

The new build's Nu DLL is `5bcf797de1ae15dc79f9a0f49b30d96247816f928b158a519f64cb563f8b8e3c`, with product metadata `1.0.0+064f7ae92a8506689cd91aff5e6804a375d6ef3d`. It is a new binary build, not byte-identical to the earlier B0 DLL. Both B1 arms use identical probe, Nu, Gaia, application, helper and FSharp.Core binaries; the [receipt](../experiments/nu-history-b1/result-receipt.json) gives their hashes. Source identity, product metadata and binary identity remain separate evidence. SDK10.0.302/runtime10.0.10 were used.

## Schedule and observations

Resumption is requested from the halted post-process hook. Because tasklet processing has already passed, the next frame starts halted, applies the deferred resume and emits an activation TimeUpdate. Each later Update precedes its next TimeUpdate. Requesting halt inside the final Update makes it effective in that frame's tasklet phase, suppressing the trailing TimeUpdate. The expected event word is therefore `(TimeUpdate, Update)^N`, not an inferred one-step property of a GUI button.

The history drift has exactly ten of each event; undo and the following halted callback produce none. Continuation has exactly twenty of each in each arm. External measurement counters survive undo: history ends at30/30 and fresh at20/20. Comparison uses local step numbers and event words; it does not require equality of these deliberately different totals or of absolute engine clocks.

Every continuation observation follows Update, tasklets, ImSim/content and Gaia's normal render-message processing, before the next TimeUpdate. The probe compares every represented gameplay field by exact single-precision bits and map keys/values against a bounded source prediction. That prediction calculates displacement with a declared sign reversal; it does not call `Gameplay.update`. The separate Python comparison checks complete models and selected projections between arms and the exact phase/event schedule.

The selected projection covers all scene entity names, paddle/ball positions and sizes, brick positions/sizes/colors, score/message text and model rotation. It is not an assertion about every possible entity property, a framebuffer or the whole WorldState. Left/Right queries are monitored at each Update through the same host query used by the application; both counts remain zero. No input injection or replay was constructed.

## All attempts and outcomes

| Attempt | Actual outcome |
| --- | --- |
| Build01 | Failed with one F# FS0001 syntax error: a missing list-element separator in the schedule observation.396 dependency warnings. No runtime launched. |
| Build02 | Added the separator; build passed with243 dependency warnings and zero errors. No requirement was weakened. |
| History01 | Exit0, no timeout. New seed, snapshot, ten-step drift, effective halt, actual undo, immediate/next-halted B0 checks, then twenty continuation observations and a final halted check all passed. |
| Fresh01 | Exit0, no timeout. Fresh initialization differs from the target as required by its negative control; full reconstruction passes, then the same twenty continuation observations and final halted check pass. |
| Comparison01 |20/20 complete models and20/20 selected projections agree. Exact local event words agree. Deliberately corrupted projected position, step order and event order are all rejected. These three checks mutate in-memory observations; they are not extra runtime tasks. |

Both continuations reverse the horizontal direction on **Update5**, from bit pattern `BF5B043E` to `3F5B043E`. At Update20, time is169, score100, bricks29 and lives5. The final ball position is approximately `(-119.9222565,22.2911835,0)`, with direction `(0.8555335,-0.5177476,0)`; the receipt retains exact bits. Paddle and all brick values/names remain unchanged. No callback watchdog or600-second deadline was reached. All build and runtime logs/trace hashes are retained under `.artifacts/r03-b1-20261015/`.

Process durations were48.156 and39.984seconds. The arms perform different work and include rendered startup; these durations are execution-accounting facts, **not a cost comparison**. No unfavorable runtime attempt was discarded or replaced.

## What follows

This is a positive bounded mechanism result: a newly retained world and a supported fresh setter reconstruction yield the same declared continuation at the selected pin. The no-RNG prefix deliberately avoids respawn/reset. Sound requests/playback, hidden entity state, host input history, whole-world identity, native rigid-body/contact state and rendered pixels remain outside the measured contract. Managed Breakout geometry does not exercise physics restoration merely because native engines run around it.

The B0/B1 observation gap for this represented-state case is now resolved at the instrumented boundary. Before a cost or agent-benefit study, select a practical recovery/repair obligation and account for checkpoint acquisition, setup, retention/reconstruction and validation work in both arms; ordinary agent access remains unverified. A native-physics, audio-effect, schema-change or randomness promise needs its own correspondence and observations. Broader Nu benefit and other prepared directions remain empirical questions.
