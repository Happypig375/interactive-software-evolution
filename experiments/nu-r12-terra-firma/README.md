# R12 Terra Firma load/save/reopen feasibility

This package observes the existing pinned Terra Firma scene before the
proposed shared-tint/local-roughness comparison. It preserves original
application code privately and adds an external loop observer. It does not
invoke propagation, perform a revision, run task-solving agents or estimate
authoring benefit. [PROTOCOL.md](PROTOCOL.md) owns the assigned phases and
comparison; the [reuse contract](../../docs/nu-reuse-and-authoring-contract-2026-10-11.md#2026-10-18-existing-terra-firma-family-and-next-revision-case)
owns the practical case and remaining questions.

One corrected native L0/L1 pair passes the declared checks. The first L0 had
invalid Symbol formatting despite a completed process/save; that attempt remains
retained and unscored. After the three-call correction, four literal formatter
checks, focused review and a new compiled-source seal, the corrected pair
preserved the declared 197-entity correspondence, 166 links, 11 histories and
selected properties of 32 palms/four Villas. Seventeen synthetic checker
controls passed; interrupted work and failures remain separately recorded.
See [execution-receipt.json](execution-receipt.json) and the
[execution record](../../docs/nu-terra-firma-reopen-feasibility-2026-10-18.md).

## Inputs and stages

The source archive, existing pipeline host and accepted R05 runtime remain
private prerequisites. Their hashes are checked by `run.py`; the two hosts
are deliberately distinct. This package neither rebuilds Nu nor silently
substitutes available DLLs. Original copyrighted scene/assets/source and
derived full descriptors stay under `.artifacts/` and are not published.

Use a new output path for every attempt. These example `repro` paths are not
the retained executed attempts. On Windows, from the repository root:

```powershell
python experiments/nu-r12-terra-firma/run.py assets `
  --archive .artifacts/r03-feasibility-20261015/nu-064f7ae.tar `
  --pipeline .artifacts/r03-feasibility-20261015/source/Nu/Nu.Pipe/bin/Release/net10.0 `
  --output .artifacts/r12-propagation-20261018/terra-assets-repro

python experiments/nu-r12-terra-firma/run.py build `
  --assets .artifacts/r12-propagation-20261018/terra-assets-repro `
  --host .artifacts/r05-events-20261015/bin/Release/net10.0 `
  --output .artifacts/r12-propagation-20261018/terra-build-repro
```

Before the native application stage, review actual preparation diagnostics,
verify all eight original source units and the observer against portable-PDB
checksums/PE identity, and accept the frozen compiled output and full harness.
The runner's `ready_for_parent_review` field is a technical readiness flag,
not that review's outcome. The application uses the R05 depsfile for its
verified dependency set and its own generated runtimeconfig for GC/TieredPGO.

```powershell
python experiments/nu-r12-terra-firma/run.py run `
  --build .artifacts/r12-propagation-20261018/terra-build-repro `
  --output .artifacts/r12-propagation-20261018/terra-L0-repro

python experiments/nu-r12-terra-firma/run.py run `
  --build .artifacts/r12-propagation-20261018/terra-build-repro `
  --predecessor .artifacts/r12-propagation-20261018/terra-L0-repro `
  --output .artifacts/r12-propagation-20261018/terra-L1-repro

python experiments/nu-r12-terra-firma/compare.py `
  --l0 .artifacts/r12-propagation-20261018/terra-L0-repro `
  --l1 .artifacts/r12-propagation-20261018/terra-L1-repro `
  --output .artifacts/r12-propagation-20261018/terra-comparison-repro.json
```

L1 requires a complete L0 observation/save, including an adverse completed
one. It uses L0's actual saved bytes and a fresh application copy. No earlier
reference save replaces a failed predecessor. Missing required observations,
wrong mode or provenance, and data errors remain invalid/incomplete; a
correctly observed changed configuration/history is adverse. A single-arm
checker result is explicitly scoped `L0_only` and is not a completed pair.

## Verification boundary

`check_controls.py --scene <original Scene.nugroup> --output <new private path>`
constructs clearly marked synthetic data and checks missing entities, changed
source history, wrong mode, missing observations, wrong predecessor, delayed
B, changed save content, numeric tolerance and nonfinite values, exact
Size/Offset changes, earlier Scene-exists observations, underlying process
failure, effective GC and changed sealed observations. It never loads Nu.
The original scene is used only to establish the fixed name/history structure
for those synthetic controls.

Asset preparation accounts for all 248 outputs, including 120 transformed
images. It checks copied bytes, transformed container signatures and read-only
attributes, and retains host tracing and the checksumless PDB document limit.
Those checks do not verify decoded visual appearance. Native observations use
a hidden real SDL/OpenGL world, functional/accompanied/halted configuration,
original custom dispatchers and two successive post-process captures. The
197 original descriptors and generated character visuals remain separate.
Neither a successful process nor repository CI validates rendering, input,
native resource restoration or comparative benefit.
