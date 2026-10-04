# Blueprint compilation, observation and type-change contracts

Main-agent documentation inspection, **2026-10-04 HKT**. This checks proposed mechanisms behind S257/S259's development observations and S260's runtime explanation, and supplies a concrete alternative for Nu's evolution claims. It adds **no full-paper or independent-study count**. No compiler, engine, project or debugger session ran.

## Sources, version boundary and coverage

Native collection `PKLXQNEE` and library URL/title searches preceded selected reading. Four new records were created as the collection grew from 287 to 291 parents. The initial compiler registration helper had a syntax error before any write; it was corrected before reading the compiler body. Discovery searches exposed current-version excerpts and release-note fragments, which remain screening coverage.

| Selected official page, requested version 5.3 | Native parent / note | Actual reading |
| --- | --- | --- |
| [Compiler overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/compiler-overview-for-blueprints-visual-scripting-in-unreal-engine?application_version=5.3) | `5QYM4EYB` / `FGYEL9AX` | All 110 indexed lines, including all nine compilation stages. Decorative header image not inspected; no engine-source verification. |
| [Blueprint Debugger](https://dev.epicgames.com/documentation/en-us/unreal-engine/blueprint-debugger-in-unreal-engine?application_version=5.3) | `NS8RWB4C` / `UFRRJ3VU` | All 107 indexed lines; three original illustrations inspected: pin-value tooltip, factorial call stack and execution trace. Other illustrations not inspected. |
| [5.3 release notes](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5.3-release-notes?application_version=5.3) | `W9CQQWLS` / `ZCKK5QU3` | Selected lines 1004–1016 and 3503–3591, plus returned discovery/find context. Type-change illustration inspected. The 6,800-line release is not fully read. |
| [Debugging example](https://dev.epicgames.com/documentation/en-us/unreal-engine/blueprint-debugging-example-in-unreal-engine?application_version=5.3) | `Q6SXNU9Y` / `8B66I3PH` | Requested 5.3 body inaccessible. The unversioned search result identifies 5.8 and is discovery only; it does not fill this edition gap. |

The indexed titles identify **5.3**, but these revisable pages are not a historical snapshot of **5.3.2** or a verified shipped source/binary. Ordinary HTML requests returned 403 for all four. The compiler/debugger article text and selected release sections are preserved as explicitly labelled **tool-indexed text snapshots**, not original HTML. The four linked original PNGs succeeded by ordinary public requests after web-tool cache misses. Native attachment readback verifies their identities; all bodies/images remain outside Git.

| Saved source object | Native attachment | Bytes | SHA-256 |
| --- | --- | --- | --- |
| Compiler indexed text | `4GQD6E3T` | 8,382 | `a637abe55ea3bd352342a26d93e79c9c0b90b3ee9fb3708e0327175224a843b2` |
| Debugger indexed text | `TEV5WNA5` | 9,654 | `c2f823a3462801d1c0474594bf280d8920c40e9acb4970701b4c61f6f5e97e15` |
| Release selected indexed text | `8ET9K6PV` | 7,503 | `7795b51b5a2f36231f4f6eff72cfe43ab2dc8432b86dc08265dd810bb623c51a` |
| Pin-value illustration | `CN36MJZT` | 93,788 | `b7411953dd9902766c8b1a251dfaf6a6635f296f6e5ac45110e57bf16e0deb11` |
| Factorial call stack | `M5TYZ5X3` | 60,704 | `d2f8d8a3441ab2ac27d920ba9b4e28290001f8237bd495f306cd4b5d0e89247e` |
| Execution trace | `26J3U7K8` | 50,775 | `9ca87f5f11401114d36038f65169349f2cebf12c0d6a1636f4791ae8a7eb714d` |
| Type-change illustration | `NGEGSSX4` | 172,811 | `6340001e9b7893d34e02925d37e76cf91d33414d22713004524a5c1875d7fd0b` |

## Documented mechanisms

**Compilation and replacement.** The overview describes expansion of event/function graphs, scheduling and dependency analysis, pruning unused nodes, node-handler statements and backend emission. It identifies VM bytecode as one output and C++-like output as a debugging facility. That supports a concrete transformation account, not an assumption that visual graphs simply become an equivalent optimized native program. It supplies no causal estimate of dispatch, copying or representation cost in S260.

The generated class is reused in place. Old defaults are copied into a new class-default object through tagged serialization, with property-name consistency a stated condition. Changed instances are replaced and copied using `CopyPropertiesForUnrelatedObjects`. This is a documented reconstruction procedure; it does not establish preservation of renamed fields, suspended work, external effects or application invariants. The overview mentions final checks without enumerating a complete diagnostic contract. These are documentation claims, not verification of the corresponding 5.3.2 implementation.

**Observation during execution.** The debugger article describes breakpoints and stepping in PIE/SIE, pin watches, instance filtering, cross-language call stacks and a recent-node trace. Pin values reflect the most recent execution of their node; unexecuted nodes provide no value, including variable nodes not yet demanded. Macros are represented inside their caller rather than separate stack frames. The illustrations show an inspected projectile object, five recursive factorial frames, and recent events with an instance/time label. They do not demonstrate restoration or re-execution of earlier state. These tools make some behavior observable, but observing a path is not checking every behavioral or temporal obligation. Neither the article nor these screenshots measures a maintenance benefit.

**Adaptation after a type change.** The selected release text describes automatic cast insertion when a suitable conversion exists between old/new Blueprint-visible property types, accompanied by notes. The illustration inserts **Truncate** between a floating-point variable and the changed input. This demonstrates one compatibility repair with an explicit conversion. Whether the new numeric behavior is intended is a separate application question; no error in the illustration is alleged.

The same selected release material reports fixes involving variable removal, archetypes, delegate signatures, batched compilation dependencies and sparse class data, and describes a limited data-asset merge facility. These are vendor release claims at a bounded version, not independently reproduced failures, prevalence estimates or proof of a general migration guarantee. They make version, asset type and edit kind material to the comparison.

## Consequence for the research claim

The useful positive account is now more concrete: graph-level inspection, instance reconstruction and some type-change adaptation already exist in a mainstream game toolchain. They are credible alternatives to include when characterizing Nu, alongside S99's live model tables, S102/S103's explicit schema transformations, S105/S107's temporal methods and S225's host/reset contract. Nu's novelty cannot rest on generic availability of live editing or visual feedback.

For a stronger claim, compare the **permitted edit, mapping of old state to new state, pending work/effects, diagnostic coverage and observed successful change**. A conversion can restore connectivity while changing values; a class/property copy can reconstruct objects without proving a temporal contract; a displayed value can be stale relative to unexecuted logic. These are distinct obligations, not interchangeable correctness signals. This is a synthesis from the documented boundaries, not an experiment or proof that Nu fails them.

S257/S259's favorable task outcomes remain evidence at their original scope. The documentation makes a proposed tooling explanation plausible without isolating it from representation, experience or task allocation. S260's compiler hypothesis is now grounded in a stated pipeline, while its measured energy difference remains mechanistically unidentified. No new empirical effect follows from documentation availability.

The selected compiler/debugger text gap is resolved. Exact shipped-source correspondence, the 5.3 example page and uninspected illustrations remain narrower coverage gaps; neither more generic documentation nor another search result can establish Nu's net benefit. The next consequential route is **Phylogenix (10.1145/3715002)** for practical asset/engine integration, while the independent Unity-build comparison, contemporary practice and temporal/state/type-evolution dependencies remain available. All construction and experimental holds remain.
