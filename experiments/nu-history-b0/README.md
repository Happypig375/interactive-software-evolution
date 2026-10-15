# Functional Gaia B0 feasibility probe

This is an instrumented local feasibility experiment, not an agent task or a cost/benefit study. It uses actual Gaia initialization, MMCC Breakout, and Gaia's snapshot/undo path. Application code is unchanged. A small opt-in bridge is installed in an isolated Gaia source export; the external probe references Gaia and the application, so Gaia does not acquire a static Breakout dependency.

The [recorded result](result-receipt.json) contains the successful history/fresh checkpoint pair and all earlier runtime failures. GameplayTime 149, score 100, 29 bricks and the complete declared model/property values were restored after 11 actual drift Updates; fresh reconstruction and both negative controls passed. This is one feasibility witness at the exact scope below.

## Declared observation and controls

Both arms use functional, accompanied Gaia in Gameplay edit mode and static 60-update timing. Observation starts after the actual selection/StartPlaying sequence. No checkpoint model values are fabricated. The history arm advances until its first observed score-positive, fewer-than-30-bricks state, capped at 600 actual screen Update events. No input is injected; Left/Right input observations are counted. Randomly missing the paddle can exhaust this reachability attempt and is retained as such.

At the post-ImGui-postprocess hook, request halt and wait for the observed halted state before retaining the real world root. This is post-Update/content and pre-TimeUpdate. Nu applies the halt through a deferred tasklet after a later frame's updates; record the first eligible hit and the eventual halted checkpoint separately. After at least ten further actual screen Updates, request halt, again wait until it takes effect, call the real Gaia undo path, and inspect complete gameplay values and projected entity properties immediately after Gaia selection/camera reconciliation. Record the actual drift update count rather than claiming the request halted immediately. Observe again at the next halted boundary. Actual Update and TimeUpdate counts must remain unchanged across undo and the later halted boundary. A snapshot is accepted only if it is the same root at the top of Gaia's undo list.

The fresh arm starts a new process, waits for settled selection, and reconstructs the exact serialized checkpoint through the application's supported setter. An unchanged initial state and an intentionally omitted score must both fail complete equality and projection checks. The complete reconstruction must agree at its next halted content boundary. Immediate setter observations are retained separately. Bit encodings preserve all represented single-precision values; serialization round-trip equality is checked before a checkpoint is written. All scene entity names are compared, including absence of removed bricks; native/internal allocation IDs are excluded.

The current frame's render messages precede the hook. Immediate property equality is not a screenshot or displayed-frame check. The next halted observation checks another content/render-message boundary, but no actual framebuffer capture is claimed. Audio already emitted, RNG/input rewind, native trajectory continuation, reload, repair effectiveness and ordinary agent transport are outside B0.

The probe fails closed on wrong mode, phase/event drift, unexpected history, mismatched fields/projection, serialization loss, missing checkpoint or unhandled callback errors. A 1,200-callback limit complements the 600-Update reachability limit; use an external process deadline too. Keep each receipt directory new and retain every attempt. Do not select only successful runs.

The first two runs used a 180-second external deadline and timed out. Progress instrumentation in the second established advancing gameplay, so the third run declares a 600-second deadline before launch. The 600-Update and 1,200-callback limits, checkpoint rule and equality criteria remain unchanged. This accommodates the slow rendered environment; elapsed times are not comparative performance measurements. `run.py` supplies this deadline, captures stdout/stderr, records assembly hashes and terminates only its own process tree if the deadline expires.

The third run reached an eligible hit but the original observer incorrectly assumed `setAdvancing false` halted synchronously. The bridge rejected its still-advancing snapshot. Before the fourth run, the protocol was corrected to the explicit request/effective-halt phases above. The comparison still uses a reachable noninitial halted checkpoint and exact reconstruction of that checkpoint. The failed immediate-snapshot attempt remains in the execution record.

## Reproduction

Requires Windows, .NET SDK 10.0.302, a graphics/audio environment supported by Nu, and the pinned source/assets. Export Nu commit `064f7ae92a8506689cd91aff5e6804a375d6ef3d` to an isolated directory. Do not modify a working development checkout. The archive's Git commit comment is verified by the bridge installer; verify the full extracted archive before building.

```powershell
py -3.12 experiments/nu-history-b0/prepare.py <isolated-source> <pinned-git-archive.tar>
dotnet build experiments/nu-history-b0/Probe.fsproj -c Release -p:NuSource=<absolute-isolated-source> -p:SourceRevisionId=064f7ae92a8506689cd91aff5e6804a375d6ef3d
py -3.12 experiments/nu-history-b0/run.py history '<isolated-source>/Projects/Breakout Mmcc/bin/Release/net10.0/Breakout Mmcc.dll' <checkpoint-dir> <new-history-receipt-dir>
py -3.12 experiments/nu-history-b0/run.py fresh '<isolated-source>/Projects/Breakout Mmcc/bin/Release/net10.0/Breakout Mmcc.dll' <checkpoint-dir> <new-fresh-receipt-dir>
```

Set a package cache on the spacious drive if needed. The explicit SourceRevisionId is necessary when an exported source tree is nested inside a different Git repository: otherwise MSBuild can embed the enclosing repository's revision. Source-byte provenance and embedded product metadata are recorded separately. The probe writes its Gaia state only beside its own executable. It does not alter the user's usual Gaia settings.

Source modifications are limited to the generated bridge. Required Notice: Copyright (C) Bryan Edds. Gaia and Nu are licensed under the [Nu Game Engine Noncommercial License](https://github.com/bryanedds/Nu/blob/master/License.md). The [dated execution record](../../docs/nu-history-feasibility-2026-10-15.md) reports actual attempts, checks and remaining limitations.
