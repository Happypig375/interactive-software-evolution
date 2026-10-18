# Nu R12 public propagation probe

This package exercises the actual public `World.propagateEntityStructure`
operation on one Button/Text family in a functional, accompanied, halted Nu
stub world. Read [PROTOCOL.md](PROTOCOL.md) before execution and the
[result record](../../docs/nu-propagation-feasibility-2026-10-18.md) for its
observations and limits. [result-receipt.json](result-receipt.json) binds the
first accepted build and single runtime attempt.

Requirements: Windows, Python 3.11 or later, .NET SDK 10.0.302, and the retained
R03/R05 runtime directory with Nu source pin
`064f7ae92a8506689cd91aff5e6804a375d6ef3d`. The input `Nu.dll` must hash to
`e96cd61d188c689f7e39e2670b4d8582e26b9ea2dc95e1a15056891b7c99cd68`.
The published source does not contain these generated binaries. A rebuild at
another path/toolchain is not automatically this sealed assembly; establish
its provenance and declare a new execution identity before changing the guard.

From the repository root, use an unused output path:

```powershell
python experiments/nu-r12-propagation/run_probe.py build `
  --host .artifacts/r05-events-20261015/bin/Release/net10.0 `
  --output .artifacts/r12-propagation-reproduction/build-01
```

The build does not rebuild or write the supplied Nu host. It snapshots the
probe inputs and hashes the complete existing host, records the command and
unfiltered logs, then verifies that every host file was copied byte-for-byte.
The output manifest seals the probe DLL/PDB and dependency files. Review the
source, build receipt and manifest before the separately invoked execution:

```powershell
python experiments/nu-r12-propagation/run_probe.py run `
  --build .artifacts/r12-propagation-reproduction/build-01 `
  --output .artifacts/r12-propagation-reproduction/runtime-01
```

Execution rechecks the sealed build and uses its retained R05 dependency graph
and runtime configuration with `dotnet exec` to host the new probe assembly.
It has a 120-second deadline and an isolated working directory. The probe
hashes the actually loaded Nu assembly before world initialization, emits
complete bootstrap/pre-call/post-call observations and serialized descriptors,
and cleans up in `finally`. Raw stdout/stderr, actual command, process result,
post-run binary manifest and compact receipt are retained. Existing attempt
directories are rejected rather than overwritten. The runner does not enforce
a cumulative five-failure counter; the maintainer must honor the project's
return rule across all preserved attempts.

Exit 0 is the completed declared mechanism check; exit 1 is a completed call
with an adverse semantic result; exit 2 is invalid/incomplete preparation or
observation. Read the receipt and exact failed phase, rather than interpreting
any process exit as a whole-application result. A valid adverse result is not
an instruction to repair the engine or replace the fixture.

This check does not exercise a game loop, Gaia, button input, rendering,
save/reopen, ordinary agent access or authoring effort. Stub setup can still
call native libraries, including SDL polling during serialization. The root
ID change is recorded descriptively; live resources, pending work and external
effects are outside the preservation claim.
