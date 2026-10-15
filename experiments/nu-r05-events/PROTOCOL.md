# Frozen R05 event observation protocol

This package exercises Nu's compiled event implementation at source pin
`064f7ae92a8506689cd91aff5e6804a375d6ef3d`. It calls `World.makeStub`,
`World.subscribePlus`, `World.publishPlus`, and the returned unsubscription
callback. It contains no replacement event system.

## Observations and falsifiers

1. Three exact-address subscriptions use Group, Screen, and Game subscribers.
   Hierarchical publication must follow the pinned descending elevation order,
   `game,screen,group`, exactly once each when all handlers return `Cascade`.
2. With the same priorities and the Screen handler returning `Resolve`, the
   trace must be `game,screen`. Any later Group delivery violates the bounded
   stop-propagation observation.
3. A plain subscription names a Screen publisher handle never created in the
   stub world. The `before` publication must deliver once. After invoking the
   unsubscription callback returned for that exact subscription, the `after`
   publication must not deliver. The expected combined trace is `plain:before`.

The first private attempt had declared ascending order
`group,screen,game` / `group,screen`. Actual traces were
`game,screen,group` / `game,screen`; the unsubscription check passed. Source
inspection then found the descending comparison in `SortPriority.compare`.
That observer-specification failure is retained in the receipt and feasibility
record. The source-bound expectations above were fixed before the final run.

## Scope

The stub initializes Nu's real EventGraph and World machinery without game
assets. It establishes these three in-process capability observations. It does
not execute the full frame loop, selected-only filtering, host input, transition
handlers, entity destruction, ImSim sweeping, `monitorPlus` removal, native
subsystems, or an actual game. It supplies no benefit, performance, universal
ordering, exactly-once, or whole-application correctness result.
