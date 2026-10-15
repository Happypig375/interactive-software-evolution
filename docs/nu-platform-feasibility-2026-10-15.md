# R01 ordinary-platform dependency feasibility

**Status before execution, 2026-10-15:** protocol frozen; no fixture result had
been observed when the inputs and decision rule below were written. This probe
is authorized local construction under the 2026-10-15 continuation in
[PLAN](../PLAN.md). It addresses one dependency-level boundary from the
[2D platform contract](nu-platform-contract-2026-10-11.md); it is not a Nu
scene, a Godot comparison, or an R01 benefit study.

## Question and implementation boundary

Does the exact managed dependency declared by pinned Nu, Box2D.NET 3.1.1.557,
carry an ordinary fixed-rotation dynamic capsule horizontally through frictional
contact with an ordinary translating kinematic box, under the selected Nu-like
scale and integration settings?

The fixture calls Box2D.NET directly. It mirrors the relevant inspected
`Box2dNetPhysicsEngine` mappings: dynamic and kinematic body definitions,
capsule and box geometry, mass-to-density conversion, default friction and
restitution, metre conversion, world gravity, kinematic linear velocity,
restitution threshold and four-substep world integration. It does not execute
Nu's physics-message handling, transform application, event publication,
grounding API, entity lifetime, input, pause, jump, cues, gameplay code, or
scene transitions. A positive result can justify constructing a Nu-level
observer and scene; it cannot establish those higher-level obligations.

The mappings were checked read-only against the isolated Nu source at
`064f7ae92a8506689cd91aff5e6804a375d6ef3d`; this probe did not build or modify
that source tree.

The local package is version 3.1.1.557. Before execution, its NuGet archive
SHA-256 was
`4B1F60A808723A7E6B7A5BE67F24891CADBCE5BB5E49C3EADFE57FD8ADB430CD`,
and the selected `lib/net8.0/Box2D.NET.dll` SHA-256 was
`E5DCFE35346DA43E1E476E056721C7D5B6E617A13F5C4736C3B17A6E2A5FE5BF`.
The package manifest binds the edition to repository commit
`d72ce440f6d409c3e15720a66b060051e7fdb87d`. Package acquisition and assembly
identity do not establish that a full Nu process resolves or loads this file.

## Frozen inputs and observation phase

All distances below are Box2D metres with `H = 1 m`. This is equivalent to the
contract's virtual scale of 32 pixels/H under Nu's default `Meter2d = 32`.

- World gravity is `(0, -9.80665) m/s^2`; the rider gravity scale is 1.
- The upright capsule has centre-line height `0.5H`, radius `0.25H`, total
  height `1H`, width `0.5H`, mass 1, fixed rotation, friction 0.5,
  restitution 0, zero initial velocity, and ordinary dynamic body type.
- The platform is a `4H x 0.25H` box centred at `(0, 0)`, with friction 0.5,
  restitution 0, and ordinary kinematic body type. The rider begins exactly
  above its centre, with its lowest point at the platform top.
- The world restitution threshold is `1/32 m/s`, matching the wrapper's
  one-virtual-pixel/s setting. Each logical update calls `b2World_Step` with
  `1/60 s` and four substeps, matching the contract and Nu default. The wrapper's
  positive-delta clamp does not alter `1/60 s`.
- Both conditions first settle for 15 completed updates (0.25 s) with the
  platform stationary. At the boundary after update 15, record body positions,
  velocities and capsule-to-platform contact. Then observe 120 completed
  updates (2 s). The stationary control keeps platform velocity 0; the moving
  condition sets it to `(1, 0) m/s` once at that boundary.
- After every completed step, obtain the rider's current contact data. Count
  support only when the other shape is the declared platform and the contact
  manifold has a positive point count and the normal toward the rider lies
  within 45 degrees of world up, matching the inspected ordinary-body grounding
  orientation test. Record both bodies' positions and velocities, support
  status, and the rider-minus-platform horizontal offset. This observation
  reads solver state after the step and does not add carrying logic.

The exact dependency implementation's
[`b2Body_GetContactData`](https://github.com/ikpil/Box2D.NET/blob/d72ce440f6d409c3e15720a66b060051e7fdb87d/src/Box2D.NET/B2Bodies.cs#L471-L507)
copies only contacts with `b2_contactTouchingFlag`. Its
[`B2Worlds` transition](https://github.com/ikpil/Box2D.NET/blob/d72ce440f6d409c3e15720a66b060051e7fdb87d/src/Box2D.NET/B2Worlds.cs#L652-L701)
sets that flag after asserting `manifold.pointCount > 0` and clears it on the
stopped-touching transition before the zero-point state. Thus the first two
attempts' returned contacts were already constrained by that primary
implementation. The tracked fixture now also tests positive point count
explicitly, making the public observation criterion self-contained.

The reviewable fixture is tracked in
[`experiments/nu-r01-platform`](../experiments/nu-r01-platform/README.md). It
accepts an explicit output directory and emits a complete per-update CSV and a
JSON summary there. The original and reproduction traces remain under
`.artifacts/r01-platform-20261015/`; generated `obj/`, `bin/`, package files and
raw traces are not published.

## Prospectively declared outcomes

The stationary control validates this narrow setup only if support exists at
the settling boundary and final boundary and its absolute change in relative
horizontal offset over the 2 s observation is at most `0.01H`.

The moving condition is a positive dependency-level carrying result only if:

1. support exists at the settling boundary and final boundary;
2. the platform displacement is within `0.01H` of `2H`;
3. the absolute change in rider-minus-platform horizontal offset is at most
   `0.05H`; and
4. support is observed after at least 114 of the 120 completed observation
   updates (95%).

If the stationary control is invalid, the moving condition is inconclusive.
If the control is valid but any moving criterion fails, the ordinary raw
dependency route fails this bounded carrying probe under the frozen inputs.
The tolerance will not be widened after observing results. An API/setup failure
is recorded as an attempt rather than interpreted as absent carrying; five
failures at one unchanged gate stop the probe.

## Limited interpretation

Even a positive result shows only that ordinary solver contact can transfer
enough horizontal motion under this one flat, fixed-gravity case. It does not
show phase-correct Nu world state, an identifiable public support relation,
movement relative to support, once-only departure velocity, jump acceptance,
pause/resume, removal cleanup, exit isolation, cue counts, arbitrary gravity,
slopes, stairs, dedicated pogo-character behavior, practical usability, or
comparative benefit. Those require their own prospective construction and
observation boundaries. A raw result also does not replace R02's Blaze Vector
pair or establish Godot parity.

## Results

The package setup succeeded from the existing cache. The first API/build gate
succeeded with zero warnings and zero errors. The original fixture run, the
portable reproduction and the point-count-hardened reproduction all exited
successfully and loaded the copied `net8.0` assembly with SHA-256
`E5DCFE35346DA43E1E476E056721C7D5B6E617A13F5C4736C3B17A6E2A5FE5BF`.
Its informational version is
`1.0.0+d72ce440f6d409c3e15720a66b060051e7fdb87d`, matching the package manifest's
repository commit. All three runs' stationary and moving trace hashes match
byte for byte. Adding an explicit positive-manifold-point predicate therefore
did not change any support observation or outcome.

| Prospectively declared observation | Stationary | Moving |
| --- | ---: | ---: |
| Support at settling boundary | yes | yes |
| Support at final boundary | yes | yes |
| Supported observation updates | 120/120 | 120/120 |
| Platform displacement | `0H` | `1.9999988H` |
| Rider displacement | `0H` | `1.9000956H` |
| Absolute relative horizontal drift | `0H` | `0.099903226H` |
| Final rider/platform horizontal velocity | `0 / 0 H/s` | `1 / 1 H/s` |
| Frozen condition result | pass | **fail** |

The stationary control is valid. In the moving condition, the rider remained
in qualifying support contact throughout and reached the platform's velocity,
but friction accelerated it over the first 12 observation updates. The relative
offset reached about `-0.0999H` and remained there. This exceeds the frozen
`0.05H` carrying tolerance; it was not widened after observation. Therefore
`dependencyCarryPositive` is **false** for this case.

The `0.05H` value is an authored feasibility threshold, not an externally
validated definition of useful or perceptible carrying. The continuous result
is more informative than the binary label: support remained present for all
120 updates, the platform moved `1.9999988H`, the rider moved `1.9000956H`, and
both ended at `1H/s`, leaving a `-0.099903226H` rider-minus-platform offset.

This is a precise adverse mechanism result, not evidence that Box2D.NET cannot
support platform gameplay. It shows that ordinary contact alone, with an
instantaneous platform start and the selected default friction, does not meet
this contract's positional carry bound. A later Nu scene would need either a
prospectively justified motion profile/tolerance or explicit application/body
logic to satisfy the selected behavior. Such a revision would be a new design
and result, not a relabeling of this failed condition.

The reviewable reproduction source, frozen protocol and small result receipt
are tracked in [`experiments/nu-r01-platform`](../experiments/nu-r01-platform/README.md).
The complete generated artifacts remain private local evidence:

- original `results/summary.json` (SHA-256
  `022556F8D9E3F50B2971E5676A2A8C9F43A1510F226ECC2CE5F9464D16E5B4CA`);
- reproduced `reproduction-attempt-2/summary.json` (SHA-256
  `7F8E05FB48046D1F50AEDA5E8CFFA4D666F2B366A4E17E6B8E473019C7537A96`);
- hardened `reproduction-attempt-3/summary.json` (the same SHA-256
  `7F8E05FB48046D1F50AEDA5E8CFFA4D666F2B366A4E17E6B8E473019C7537A96`);
- each moving trace, 135 completed updates (SHA-256
  `E715CEC5B7AF4383571CB48CC4B5E96C369EA8A3D133FD62D3E85B54A000E61E`);
  and
- each stationary trace, 135 completed updates (SHA-256
  `FA73315E34A007FF16705430108D95164BC93E09FBF545BAFFE7862A37B21FAD`).

The traces include the 15 settling updates and 120 observation updates. No
tolerance revision, new physics variant, Nu scene, jump, pause, removal, exit,
cue, Godot, performance, or benefit attempt is claimed.

The tracked runner now rejects a nonempty output directory before creating a
physics world. A validation invocation against the completed attempt-3
directory exited with that rejection, and all three attempt-3 file hashes were
unchanged afterward. This preserves completed and partial attempts instead of
silently overwriting their files.
