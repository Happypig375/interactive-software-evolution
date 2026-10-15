# Nu R04 actual-application diagnostic feasibility, 2026-10-15

## Result

Four builds of the actual pinned MMCC Breakout project reproduced the proposed source-site diagnostic contrast under its effective compiler policy. Both current-domain variants built successfully with 210 warnings and zero errors. After adding only `Paused` to `GameplayState`, the explicit `Playing | Quit` variant built successfully with one additional FS0025 warning at `Gameplay.fs(90,15)`; the terminal wildcard variant again built with 210 warnings and no FS0025.

This is source-integrated compiler evidence. No application was launched, no pause behavior was implemented, and the builds do not establish runtime equivalence, diagnostic attention, maintenance benefit, or the practical value of pause.

## Frozen construction

The tracked [pre-execution contract](../experiments/nu-r04-application-diagnostics/pre-execution-contract.md) was written before the first build. It fixes Nu `064f7ae92a8506689cd91aff5e6804a375d6ef3d`, archive SHA-256 `EB0AA77197DE1971D79AA0657C2AF5CF33B99BA8302A24BA44F3306CCA4BF92B`, original `Gameplay.fs` SHA-256 `571E2A5CE3F0630972F2FBE4E9A6A3C376BCF4D1A74589D14C882B2EE0DB1423`, .NET SDK 10.0.302, the four exact transformations, predictions, and falsifiers.

The [source record](../experiments/nu-r04-application-diagnostics/source-provenance.md) binds the existing union at lines 9-11 and the terminal update clause at lines 167-168. The complete deltas are in [variant-transformations.patch](../experiments/nu-r04-application-diagnostics/variant-transformations.patch). The baseline wildcard changes only `| Playing | Quit -> gameplay` to `| _ -> gameplay`. Each successor adds only `| Paused` to the union; it adds no pause trigger, update behavior, content, time, lifecycle, project, asset, or dependency edit.

The portable [runner](../experiments/nu-r04-application-diagnostics/run-probe.ps1) verifies the archive and all four complete-file hashes, extracts one fresh private source tree, regenerates every variant from the verified original, and gives every full graph build a distinct artifacts path. The four builds share only a task-private package cache. It uses Release, `AnyCpu`, `net10.0`, and the unchanged checked-in warning properties. It clears `PostBuildEvent` because the original refinement command assumes project-local `bin` while this compiler-only run redirects every compiled output outside the source tree. The full project and package graph still builds; no compiler or warning property is overridden.

The effective evaluated properties were `WarningLevel=5`, `WarnOn=FS1182`, `NoWarn=FS0009;FS0052;FS1178;FS3391;FS3536;FS3560`, `WarningsAsErrors=FS0026;FS0049;FS3239;3239;`, and `TreatWarningsAsErrors=false`. The toolchain was F# compiler product `15.2.302-servicing.26329.109+35b593bebfcba58f8e78298cef14c2761f5d86c6`, `fsc.dll` SHA-256 `3DB18554E1D49181C6A184EE1AD4C8C0C5DB457DE7F3CCE2AF5A098497B79A68`, and FSharp.Core 10.1.302. All 33 resolved packages and versions were identical across variants and are retained in [resolved-packages.txt](../experiments/nu-r04-application-diagnostics/resolved-packages.txt).

## Build observations

The tracked [result receipt](../experiments/nu-r04-application-diagnostics/original-results.tsv) records the final execution:

| Variant | Build | MSBuild warnings/errors | Selected FS0025 | Assembly version | Assembly SHA-256 |
| --- | --- | ---: | ---: | --- | --- |
| baseline explicit | success | 210 / 0 | 0 | 1.0.0.0 | `B9C719FEE9715D7B4B6F0815EADA03EEF172EAB60163AFA6AAAB110B19EEE42C` |
| baseline wildcard | success | 210 / 0 | 0 | 1.0.0.0 | `0F4B4F6E7D2210433CB60F7C31DF3D8F73D14DF04A539335E8DE581890C2A1DD` |
| Paused explicit | success | 211 / 0 | 1 warning | 1.0.0.0 | `B5F475DFA194E258893929827BC17809CFFBABF44B0D80520C2C63C837ED8581` |
| Paused wildcard | success | 210 / 0 | 0 | 1.0.0.0 | `F03C5B670C751F000352F2A166A0B52E5F17C8007A542111E51D7AED3155BFD6` |

The FS0025 text identifies `Paused` as an uncovered example. It is warning-only and does not block the project build. MSBuild prints every warning in the build body and again in its summary, so that diagnostic has two raw log lines and one canonical source-location/message. The same accounting is preserved for every diagnostic in [diagnostic-counts.tsv](../experiments/nu-r04-application-diagnostics/diagnostic-counts.tsv): the three variants without FS0025 each report 133 NU1901 and 77 NU1902 package-vulnerability warnings; Paused explicit adds one FS0025. The private logs retain all 420 or 422 raw diagnostic lines without filtering, plus 150 or 151 canonical location/message lines.

Each assembly hash belongs to the exact output of the reported fresh build. The hashes differ among source variants, and the first retained attempt produced different hashes in a different artifacts path. Neither source identity nor assembly hashes are treated as behavioral equivalence evidence.

The final run restored the extracted `Gameplay.fs` to its original hash, preserved the project file hash `817DF993B65AAE04557913CDA8D02B32AB5B8A32C6863C3769AA8BEF0B55F158`, and compared complete pre/post manifests of all 3,240 extracted files with zero difference. Exact transformed sources, project assets, commands, logs, assemblies, and manifests remain privately under `.artifacts/r04-application-diagnostics-20261015/run-02/`. The pre-existing R03 source and build evidence were not read as build outputs, modified, or rebuilt.

## Attempts and reproduction

Both complete four-build attempts are retained and summarized in [attempts.tsv](../experiments/nu-r04-application-diagnostics/attempts.tsv). Run 01 completed all builds but exited 1 because its receipt logic treated MSBuild's `1>` node prefix and the unprefixed summary repetition as two unique FS0025 diagnostics. The repair removes only that presentation prefix before deduplication. It did not alter source generation, build commands, predictions, or warning policy. Fresh run 02 executed the final runner and passed all four predictions.

From the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File experiments/nu-r04-application-diagnostics/run-probe.ps1 `
    -NuArchive '.artifacts/r03-feasibility-20261015/nu-064f7ae.tar' `
    -OutputRoot '.artifacts/r04-application-diagnostics-20261015/reproduction-01'
```

The destination must be fresh. The [README](../experiments/nu-r04-application-diagnostics/README.md) describes retained outputs and boundaries.

## Disposition and limits

The actual project confirms the narrow adapted-probe prediction: at the selected match, adding an otherwise unhandled `Paused` case creates one warning-only FS0025 in the explicit arm and none in the wildcard arm. It also confirms that the existing dependency graph has substantial unrelated warnings, so later information-delivery work must preserve the exact returned stream rather than assuming a clean compiler channel.

The successor is intentionally incomplete and unreachable. The compiler result says nothing about board visibility, gameplay-time freezing, resume/quit triggers, fresh restart, or whether identity is the correct whole-application behavior. The separate source audit shows that the wildcard is legitimate for paused simulation updates while content and time require coordinated compiler-silent changes. Runtime construction and its trigger/effect oracle remain separate work.

Because `experiments/nu-r04-application-diagnostics/` is a new unrecognized path, change-scoped CI classifies this publication conservatively as **full**. Local validation covers the experiment runner and receipts; no local full historical suite or runtime is claimed.
