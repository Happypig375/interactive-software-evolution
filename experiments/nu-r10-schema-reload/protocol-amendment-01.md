# R10 schema probe: pre-execution clarification 01

2026-10-16. This amendment follows independent protocol review. Harness drafting
has begun, but the implementation owner confirmed that source preparation,
build and native execution have not begun. The original frozen contract is
retained unchanged (SHA-256
`4c6bc39e4927c593f14026373d8e1a147a721c15dc1228a260c1643cf0006076`).
This clarification expands no application treatment or outcome.

## Complete independent oracle

The post-update oracle covers the complete represented model, not only the
scalars listed in the original contract. Relative to the independently
reconstructed checkpoint, the expected post-state is:

- GameplayTime 150 and GameplayState Playing;
- identical paddle position and size;
- ball position `(-64,56,0)` and direction `(0,-1,0)`, with size and speed
  unchanged;
- exactly the old brick map minus `@455`, with every other key, geometry and
  color unchanged;
- score `100 + observed reward`, lives 5, and the observed reward unchanged.

The required mapped case has reward 200 and score 300. A valid live observation
with reward zero instead has score 100; its removal/bounce obligations remain.
The expected retained-field structure is prepared before live reload from the
frozen checkpoint and declared arithmetic/geometry, without calling application
update code. The observed scalar reward selects the arithmetic result; it does
not define the other expected fields. Fresh/live agreement is a secondary
comparison and cannot pass two identically incorrect arms.

Check the complete declared scene projection against these expected values,
including the exact entity-name change, remaining brick values, paddle/ball,
score/lifecycle text, life indicators and the time-derived static-model rotation.
Fields of that projection unaffected by the declared update remain equal to
the checkpoint. Require zero sampled Left/Right-held input during the actual
advancing update, as well as the pre-advance counts. The next halted observation
must preserve the complete post-state and projection with no extra update.

## Failure threshold

The project's five-unresolved-failures return rule applies to **every unchanged
gate**, including preparation, compilation, launch and runtime observation.
Preserve one chronological attempt ledger recording each gate and disposition.
Changing compiler error classes does not reset the compilation gate. A fifth
unresolved failure at one gate requires return before another attempt there;
later successful attempts cannot retroactively satisfy the rule.

An expected negative checker control is not an unresolved engineering failure.
A valid observation of a failed application requirement is a scientific result,
not permission to rerun until the desired mapping appears. No explicit mapping
repair belongs to this initializer-only arm.
