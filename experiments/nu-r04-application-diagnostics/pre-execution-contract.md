# Pre-execution contract

Frozen before the first application build on 2026-10-15.

## Question and scope

Compile four variants of the actual pinned MMCC Breakout project to test whether the source-site FS0025 contrast observed in the pure adaptation also appears under the real project graph and checked-in compiler policy:

1. current `Playing | Quit` with the original terminal enumeration;
2. current `Playing | Quit` with the equivalent terminal wildcard;
3. the original enumeration after adding only `Paused` to `GameplayState`; and
4. the wildcard after adding only `Paused` to `GameplayState`.

This is a compiler feasibility check. It does not execute Breakout, establish application equivalence, implement pause, expose a diagnostic to an agent, or measure maintenance value.

## Frozen source and toolchain

- Nu commit: `064f7ae92a8506689cd91aff5e6804a375d6ef3d`.
- Input archive SHA-256: `EB0AA77197DE1971D79AA0657C2AF5CF33B99BA8302A24BA44F3306CCA4BF92B`.
- Original `Projects/Breakout Mmcc/Gameplay.fs` SHA-256: `571E2A5CE3F0630972F2FBE4E9A6A3C376BCF4D1A74589D14C882B2EE0DB1423`.
- Project: `Projects/Breakout Mmcc/Breakout Mmcc.fsproj`, Release, `AnyCpu`, `net10.0`.
- .NET SDK: 10.0.302. The compiler product version and produced assembly identity will be recorded from the actual run.
- Preserve the project files, `WarningLevel=5`, `WarnOn=FS1182`, six explicit suppressions, and `WarningsAsErrors=FS0026;FS0049;FS3239;$(WarningsAsErrors)`. Do not add a warning suppression, promotion, or package upgrade.
- Use one fresh archive extraction in the experiment-private output. Each variant is regenerated from the verified original text. Each build uses its own artifacts path and the same task-private NuGet package cache. This safely reuses downloaded immutable packages but not compiled outputs.
- Set `PostBuildEvent` empty on the command line. The original post-build command assumes project-local `bin`; the experiment redirects all build outputs outside the source tree and does not need asset refinement for a compiler-only observation. This is a declared build-path adaptation, not a source or warning-policy edit.

## Exact variants

The original terminal clause is:

```fsharp
| Playing | Quit -> gameplay
```

The wildcard replacement is:

```fsharp
| _ -> gameplay
```

The successor edit adds only this union line after `Quit`:

```fsharp
| Paused
```

No pause trigger, update branch, content gate, time guard, lifecycle code, asset, project, or dependency is changed. The runner requires exactly one match for each transformation and verifies the following complete-file hashes before each build:

| Variant | Expected `Gameplay.fs` SHA-256 |
| --- | --- |
| baseline-explicit | `571E2A5CE3F0630972F2FBE4E9A6A3C376BCF4D1A74589D14C882B2EE0DB1423` |
| baseline-wildcard | `5FF5CB277FAD9359405EE0341C70837319221EC710F2178E632675A856E38566` |
| paused-explicit | `8FD9F60DB811FF5E791F8B2FBB2EDEE6C11F732F98EBF67F33C30C31F78FCDC6` |
| paused-wildcard | `9268684F8024D98E0C8BC6E802B12D1F87B21EE8E7C6CD11770A2780C9708630` |

## Predictions and pass conditions

| Variant | Predicted build | Predicted unique selected-source FS0025 |
| --- | --- | ---: |
| baseline-explicit | success | 0 |
| baseline-wildcard | success | 0 |
| paused-explicit | success; warning only | 1 |
| paused-wildcard | success | 0 |

A build passes its narrow prediction only if it exits zero and has the predicted number of unique FS0025 diagnostics located in the selected `Gameplay.fs`. The run must retain full stdout/stderr and count every warning and error code, including dependency, vulnerability, SDK, and duplicate summary lines. Any additional FS0025 is recorded rather than filtered.

The comparison is falsified or limited if extraction identity fails; a transformation is not unique; a nonselected source file changes; the effective warning properties differ; a build does not compile the intended `Gameplay.fs`; a baseline emits selected-source FS0025; `Paused` plus enumeration does not emit it; the wildcard emits it; FS0025 is promoted to an error; any build otherwise fails; or logs/assemblies cannot be assigned to exact variant hashes.

Assembly version and SHA-256 are evidence of the produced inputs, not semantic equivalence. Equal source pins do not imply equal binaries, and differing binaries do not establish behavioral difference.
