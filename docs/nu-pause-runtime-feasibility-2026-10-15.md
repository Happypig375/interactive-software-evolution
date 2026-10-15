# Nu R04 pause runtime feasibility, 2026-10-15

## Result

The bounded source-integrated check completed. Both current baselines passed four one-pair fixtures, and both completed pause implementations passed the full pause/lifecycle oracle. The explicit and wildcard arms had equal fixed observations within each pair. Five frozen source faults were then detected once each at their prospectively declared first gates.

This establishes feasibility for the pinned MMCC Breakout construction and shows that the wildcard is a legitimate implementation of the selected paused-update clause. It does not show a maintenance advantage for explicit enumeration, measure diagnostic attention, or prove whole-application equivalence beyond the fixed observations.

The construction used Nu `064f7ae92a8506689cd91aff5e6804a375d6ef3d`, .NET SDK 10.0.302, functional accompanied Gaia, the fixed published B0 symbol, isolated sources, and four references:

1. unchanged baseline with `Playing | Quit`;
2. unchanged baseline with `_`;
3. completed pause with `Playing | Quit | Paused`;
4. completed pause with `_`.

Within each pair, the selected update clause was the only application-treatment difference. Common pause behavior required coordinated edits to the union, toggle message/transition, TimeUpdate, scene-content predicate, simulant handle, and Pause button.

## Observations

The baseline fixtures were active B0, lives zero, empty bricks, and Quit. Each ran exactly one source-ordered TimeUpdate/Update pair. Both clauses produced the declared model and complete projection for all four fixtures. After excluding configuration and independently generated setup values, their 13 fixed trace records were exact JSON matches.

The completed references reconstructed unchanged B0, published the real Pause ClickEvent, and observed `Paused` with the scene and Resume control present. During ten positive event pairs, GameplayTime remained 149 and all represented paddle, ball, brick, score, lives, control, entity-name, text, color, and rotation values remained fixed. All 20 handlers saw engine advancement with `GameDelta.Updates=1`; this was local application pause, not an engine halt. No `PlaySoundMessage` crossed the observer during the interval.

Resume retained B0 and advanced exactly one pair to the source-predicted time-150 model. At that Update, the probe sampled Left and Right as both up; it did not observe all possible input or replay state. A second Pause followed by Quit reached selected/idling Title with the vacant invariants and no GameplayScene. TitlePlay then produced one source-predicted fresh pair at time 1. Each arm recorded Pause/Resume count 3, Quit count 1, and TitlePlay count 1. The two arms' 22 fixed B0 records through resumed completion matched exactly as canonical JSON. Their later random vacant/fresh values differed as expected and independently satisfied the frozen ball, grid, color, lifecycle, and projection invariants.

The source faults supplied actual oracle-sensitivity evidence:

| Fault | Observed first failure |
| --- | --- |
| missing Pause binding | counted Pause event left the model Playing; `pause-reached` |
| Playing-only content | model became Paused but scene disappeared; `pause-projection` |
| advancing paused time | first positive pair changed time 149 to 150; `pause-frozen-model` |
| reset on resume | ten frozen pairs passed, then Resume produced a fresh time-0 model; `resume-retained` |
| stale model after Quit | Title selected/idling but time-150 Paused B0 values remained; `quit-reset` |

Each detection produced probe exit 1, engine exit 0, no timeout, and the required prior trigger/count evidence. No fault was rerun or repaired after observation.

## Reconstruction limitation

The initial baseline pair passed before the common setup amendment. The first pause-explicit run then failed at the B0 projection gate before any click or update. That trace did not include enough projection detail. A prospective observation-only probe reran the same frozen application and stopped at the same gate; it recorded B0 bricks `@477` and `@478` with their correct B0 colors but fresh-grid positions `(-128,64)` and `(-128,80)` instead of `(128,128)` and `(128,144)`.

Pinned content reconciliation reuses a child when key and dispatcher agree. Position uses the initialization/reinitialization operator while color is dynamic. That source policy is consistent with a prior generated-key collision: retained position and updated color. The fresh initial key set was not logged, so the collision remains an inference.

The dated protocol amendment derives a clearing model from the one already-existing initial model by changing only `GameplayState` to `Quit`. At the next halted post-content callback it requires exact derived-model equality, zero Gameplay Update/TimeUpdate events, the same selected/idling Gameplay screen, and no GameplayScene. It then installs unchanged B0 and applies the original complete oracle. All nine final runs passed that common boundary.

This step is visible alignment work. Direct `SetGameplay` into a populated generated-name scene is not a general reconstruction guarantee across same-name identities, and clearing content does not demonstrate that live replacement preserves identity.

## Build and hosting evidence

The final full preflight prepared four references plus five exact single-fault variants and built all nine complete Release/net10.0 graphs. Every graph exited 0 with 334 warnings, zero errors, and only NU1608, NU1901, and NU1902. No package or warning policy was overridden.

The clearing amendment changed the tracked probes after the engine builds. To preserve the accepted engine evidence, each amended probe was compiled directly against its arm's frozen output. All nine probe-only builds exited 0 with zero warnings and errors. The runtime wrapper copied and verified each complete host manifest, checked the external application hash and exact 600-second deadline, and ran `AmendedProbe.dll` using the original 44-library `Probe.deps.json` plus original runtime configuration. It added five probe files and did not replace application, Nu, Gaia, native, or dependency binaries.

The first probe-only build attempt is retained: baseline-explicit compiled, then the harness failed because it resolved a preflight-relative receipt path from the repository root. The corrected harness changed only that resolver. The probe and contract bytes were unchanged.

The complete preparation history includes eight numbered preflights, two successful narrow harness checks, the original baseline successes, both retained pause reconstruction failures, four amended reference successes, and five expected source-fault detections. [The tracked receipt](../experiments/nu-r04-pause-runtime/preflight-results.md) records the chronology. [The compact JSON receipt](../experiments/nu-r04-pause-runtime/result-receipt.json) binds current sources, build receipts, loaded assembly hashes, raw process/trace hashes, results, comparisons, and parent verification receipts.

## Trigger, audio, and scope

The driver publishes actual unit-valued Pause, Quit, and TitlePlay entity events and subscribes independently to their counts. This checks real dispatcher subscriptions at that event boundary. It skips pointer position, Down/Up, perimeter/overlap, physical one-shot delivery, native input, and ButtonFacet click sound.

The identical opt-in audio callback observes requests only at `enqueueAudioMessage` and `enqueueAudioMessages`. A single and plural positive control proved callback reachability and one-pass plural enumeration. The claim is only that no new PlaySound request crossed those helpers during the scored paused interval. Native playback and direct core initialization enqueue are outside scope.

The result is one pinned application, mode, successor requirement, and observation protocol. It does not establish practical value, common task frequency, whole-Nu behavior, a completed physical pause feature, candidate access, agent maintenance benefit, or superiority of one clause. The five faults demonstrate oracle sensitivity to authored faults; they do not estimate fault prevalence.

Because `experiments/nu-r04-pause-runtime/` and this document are new paths outside the recognized routing table, change-scoped CI should conservatively use **full** validation when the maintainer publishes them.
