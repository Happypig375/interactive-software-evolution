# R06 prospective setup amendment — 2026-10-15

Status: written before the amended probe source, any R06 build, and any R06
process. It supplements, and does not rewrite,
`pre-execution-contract.md` (clarified SHA-256
`4ecd7f4afc602c22182aa8fe954d9753e660b2fe980da6c0c5c7c39121df4951`).

## Reason and bounded change

The retained R04 diagnostic found that fresh `Gen.name` brick keys can collide
with fixed B0 keys. Declarative reconciliation then preserves existing entities
whose positions use reinitializing `==`, even though their dynamic colors use
`:=`. The exact finding is
`.artifacts/r04-pause-runtime-20261015/diagnostic-seed-observation-01/diagnostic-finding.md`.
The B0 model can therefore match while two projected positions remain stale.

Amend only the common H/R setup before any acquisition, clock pair, GC sample,
drift, or primary timer. The fixed B0 inputs, ten-pair event word, source-bound
delta checks, H and R recovery operations, readiness boundary, oracles and
attempt order remain unchanged.

## Prospective setup sequence and observations

1. At the first halted functional/accompanied callback, require Gameplay to be
   selected and idling and observe the complete fresh model and projection.
   Install the existing Update and TimeUpdate counters. Read the fixed B0 target
   only long enough to validate its summary and derive the existing canonical
   model/projection string oracles; do not retain that `Gameplay` value.
2. Derive a canonical cleared-model string from the **existing fresh Gameplay
   value with only `GameplayState = Quit`**. Set that record directly with
   `SetGameplay`. Do not publish a quit event and do not evaluate
   `Gameplay.empty` or `Gameplay.initial`; this setup performs no new brick-name
   or color draw.
3. Wait for exactly one further halted post-content callback. Before installing
   B0, require zero Update and TimeUpdate events, the same selected/idling
   Gameplay screen, absence of `B0.scene`, and exact equality between the
   current complete model and the canonical cleared-model string. Record this
   boundary, including counters, selection/idling, scene absence and the model.
4. Only after those assertions, deserialize the unchanged fixed B0 target and
   call `SetGameplay`. At the next halted callback enforce every existing B0
   model, projection, projected-value and negative-control requirement before
   preparing either route's recovery material.

Across callbacks the setup may retain canonical strings and scalar counters
only. It must not retain another `Gameplay`, `WorldState`, or world root. Local
values used within one callback must not be captured by the callback closure.

## Falsifiers and interpretation

Any Update or TimeUpdate event during content removal, callback-count
discrepancy, selection/idling change, advancement, surviving Gameplay scene,
cleared-model mismatch, random-model construction, or weakened B0 oracle fails
the process before measurement. Such
an outcome is retained as setup/fixture evidence and is not a component-cost
observation.

The amendment removes a common reconstruction identity confound from both
routes. It does not change the measured reconstruction after the ten unchanged
identity drift steps, claim that ordinary maintenance uses this setup, or turn
the component probe into a total-maintenance comparison.
