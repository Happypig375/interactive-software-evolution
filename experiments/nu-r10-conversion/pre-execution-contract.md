# R10 Prime 11.5.1 conversion probe: pre-execution contract

Recorded before the first restore, build, or execution on 2026-10-15. This is
the tracked copy of the original contract. Publication changes source location
and package restore only; it does not change the witness, expectations,
falsifiers, or result definition.

## Scope and fixed witness

The executable calls packaged Prime 11.5.1 `valueToSymbol` and
`symbolToValue`. It tests only the conversion and application-mapping boundary
specified in the [R10 live-edit contract](../../docs/nu-live-edit-contract-2026-10-11.md#application-mapping-for-the-conditional-schema-extension).
It does not load Nu, Gaia, or MMCC Breakout and cannot validate reload,
synchronization, a supported insertion point, effects, or resumed gameplay.

The outer V0 record uses Gameplay's seven field names and expansion policy. The
fixed noninitial witness has gameplay time 941, state Playing, paddle
position/size 110/64, ball position/size/speed/direction 73/8/3/-1, brick keys
`brick-A` and `brick-C` with distinct position/size/color values, score 700,
and three lives. Nested geometry and color are deliberately represented by
integers. Actual MMCC uses Vector3 and Color values and can include mutable or
shared runtime boundaries this probe does not exercise.

## Expectations and falsifiers

1. Raw V0 to reordered, expanded V1 conversion succeeds, retains all seven V0
   fields by name, and supplies `BrickReward = 0`. Any exception, nonzero
   reward, or retained-field difference falsifies this expectation. Because
   zero violates the first-installation requirement of 200, successful raw
   conversion is expected to fail the application mapping.
2. A provenance-aware V0 installation augments the expanded V0 symbol with a
   named `BrickReward = 200` pair before V1 deserialization. It must retain the
   fixed witness and yield reward 200. Any retained-field difference, other
   reward, or exception falsifies feasibility of this isolated mapping.
3. Subsequent V1-to-V1 conversions through Prime must retain rewards 200, zero,
   and 75 exactly. A second ordinary conversion must retain the full state and
   configuration. Resetting zero or 75 to 200, or changing another field,
   falsifies the retained-configuration and repeat requirements.
4. A fresh V1 factory state has reward 200 and fresh score/lives/brick values.
   Reaching those reset values during installation is a failure even though
   they are correct for an explicit new round.
5. Reordering the two fields of the unexpanded nested paddle record is expected
   to map its serialized position into destination size and serialized size
   into destination position. An exception or name-based preservation
   falsifies this positional prediction. A type-valid swap is an adverse
   semantic result, not successful state preservation.
6. Replacing active union case `Playing` with `Active` is expected to throw a
   Prime conversion exception. The local Nu-shaped exception wrapper should
   mark fallback use and return the declared fresh state. No exception, or an
   unmarked or resetless result, falsifies this distinction. This wrapper is a
   probe of exception-only control flow, not evidence that Nu loaded it.
7. An explicitly unknown source edition must return an unresolved error without
   conversion or reset. Inferring V0 from a zero reward falsifies the contract.

Every case is emitted as JSON. The process exits nonzero if any expected
observation is absent. Output also records the loaded Prime assembly identity,
path and SHA-256 hash. A passing explicit symbolic mapping is only a proposed
isolated mapping; it does not validate a usable Nu insertion point or semantic
preservation across mutable references, callbacks, effects, or actual gameplay.
