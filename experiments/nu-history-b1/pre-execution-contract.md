# Seeded functional Gaia B1 continuation

**Prospective contract, 2026-10-15; written before implementation/execution.** Continue the [B0 feasibility case](../nu-history-b0/README.md) with a fixed, previously observed model checkpoint. This is a represented-state continuation experiment, not a recovery-cost comparison, a retained native-physics replay, an agent task or a debugging-benefit study.

## Target and comparison

The input is the complete serialized model and selected projection from B0 `history-04`: GameplayTime 149, score 100, 29 bricks and five lives. The earlier process has exited. Its serialized values are copied byte-for-byte into `checkpoint/` with provenance; no original live world root is claimed to survive. Every arm starts a new functional, accompanied Gaia process with the same pinned Nu source, MMCC Breakout application, Gameplay edit mode and static 60-update clock. Selection must settle before reconstruction.

The history arm reconstructs those values with the supported application setter, checks the halted B0 contract, retains a **new** real Gaia snapshot, advances exactly ten screen Updates, halts, and uses actual Gaia undo. It verifies the complete B0 model/projection immediately and at a second halted callback. The fresh arm reconstructs the same input without this drift/undo. Both then resume for exactly twenty screen Updates. Absolute engine update/tick/date clocks, initialization randomness, internal allocation IDs and startup work are excluded from equivalence. Retained brick names, values and selected entity addresses are included.

Use the existing opt-in Gaia bridge and B0 observation helpers unchanged. Nu core and application source are unchanged. Observers record counters outside the retained World so undo cannot silently rewind the measurements.

## Observations and source predictions

Observe after Gaia's ImGui post-process hook, following application Update, deferred tasklets, content synchronization and the normal render-message boundary. This is before the subsequent TimeUpdate. Request halt **inside** the tenth drift or twentieth continuation Screen.Update event, before end-frame tasklets. The predicted local sequence on deferred resumption is `(TimeUpdate, Update)` repeated ten or twenty times; compare actual order and counts, not editor frame count or elapsed time. A post-process halt request would permit an extra Update and is not the selected protocol.

For the twenty-step continuation, record the complete gameplay model, selected projected properties and scene entity names at every matched Update boundary and at a subsequent halted boundary. Require equal traces across arms and agreement with an independently constructed, source-bounded trajectory prediction. The reference calculates only repeated single-precision displacement and a declared horizontal sign change, not a call to `Gameplay.update` or an alternate full game implementation.

From the fixed target, the ball moves down and left at speed three. Its look-ahead wall condition predicts an X-direction reversal on Update **5**, followed by rightward motion. The twenty-step prefix is geometrically clear of bricks (lowest extent 56), paddle (-160), top wall (172) and death threshold (-180); no initialization or respawn should draw randomness. Model time should reach **169**, and paddle, brick keys/values, score and lives must remain unchanged. The complete model comparison checks all fields, not only these summary values. Rotation and HUD projections must follow the matching model time and values.

Observe Left/Right through the same host-key query used by the application on every Update. This is a **monitored absence-of-input** condition; no keyboard replay, focus control or input injection is constructed. Any observed input, reset, screen transition, unexpected model change, event order/count mismatch or missed required bounce is retained as an invalid or failed attempt with its actual phase. It is never silently removed from the execution record. A 200-callback watchdog and 600-second external process deadline bound each attempt. Output directories must be new; all attempts and setup failures are retained.

The source predicts one wall sound request in this prefix, but this experiment has no validated audio-message observer and does **not** test request multiplicity, playback or audio rollback. The sprites use managed geometry collision checks. Native subsystem initialization/integration/reconstruction occurs as part of Gaia, but this case does **not** exercise rigid-body/contact restoration. No framebuffer capture or displayed-image equality is claimed.

## Falsifiers and interpretation

- Restored B0 values agree but either resumed trace differs: the corresponding B1 continuation obligation fails.
- Both arms agree but miss the declared bounce, alter unrelated state or violate the local event schedule: agreement alone does not pass the experiment.
- Model values agree but a projected property or entity set differs: report that projection failure separately.
- The observer cannot obtain the declared phases/counts: retain the observer failure; do not call it a history mechanism defect.
- Any new randomness, input or screen reset invalidates the selected no-input prefix; preserve the attempt and redefine a later contract before another execution.

The original naturally reached B0 witness and this seeded continuation answer different questions. A pass would establish one bounded continuation witness at this pin and observer boundary. It would not establish native replay, general deterministic history, ordinary agent access, comparative cost or Nu's empirical benefit.

## Reproduction and results

Implementation and actual results will be recorded after this prospective contract. Reuse the B0 pinned archive/bridge preparation and its source-integrity receipts; all new binaries, logs and detailed traces belong under ignored `.artifacts/` directories. Keep the executable receipt separate from predictions above. Required source attribution remains in the [B0 bridge installer](../nu-history-b0/prepare.py).
