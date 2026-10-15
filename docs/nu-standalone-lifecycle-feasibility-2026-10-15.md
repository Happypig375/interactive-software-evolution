# Nu R02 standalone lifecycle feasibility, 2026-10-15

## Result and decision

Both unchanged Breakout applications passed their one assigned standalone
lifecycle run: natural Splash to Title, Play, active Gameplay, Quit, stable
Title, and a second fresh Play. The separately frozen exact-initializer
diagnostics also passed for both logical gameplay generations in each arm.
No runtime was retried, replaced, extended, or excluded. Both processes exited
zero without timeout or cleanup error.

This establishes a common bounded lifecycle and usable public observation
points for the pinned applications. It advances R02 beyond the earlier
[source contract](nu-source-contracts-and-scenarios-2026-10-11.md) and supplies
the standalone prerequisite for the [pause/exit case](nu-pause-exit-contract-2026-10-11.md).
It does not establish pause correctness, package equivalence, an isolated
architecture effect, ordinary candidate access, or maintenance benefit.

The applications use Nu `064f7ae92a8506689cd91aff5e6804a375d6ef3d`, ordinary
imperative/unaccompanied/advancing standalone configuration, StaticFrameRate
60, and TickDeltaAveraging=false. All were read back at runtime. The probes
reproduce the original viewport construction: virtual resolution 640×360,
display scalar 2, and window/geometry bounds 1280×720. They use public
`World.runPlus` callbacks without changing either application, engine,
plugin, or asset input.

## Observed lifecycle

The following values are completed `postProcess` callback ordinals, not elapsed
seconds or a cross-arm performance measure. Both arms reached their first
idling Title at callback 189, within the frozen startup bound of 200.

| Observed boundary | MMCC | ImSim |
| --- | ---: | ---: |
| First Play published | 189 | 189 |
| First selected/idling Gameplay | 284 | 284 |
| Quit published after three active samples | 287 | 287 |
| Returned selected/idling Title | 382 | 384 |
| Second Play after three Title-hold callbacks | 385 | 387 |
| Second selected/idling Gameplay | 480 | 482 |
| Result after five fresh-session callbacks | 485 | 487 |

Each arm recorded exactly two Play ClickEvents, one Quit ClickEvent, two
Gameplay Select/IncomingFinish pairs, one Gameplay
Deselecting/OutgoingFinish pair, and the required two Title entry/exit pairs.
Every first post-Select scalar witness was Playing, score 0, lives 5, and 30
bricks. Across the three active samples, each arm's ball position changed and
the sampled Left, Right, and P keys were all up. The second session remained
Playing without an unsolicited Quit or Title transition for all five assigned
callbacks.

The traces expose different request ownership. MMCC's Gameplay request and
Quit/Title requests were observable immediately after ClickEvent publication
in the same callback. ImSim's Gameplay request appeared in the following
callback; its Quit property appeared one callback after publication and its
top-level Title request one callback later. The observer did not impose
synchronous consumption on ImSim.

All three MMCC action-to-idling intervals were 95 callbacks. ImSim's two Play
intervals were also 95, while Quit took 97. The frozen nominal source
prediction was **96** for ImSim Play; the observed 95 is retained as a
prediction discrepancy. The nominal values were never equality gates. All
intervals satisfy the unchanged 100-callback bound; neither that bound nor the
frozen contract was revised after execution.

The narrow source explanation is that the same next ImSim
[`Breakout.Process`](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20ImSim/Breakout.fs#L45)
call consumes Play, sets Gameplay, and declares the selected Gameplay screen.
[`beginScreenPlus10`](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu/World/WorldModule2.fs#L422)
starts the outgoing transition immediately. The old arithmetic inserted an
extra callback between request consumption and transition start.

The actual cleanup obligations differ. At stable Title, MMCC exposed its
vacant model: time 0, Quit, score 0, lives 0, zero bricks, and no Gameplay
scene. ImSim retained its unselected Gameplay screen and screen properties
(Quit, score 0, lives 5, and 30 retained brick entries), while its Scene,
Paddle, Ball, Quit button, and retained brick/life entities were absent.
Retained configuration/data and live scene lifetime are distinct; imposing
MMCC's property reset on ImSim would reject its valid package behavior.
The ImSim raw projection records the group and named Paddle/Ball/Quit absence.
Per-brick and per-life absence is supported by the executed, independently
reviewed predicate; its individual boolean results were not enumerated in the
compact trace and cannot be replayed independently from those rows.

## Exact-initializer diagnostic

The [prospective addendum](../experiments/nu-r02-standalone-lifecycle/initializer-diagnostic-addendum.md)
uses two application-specific public seams, independently of the primary
post-Select scalar check. Both were installed before any action and returned
`Cascade` without changing application state.

MMCC's `Game.PostSelectEvent` observed each completed synchronous initializer
before the first selected gameplay update. Both generations had GameplayTime
0, Playing, score 0, lives 5, and 30 bricks. The captures occurred at outer
entries 252 and 448. Selection was Gameplay in both captures; transition
state was deliberately not an initializer predicate because its assignment
occurs separately. The first ordinary post-Select projection can already
contain ball movement, so its scalar success alone is insufficient evidence
of a pre-update observation.

ImSim's `Game/Gameplay/Scene.RegisterEvent` observed the four screen scalars
after their initialization and before scene children were declared. Both
captures had Playing, score 0, lives 5, and 30 bricks, with Gameplay selected
and Scene present. Each was bound to the immediately preceding pre-Play
observation that Scene was absent. The captures occurred at outer entries 252
and 450, with distinct Scene IDs 270 and 1171. This supports the pinned
recreate-on-reentry lifetime; it is not a general initializer hook for an
implementation that retains its scene.

These are exact observations of the declared scalar boundary, not a complete
pre-physics/native-world snapshot. The diagnostic would retain its own
failure or missingness independently of the primary outcome.

## Construction and preserved attempts

The [package](../experiments/nu-r02-standalone-lifecycle/README.md),
[frozen contract](../experiments/nu-r02-standalone-lifecycle/pre-execution-contract.md),
and [compact receipt](../experiments/nu-r02-standalone-lifecycle/result-receipt.json)
bind source, preparation, build, review, execution, and raw observation
identities. The original archive SHA-256 is
`eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b`.
An independent full archive comparison and subsequent build checks covered
all 3,240 original source inputs with no mismatch. Each final application host
had 349 files; exact path, size, and hash closure was checked independently
before release and by the runner before its assigned launch.

Preparation and probe mistakes remain part of the construction history:

| Attempt | Disposition |
| --- | --- |
| Preflight 01 | Rejected a hardcoded application aggregate based on a different serialization recipe. Full per-file archive comparison established unchanged inputs before the canonical manifest correction. No build or launch. |
| Preflight 02 | Prepared successfully, then superseded before build for documented probe/script corrections. |
| Preflight 03 | Both full builds failed in probe code: 71/73 errors and 272 warnings. Original application/engine inputs remained unchanged. |
| Probe repair 01 | Both probe-only compiles failed; logs and inputs retained. |
| Probe repair 02 | Both probe-only compiles passed against the verified earlier dependency graph. No native launch. |
| Preflight 04 | Both fresh builds passed, but assembly-name receipt inspection failed on spaced paths. The incomplete receipt was retained and not released for execution. |
| Preflight 05 | Both fresh builds passed with complete assembly identities and strengthened receipt/host guards. This is the only runtime source. |

The final builds used SDK 10.0.302. Each reported 270 warnings, zero errors,
and only NU1901/NU1902 diagnostic codes; dependency versions and warning policy
were preserved. Both running processes reported runtime 10.0.10. The accepted
build receipt SHA-256 is
`a60b2b7fb244da88f9b0a38bd09d4555259a508a5aafc71503e804ac511eba84`.
Wrong-deadline and wrong-build-hash checks rejected execution before creating
an output directory. Independent AI review and the maintainer accepted the
fixed source/build before the first launch; this is not human scientific
approval.

MMCC completed in 88.266 process-wall seconds and ImSim in 78.719, each below
the unchanged external 600-second deadline and internal 600-post-callback cap.
These durations include startup, tracing, rendering, and termination. The
single sequential runs were not designed to estimate a performance difference.
All preparatory and runtime records remain locally preserved; source archives,
binaries, full traces, and logs are not added to public Git.

## Interpretation and next work

The probe publishes the existing entity ClickEvents. It exercises the real
application subscriptions and lifecycle, while bypassing SDL delivery,
pointer hit testing, ButtonFacet Down/Up, ImGui capture, and click sound.
No framebuffer, native audio, held-key replay, collision equivalence, or
physical-input claim follows. The existing ImSim quit/advancement workaround
remains present; C-exit is an adaptation motivated by the historical issue,
not a newly reproduced unfixed Breakout defect.

Next establish the supported input and effective-pause observations for the
prepared pause/exit references. A programmatically queued SDL key event can
exercise an event-subscribing reference, but does not set SDL's held-key state;
it cannot by itself evaluate every valid polling-based implementation. Preserve
that access boundary, normal UI effects, quit precedence, fixed observation
phases, and separate reference-construction costs. The current lifecycle
success supplies a prerequisite, not the missing pause implementation or its
benefit. New source/runner paths conservatively select full change-scoped CI.
