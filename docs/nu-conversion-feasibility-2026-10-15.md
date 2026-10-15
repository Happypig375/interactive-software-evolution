# Prime 11.5.1 conversion and reward-mapping feasibility

**Date:** 2026-10-15

**Repository head observed before construction:** `49ff4d9b42a89b074f3892585f88a6a1e618d533`

**Scope:** isolated execution of pinned Prime conversion APIs and a bounded
application mapping; no Nu/Gaia live-reload execution

## Decision addressed

The [R10 live-edit contract](nu-live-edit-contract-2026-10-11.md#application-mapping-for-the-conditional-schema-extension)
requires a V0-to-V1 first installation to retain the seven existing Gameplay
fields and introduce `BrickReward = 200`. Later V1 reloads must retain the
configured reward, including a legitimate zero and a nondefault value such as
75. A new round may initialize reward 200. Unknown source editions must remain
explicitly unresolved.

This check asks whether the pinned Prime 11.5.1 conversion behavior and a
source-edition-aware symbol mapping can realize those value correspondences in
an isolated executable. The tracked
[reproduction package](../experiments/nu-r10-conversion/README.md) contains the
[pre-execution expectations and falsifiers](../experiments/nu-r10-conversion/pre-execution-contract.md),
source, exact package lock and a small
[publication-check receipt](../experiments/nu-r10-conversion/result-receipt.json).
Full attempt logs and build products remain ignored. Existing
`.artifacts/r03-feasibility-20261015/` source/build state was not read for
execution or modified.

## Pinned runtime and source correspondence

The probe targeted .NET 8 and was built by SDK 10.0.302. Its lock file resolves
Prime exactly to 11.5.1, FSharp.Core 10.1.302, Csv 2.0.93 and FParsec 1.1.1.
The loaded assembly reported:

| Identity | Observed value |
| --- | --- |
| Assembly / file version | `11.5.1.0` / `11.5.1.0` |
| Informational version | `11.5.1+4026f3156865d536d0c4d36f1dc361485df8117a` |
| Original loaded copy (ignored) | `.artifacts/r10-conversion-20261015/bin/Release/net8.0/Prime.dll` |
| Publication-check loaded copy (excluded build output) | `experiments/nu-r10-conversion/bin/Release/net8.0/Prime.dll` |
| Loaded DLL SHA-256 | `61A67158910296D92E22CF4C4D7EC9EDB194C55AB00098534850E281E370C787` |
| Cached package DLL SHA-256 | `61A67158910296D92E22CF4C4D7EC9EDB194C55AB00098534850E281E370C787` |
| Cached `.nupkg` SHA-256 | `29B453CD6076EA73E8A075067897C764C9EC52C42B8F5BB88166A47F90DCA865` |

The informational version agrees with the Source Link commit already bound to
the package. The executable calls the ordinary `valueToSymbol` and
`symbolToValue` wrappers reconstructed in the live-edit contract. The relevant
source routes are expanded-record serialization and name lookup, unexpanded
record positional reconstruction with type defaults, and union-case lookup by
name. Nu's inspected model getter serializes the old object, attempts symbolic
deserialization, and reaches `TryGetFallbackModel` only after a deserialization
exception. The probe's small exception wrapper mirrors that ordering for one
failure case; it is not Nu runtime code.

The V0/V1 outer records reproduce Gameplay's seven named fields and expansion
policy. Nested paddle, ball and brick records remain unexpanded, and the bricks
remain a `Map<string, Brick>`. Discriminating integer geometry/color values
replace Nu's Vector3/Color values so this probe isolates generic
correspondence. It does not establish conversion of every actual MMCC value or
reference.

## Fixed witness and observed values

The noninitial V0 witness was fixed before execution: gameplay time 941,
Playing, paddle position/size 110/64, ball position/size/speed/direction
73/8/3/-1, brick `brick-A` at 101/64/color 1122867, brick `brick-C` at
303/32/color 4478310, score 700 and three lives. Brick identities and values,
not only their count, were compared exactly.

| Case | Actual observation | Contract disposition |
| --- | --- | --- |
| Raw V0 to reordered expanded V1 | All seven fields retained; `BrickReward = 0`; fallback false; no exception | Prime conversion succeeded but violated first-installation reward 200. This is the consequential adverse result. |
| Explicit V0 installation | A V0-provenance branch added a named reward-200 symbol before V1 deserialization; all seven fields and both brick records retained; reward 200 | Isolated value mapping feasible when provenance is available before defaulting. |
| Repeated V1 conversion | V1A to V1B to V1C retained the full witness and reward 200 | Repeat value correspondence passed for two conversions. |
| Deliberate zero and 75 | Each value survived V1A to V1B to V1C with the full witness unchanged; the V1 edition branch also retained zero | Legitimate zero was not treated as missed migration, and later configuration was not overwritten with 200. |
| Explicit fresh V1 round | Time 0, score 0, five lives, reward 200 and brick key `fresh-brick` | Correct as a separate lifecycle initialization; these values would be a preservation failure during installation. |
| Nested paddle field reorder | Source position 110 became destination `Size = 110`; source size 64 became destination `Position = 64` | Conversion was type-valid but semantically swapped the fields, confirming the positional hazard. |
| Active case rename | Converting `Playing` to a union with cases `Active | Quit` raised `Prime.ConversionException`; the local wrapper marked fallback and returned fresh score 0, five lives, reward 200 and `fresh-brick` | Confirms failure and reset are observably different from successful zero-default conversion. It does not show Nu executed this fallback. |
| Unknown edition | Returned `Error "unknown source edition: unregistered"`; no conversion or reset | Preserves an explicit unresolved outcome without inferring edition from reward zero. |

All eight predeclared case checks returned true and the final process exited
zero. The Release build completed with zero warnings and zero errors. Earlier
attempts remain in the artifact ledger: one malformed restore argument, one
compile failure caused by ambiguous F# record labels, and one successful probe
calculation followed by JSON formatting failure. None produced or erased a
contrary conversion observation; the repairs changed CLI syntax, type
annotations and output formatting while retaining the package, witness,
mapping and falsifiers.

## What this changes and what remains open

The source-derived defaulting prediction is now executable evidence for the
exact packaged Prime assembly: adding the integer field can convert cleanly to
zero and bypass an exception-only fallback. Therefore a clean conversion or a
running application would not establish the intended V0-to-V1 reward mapping.
The probe also supplies a concrete, provenance-aware symbolic mapping that
returns the declared isolated values and preserves zero on later editions.

This is conversion/mapping feasibility only. The successful explicit mapping
is not an identified supported insertion point in Nu, and it does not validate
Gaia reload, FSI/plugin binding, screen synchronization, pre-installation
witness access, actual MMCC Vector3/Color/reference conversion, ongoing-game
behavior, effects, atomic recovery, or the restart/reconstruction comparator.
It also does not show that successfully converted state has the intended
application meaning: the nested positional case demonstrates the opposite.
Those boundaries remain prerequisites for any R10 live-reload or benefit
claim.
