# R02 standalone lifecycle feasibility

This package builds two arm-specific probes against one fresh extraction of Nu
`064f7ae92a8506689cd91aff5e6804a375d6ef3d`. It leaves Nu, MMCC Breakout,
ImSim Breakout, both plugins, and all assets unchanged. The probes use public
`World.runPlus`, stable trace-only subscriptions, and synthetic publication of
the applications' existing Play and Quit ClickEvents.

The frozen comparison, phase bounds, observations, outcomes, and limits are in
[`pre-execution-contract.md`](pre-execution-contract.md). The secondary
fresh-initializer diagnostic is frozen separately in
[`initializer-diagnostic-addendum.md`](initializer-diagnostic-addendum.md).
A pass establishes only bounded standalone lifecycle/observer feasibility. It
does not validate physical input, pause behavior, audio, framebuffer output,
cross-package equivalence, or practical benefit.

From the repository root, prepare and build with the pinned SDK:

```powershell
python experiments/nu-r02-standalone-lifecycle/prepare.py `
  .artifacts/r03-feasibility-20261015/nu-064f7ae.tar `
  <new-preflight-directory>

python experiments/nu-r02-standalone-lifecycle/build.py `
  <new-preflight-directory>
```

After source and build review, the two assigned launches are performed once in
fixed order and with the exact deadline:

```powershell
python experiments/nu-r02-standalone-lifecycle/run.py `
  <accepted-preflight-directory> mmcc `
  .artifacts/r02-standalone-lifecycle-20261015/runtime-mmcc-01 --timeout 600 `
  --accept-build-sha256 <reviewed-build-receipt-sha256>

python experiments/nu-r02-standalone-lifecycle/run.py `
  <accepted-preflight-directory> imsim `
  .artifacts/r02-standalone-lifecycle-20261015/runtime-imsim-01 --timeout 600 `
  --accept-build-sha256 <reviewed-build-receipt-sha256>
```

Preparation extracts the archive once, verifies exact application-tree
manifests, and copies the tracked probe inputs into private arm directories.
Builds are sequential. Each application project produces its ordinary host and
assets; four named probe files are then added to that host. The build receipt
binds the full host manifests and rechecks every original extracted input.
Runtime outputs are append-only evidence directories and are not committed.

## Recorded result (2026-10-15)

Both assigned runs passed the frozen primary lifecycle oracle and the separate
exact-initializer diagnostic. MMCC completed with 485 pre/post callbacks and
ImSim with 487; both engines returned zero, neither timed out, and both owned
processes were terminal without cleanup errors. Each arm observed two Play
clicks, one Quit click, two Gameplay Select generations, stable Title, and a
fresh Playing session. The three sampled active positions changed while the
sampled Left, Right, and P keys were up.

The MMCC exact seam observed both generations at Playing, GameplayTime 0,
score 0, five lives, and 30 bricks. The ImSim seam observed the same common
scalars, generation-bound absent Scenes before both Play actions, present
Scenes under selected Gameplay in both callbacks, and distinct Scene IDs 270
and 1171.

Observed MMCC Play/Quit/Play action-to-idling increments were 95/95/95.
Observed ImSim increments were 95/97/95. The two ImSim Play observations are
one callback earlier than the source-derived nominal +96 prediction frozen in
the contract; they remain within the fixed 100-callback bound, so the oracle
was not revised. MMCC application requests first appeared immediately after
publication, while ImSim requests first appeared at later post-process
entries, consistent with the contract's absence of a same-callback equality
requirement.

The final SDK-10.0.302 build checked 3,240 original source inputs with zero
mismatches. Both 349-file host closures built with 270 warnings, zero errors,
and diagnostic codes `NU1901` and `NU1902` only. Earlier evidence is retained:
one setup-manifest failure, one superseded preparation, a 71/73-error full
compile, a two-error-per-arm probe repair, a passing probe-only repair, and a
passing build whose assembly-name metadata was unavailable. The final accepted
build receipt SHA-256 is
`a60b2b7fb244da88f9b0a38bd09d4555259a508a5aafc71503e804ac511eba84`.

[`result-receipt.json`](result-receipt.json) records the full attempt history,
source and host closure counts, assembly identities, action/request boundaries,
outcomes, and exact identities for both private process receipts, logs, result
files, and traces. The raw evidence remains under
`.artifacts/r02-standalone-lifecycle-20261015/runtime-mmcc-01` and
`runtime-imsim-01`. Each native run added `Log.txt` and `imgui.ini` to its
verified 349-file pre-launch host; the receipt records their identities and
confirms that no pre-launch manifest file changed.

These passes are bounded evidence for synthetic existing-ClickEvent lifecycle
and observer feasibility in the two unchanged pinned applications. They do not
test physical pointer input, SDL delivery, full input/replay behavior, audio,
framebuffer output, pause behavior, cross-package causality or equivalence,
practical value, maintenance benefit, or standalone agent access. The
post-Select scalar witness is post-step; the secondary exact callbacks are
pinned source seams rather than a general initialization guarantee. The
executed ImSim stable-Title predicate checked absence of every retained-brick
and retained-life derived entity, but the compact stable-Title trace projection
does not enumerate those individual booleans.
