# R04 build and execution receipt

This tracked receipt summarizes the complete retained history. Exact arm-level hashes and raw artifact identities are in [result-receipt.json](result-receipt.json); ignored sources, binaries, logs, and traces remain under `.artifacts/r04-pause-runtime-20261015/`.

## Identity

- Nu commit: `064f7ae92a8506689cd91aff5e6804a375d6ef3d`
- archive SHA-256: `EB0AA77197DE1971D79AA0657C2AF5CF33B99BA8302A24BA44F3306CCA4BF92B`
- B0 symbol SHA-256: `FFEE72D91C6E4A32B650D45E9ADDD9E02E179163D0C8BBAAA8CDDB9C92BC783A`
- SDK: 10.0.302
- `fsc.dll`: version 15.2.302.0, SHA-256 `3DB18554E1D49181C6A184EE1AD4C8C0C5DB457DE7F3CCE2AF5A098497B79A68`
- SDK `FSharp.Core.dll`: assembly version 10.1.0.0, SHA-256 `E53A949A32BC698D23BBFB96EBF6D6EEB05E8EA66A1719B22CF5005E6DFDC831`
- final prepare receipt: `12E3DCB46EA2B70E1E6F090A218EBDC6C26F9734714BA52681B21244C4595537`
- final nine-graph build receipt: `C4C35AACB8CD22E37B480C9E3658342863D4A3D03DC417E90A1B9E8BA38C1971`
- parent preflight verification: `9A3F6C87B0774EDAAF417A11BFC359100756AA15007903EAFBB3C6A6C45398B9`
- amended probe-only build receipt: `5337D666036012C5D265B26342EEF015FF11253567221547A167EBB3188FEB9A`

The nine variants and five exact fault patches are recorded in [variant-manifest.md](variant-manifest.md). Complete-file comparisons established one selected-clause difference inside each explicit/wildcard pair, identical common pause edits inside the completed pair, and exactly one declared behavior fault in each sensitivity variant. Gaia and audio instrumentation were byte-identical across arms.

The final full-build probe sources were `Common.fs` `0C8B7249...E9643`, `BaselineProbe.fs` `AC78B6A8...16725`, and `PauseProbe.fs` `0FBA3A20...6BA15`. After the retained runtime reconstruction failure, the prospective common-clear amendment changed only the two probe entry points and contract: final tracked baseline `CAA56557...A5211`, pause `AC9D0B79...E5846`, and contract `2EC8D027...FA3DE`; Common remained byte-identical. Historical and successor hashes are preserved in the private amendment receipts.

## Full builds

All nine Release/net10.0 project/probe graphs built under the checked-in compiler, warning, and package policy. Each emitted 334 warnings, zero errors, and only NU1608, NU1901, and NU1902. The build driver did not override warning or package properties. The resolved set contains the same 35 package name/version entries in [resolved-packages.txt](resolved-packages.txt); no package was upgraded.

| Arm | Exit | Warnings / errors | Probe SHA-256 | Application SHA-256 |
| --- | ---: | ---: | --- | --- |
| baseline explicit | 0 | 334 / 0 | `CE846768...31430` | `71AF2756...589C4` |
| baseline wildcard | 0 | 334 / 0 | `0B055471...EE352` | `33ECE5D1...E2804` |
| pause explicit | 0 | 334 / 0 | `92683D50...418DB` | `C2E16277...2A2CC` |
| pause wildcard | 0 | 334 / 0 | `4932B628...C9722` | `CF79E81D...00F09` |
| missing-toggle fault | 0 | 334 / 0 | `67F2E05C...D9522` | `3A8F4A8A...7BAD8` |
| hidden-content fault | 0 | 334 / 0 | `CCFA072B...E45F2` | `A5858758...55962` |
| advancing-time fault | 0 | 334 / 0 | `E19CFACE...5D51C` | `C6C7F277...8ED33` |
| reset-resume fault | 0 | 334 / 0 | `59B1786E...0DAB8` | `E34707A6...A0E2D` |
| stale-quit fault | 0 | 334 / 0 | `FD6D49BA...3B9FB` | `2EE5207C...2A6F7` |

Different fresh output roots produced different Nu/Gaia binaries even for byte-identical corresponding sources, so no binary-equality inference is made from source equality. All listed managed assemblies report version 1.0.0.0.

## Probe-only successor

The reconstruction amendment did not rebuild any accepted application, Nu, or Gaia graph. Each amended probe was compiled directly against its own frozen arm output. The first build-harness attempt successfully compiled baseline-explicit, then stopped because the verifier resolved preflight-relative receipt paths from the repository root. Its log and output are retained. The corrected second attempt built all nine probes with zero warnings and zero errors.

Before every launch, the accepted wrapper verified the complete frozen runtime manifest, the externally loaded application SHA-256, B0, 600-second deadline, and original host files. It then invoked the amended assembly with `dotnet exec --depsfile Probe.deps.json --runtimeconfig Probe.runtimeconfig.json`. `Probe.deps.json` contains 44 libraries and one target group. The only added runtime files were the five `AmendedProbe` outputs. Three previously launched frozen hosts contained `Nu.Gaia.State.txt`; six did not. The probes overwrite that state file before `selectNuPlugin`, and the difference was recorded rather than normalized away.

## Retained preparation attempts

1. `preflight-01` stopped before build: the content-gate transform matched two anchors. The matcher was narrowed to the scene-content comment and condition.
2. `preflight-02` built all four original dependency graphs, then every copied probe failed with one FS0001 caused by missing separators in a multiline receipt list. Each unfiltered log retained 334 warnings and one error.
3. `preflight-03` built all four references successfully, 334 warnings and zero errors each. Independent review then found scientific gaps: randomized `Gameplay.empty` equality, incomplete fresh invariants, missing exact entity-name checks, insufficient failure observations and deltas, and no actual source-fault variants.
4. `preflight-04` froze the reviewed source but stopped before build on those gaps.
5. `preflight-05` stopped during extraction after `Common.fs` changed, preventing unequal probe bytes from being copied across arms.
6. `preflight-06` prepared nine variants. Baseline-explicit then ended with 334 warnings and three FS0072 errors because `positionKey` lacked its `Vector3` annotation; the sequential build was stopped.
7. `preflight-07` stopped before build when source review proved a generated RGB component can round to exactly `1.0f`; three strict upper bounds were changed to inclusive bounds.
8. `preflight-08` is the accepted nine-arm build above. Separate baseline and pause harness checks before it each passed with 244 warnings and zero errors.

No failed attempt was replaced or deleted.

## Runtime history and final outcomes

The first explicit and wildcard baseline runs both passed the four fixtures. Their complete nonconfiguration observations matched exactly and were independently replayed. The first pause-explicit run then stopped at `B0 projection mismatch` before a click or update. An observation-only probe rerun stopped at the same gate and recorded B0 bricks `@477` and `@478` with correct B0 colors but retained fresh-grid positions. Pinned keyed reconciliation supports a prior generated-key collision explanation, but initial names were not logged; the collision remains an inference.

The prospective correction first sets the one existing initial model to `Quit`, observes a halted post-content boundary with zero Gameplay Update/TimeUpdate events, the same selected/idling screen, exact derived model, and absent GameplayScene, then installs unchanged B0. This is reconstruction alignment work. It does not show that direct `SetGameplay` generally preserves or replaces same-name identities.

All four amended references passed once, without timeout or exception:

| Arm | Probe exit | Callbacks | Updates / TimeUpdates | Outcome |
| --- | ---: | ---: | ---: | --- |
| baseline explicit | 0 | 14 | 4 / 4 | four fixtures passed |
| baseline wildcard | 0 | 14 | 4 / 4 | four fixtures passed |
| pause explicit | 0 | 22 | 12 / 12 | full pause/lifecycle oracle passed |
| pause wildcard | 0 | 22 | 12 / 12 | full pause/lifecycle oracle passed |

The 13 fixed baseline records were exactly equal between clauses after excluding configuration and independently generated clear values. The 22 fixed pause records through the resumed one-pair boundary were also exactly equal. Both later lifecycles independently satisfied the prospective randomized vacant/fresh invariants. In each pause arm, ten pairs retained time 149 and all represented B0 values while 20 handlers recorded positive advancement; resume produced the exact one-pair time-150 model; click totals were Pause/Resume 3, Quit 1, TitlePlay 1. Only the three positive-control audio requests were observed.

Every frozen source fault was run once and detected at its declared first gate. Probe exit 1 is expected detection; every engine exited 0 and no attempt timed out:

| Fault | Required evidence reached | First failing gate |
| --- | --- | --- |
| missing toggle | Pause count 1; model remained Playing | `pause-reached` |
| hidden content | Pause count 1; model Paused; scene absent | `pause-projection` |
| advancing time | first advancing TimeUpdate/Update pair; time 150 | `pause-frozen-model` |
| reset resume | ten frozen pairs; Pause count 2; fresh time-0 model | `resume-retained` |
| stale Quit | Pause count 3; Quit count 1; Title selected/idling; B0-like model retained | `quit-reset` |

These controls show that the frozen oracle detects the five authored faults in this execution. They do not estimate real fault prevalence or maintenance benefit.
