# R04 diagnostic feasibility probe: pre-execution contract

Written before any probe build or execution on 2026-10-15. This is the original contract copied from the preserved private attempt; its `.artifacts` paths describe that execution.

## Scope and fixed inputs

- Source identity: Nu `064f7ae92a8506689cd91aff5e6804a375d6ef3d`, copied at `../r03-feasibility-20261015/source`; its `source-integrity.json` reports 3,240 checked files and no mismatch.
- Selected site: `Projects/Breakout Mmcc/Gameplay.fs`, union at lines 9-11 and `Gameplay.update` match at lines 89-168.
- Exact current terminal clause: `| Playing | Quit -> gameplay`. The compared current-domain clause is `| _ -> gameplay`; the guarded `Playing` branch is shared.
- Toolchain: installed .NET SDK 10.0.302 and its bundled F# compiler. The runner will record `dotnet --info`, the F# Interactive banner, resolved project properties and the resolved `FSharp.Core` version.
- Source policy in every case: target `net10.0`, warning level 5, no FS0025 suppression, and only FS0026, FS0049 and FS3239 promoted to errors, matching the selected Nu project's explicit policy. FS0025 is predicted to remain a warning.
- Isolation: all derived source, `obj`, `bin`, logs, CLI home and package cache belong to `.artifacts/r04-diagnostics-20261015`. The pinned Nu source tree is read-only input and will not be built or modified.

## Cases, observations and predictions

1. `baseline`: define only `Playing` and `Quit`; compare the explicit terminal clause with the wildcard across both states and active/inactive guard inputs. Prediction: equal returned records for the finite matrix, no FS0025, exit 0.
2. `successor-distinct-explicit`: add `ReadyToServe` but leave `Playing | Quit` as the terminal clause. Prediction: FS0025 warning, build succeeds under the frozen policy, and reaching the added case produces a match failure.
3. `successor-distinct-catchall`: add `ReadyToServe` while retaining the wildcard. Declared local oracle: this case must move the paddle one step while preserving the remaining fields. Prediction: no FS0025, build succeeds, but the oracle fails because identity is incorrect.
4. `successor-distinct-explicit-wrong`: enumerate `ReadyToServe` with an identity body. Prediction: no FS0025 and build succeeds, but the same oracle fails. This is the explicit check that coverage does not entail correct behavior.
5. `successor-fallback-explicit`: add `Paused` but leave `Playing | Quit` as the terminal clause. Declared local oracle: identity is correct for the added case. Prediction: FS0025 warning, build succeeds, and reaching `Paused` produces a match failure until a coverage repair is made.
6. `successor-fallback-catchall`: add `Paused` under the wildcard. Prediction: no FS0025, build succeeds, the identity oracle passes, exit 0. This is the legitimate fallback case.

Every build output, diagnostic code/severity, process exit and oracle observation is retained, including predicted adverse results. A mismatch against a prediction is evidence, not a reason to replace the case.

## Falsifiers and limits

- Current-domain equivalence is falsified if any matrix row returns unequal records or either variant raises.
- The warning-only prediction is falsified if FS0025 is absent from an unchanged explicit successor, promoted to an error, or the build otherwise fails because of the probe.
- Diagnostic silence is falsified if either wildcard successor emits FS0025.
- The legitimate-fallback prediction is falsified if `Paused` under the wildcard changes the record or fails.
- The probe establishes only compiler and small pure-function behavior under this fixed toolchain. It does not establish whole-Nu runtime equivalence, temporal/lifecycle correctness, agent attention, maintenance benefit or representative task coverage.
