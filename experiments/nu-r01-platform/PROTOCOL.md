# Frozen protocol: ordinary dynamic rider on a kinematic platform

This tracked copy republishes the protocol frozen in
[`docs/nu-platform-feasibility-2026-10-15.md`](../../docs/nu-platform-feasibility-2026-10-15.md)
before the first fixture execution. It was also present before the tracked
reproduction run. The reproduction changes output placement only; it does not
change physics inputs, observation phases, tolerances, or outcome rules.

## Boundary

The question is whether Box2D.NET 3.1.1.557 carries an ordinary fixed-rotation
dynamic capsule horizontally through frictional contact with an ordinary
translating kinematic box under the selected Nu-like scale and integration
settings.

The fixture directly mirrors relevant mappings inspected in Nu source commit
`064f7ae92a8506689cd91aff5e6804a375d6ef3d`: dynamic and kinematic body types,
capsule and box geometry, mass-to-density conversion, friction, restitution,
metre conversion, gravity, kinematic linear velocity, restitution threshold,
and four-substep integration. It does not execute Nu message handling, entity
transforms, publication phases, grounding APIs, lifetime, input, pause, jump,
cues, gameplay, or scene transitions.

## Frozen inputs and observations

- `H = 1 m`. Under Nu's default `Meter2d = 32`, this corresponds to 32 virtual
  pixels/H.
- Gravity is `(0, -9.80665) m/s^2`; the rider gravity scale is 1.
- The rider is an upright ordinary dynamic capsule: centre-line height `0.5H`,
  radius `0.25H`, total height `1H`, width `0.5H`, mass 1, fixed rotation,
  friction 0.5, restitution 0, and zero initial velocity.
- The support is an ordinary kinematic `4H x 0.25H` box centred at `(0, 0)`,
  with friction 0.5 and restitution 0. The rider starts centred with its lowest
  point at the platform top.
- The restitution threshold is `1/32 m/s`. Each logical update is `1/60 s` with
  four solver substeps.
- Both conditions settle for 15 completed stationary-platform updates
  (0.25 s). The next 120 completed updates form the 2 s observation. The
  stationary control retains zero platform velocity. The moving condition sets
  platform velocity to `(1, 0) m/s` once at the observation boundary.
- After each step, record both bodies' positions and velocities, their relative
  horizontal offset, and whether the rider has contact with the declared
  platform with at least one manifold point and whose normal toward the rider
  is within 45 degrees of world up.

At the pinned dependency commit,
[`b2Body_GetContactData`](https://github.com/ikpil/Box2D.NET/blob/d72ce440f6d409c3e15720a66b060051e7fdb87d/src/Box2D.NET/B2Bodies.cs#L471-L507)
already copies only contacts carrying `b2_contactTouchingFlag`.
[`B2Worlds`](https://github.com/ikpil/Box2D.NET/blob/d72ce440f6d409c3e15720a66b060051e7fdb87d/src/Box2D.NET/B2Worlds.cs#L652-L701)
sets that flag after asserting a positive manifold point count and clears it on
the stopped-touching transition before the zero-point state. The explicit
positive-point check in this fixture makes the observation rule independent of
that internal invariant and guards against accepting a stale or malformed
manifold.

## Frozen outcome rules

The stationary control is valid only when support exists at the settling and
final boundaries and relative horizontal drift is at most `0.01H`.

The moving condition is positive only when all of these hold:

1. support exists at the settling and final boundaries;
2. platform displacement is within `0.01H` of `2H`;
3. absolute change in rider-minus-platform horizontal offset is at most
   `0.05H`; and
4. support is observed for at least 114 of 120 observation updates.

The `0.05H` limit is an authored feasibility threshold chosen before execution.
It is not an externally validated definition of useful or perceptible platform
carrying. Reviewers should assess the reported continuous displacement, lag,
velocity, and support observations alongside the binary rule. The threshold
must not be widened after observing this result to turn the failure into a
pass.

If the stationary control is invalid, the moving result is inconclusive. A
valid control plus any failed moving criterion is an adverse result for this
bounded raw-dependency route. It is not a general Box2D.NET defect and does not
establish Nu-world, gameplay, or comparative behavior.
