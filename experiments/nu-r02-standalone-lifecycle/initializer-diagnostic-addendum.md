# Secondary exact-initializer diagnostic addendum

Frozen prospectively on 2026-10-15 before the first build. This read-only
diagnostic follows the source review in private record
`fresh-initializer-observation-seam.md`, SHA-256
`543f619d8df5449b3e9e31f2c6948c1087ceecb5701032177d2482bdb9a88bf5`.
It does not change the primary lifecycle oracle, its limits, or its outcome.
The independent source review accepting this seam has SHA-256
`0fdf6679709d0e02919c0c6fe3f12e989853e221a3348af0b93ba3bd4fdfce1d`.

The MMCC probe subscribes in the first pre-process to
`Game.Handle.PostSelectEvent`, returns `Cascade`, and accepts only payload
`Some Simulants.Gameplay`. After the application's synchronous Select handler
has installed `Gameplay.initial` and before the first selected gameplay update,
the callback records the counted logical Select generation, GameplayTime,
Playing/score/lives/bricks, selected Gameplay confirmation, outer-entry
ordinal, and clocks. It makes no transition-state assertion inside this
callback.

The ImSim probe subscribes in the first pre-process, with `Game` as subscriber,
to the derived `Game/Gameplay/Scene.RegisterEvent` and returns `Cascade`.
Immediately before each Play publication it records that Scene is absent. After
a counted Gameplay Select, the new Scene registration occurs after the four
screen scalar setters and before Scene children, paddle logic, or ball creation.
The callback records the Select generation, Playing/score/lives/bricks,
selected Gameplay, `Scene.GetExists`, its generation-bound pre-Play absence,
new Group.Id, outer-entry ordinal, and clocks. Both generations must be
captured, each must bind to the immediately preceding absent-Scene record, and
the two Group.Id values must differ.

Neither callback publishes an action, changes phase, writes application state,
or throws an observation exception into the application. A complete
noninitial scalar record, a present pre-Play ImSim Scene, or reused ImSim Scene
Id fails only this secondary claim. A query exception, unavailable value, or a
missing expected exact callback is secondary missingness. These outcomes remain
alongside the unchanged first-postProcess scalar gates and can neither relabel
nor replace the primary result. The seam is supported only for the pinned
applications' recreate-on-reentry lifetime and is not a general ImSim rule or a
later pause-reference requirement.
