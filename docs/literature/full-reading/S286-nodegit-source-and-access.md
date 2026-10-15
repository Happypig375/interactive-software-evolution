# S286 — NodeGit: inferred graph identity, measured snapshot merging, and the live-state boundary

**Work:** Eduardo Rinaldi, Davide Sforza and Fabio Pellacini, *NodeGit: Diffing and Merging Node Graphs*, ACM Transactions on Graphics 42(6), article 265, pp. 1–12, December 2023. [DOI 10.1145/3618343](https://doi.org/10.1145/3618343).

**Disposition:** the complete primary article closes the former body/evaluation access gap. NodeGit supplies a concrete alternative to stable-ID versioning: it infers correspondence between typed procedural node-graph snapshots, computes property/reference changes, and combines changes from two descendants of a common ancestor. The reported evaluation is favorable for correspondence recovery, curated non-conflicting merges, and sub-second diff cost on 16 Blender programs. It does not evaluate conflict repair, human collaboration, undo/redo, total workflow cost, or preservation of a running program. The separately inspected public implementation substantially corresponds to the paper, while exposing a graph-cost normalization difference and narrower adapter behavior; it was not established as the exact measured build.

## Identity and actual coverage

Native Zotero parent **`BQG8UT5U`**, version **5886**, is a `journalArticle` in collection **`PKLXQNEE`** with the exact title, three authors, DOI, date, journal, volume 42, issue 6, article/page range 1–12, and article 265 identity. Imported PDF **`JUFDJX8H`**, version **6669**, is its direct child. The file `BQG8UT5U.pdf` is **21,967,350 bytes**, SHA256 **`3df0cd5b0bb6c22532f3e392017e95fa06c44b91b0f70ea81cd4153311e1e598`**, PDF 1.5, and 12 pages. Its title page, author list, DOI, running headers and ACM reference line match the parent record.

The acquisition reconciliation labels the edition “ACM conference paper.” The primary object itself is the December 2023 **ACM Transactions on Graphics journal article**, and the native `journalArticle` type is correct. Any SIGGRAPH Asia presentation context does not convert the verified bibliographic edition into a proceedings paper.

All **12 pages** and the complete 42-item reference list were read. Text extraction returned 87,599 characters across all pages. Original 144 dpi renders of all 12 pages were inspected, covering Figures 1–9, Tables 1–3, Algorithms 1–4, Equations 1–2, the colored edit encodings, graph diagrams, render comparisons and all table cells. The paper has no appendix. It refers to supplemental visualizations for all Table 1 programs, but no supplement, raw randomized edits, expected-match files, build, compiler configuration or complete evaluation archive was acquired. No code, Blender session, test, merge or reproduction was run.

The verified PDF, extraction and renders remain in ignored `.artifacts/s286-reading-20261015/`. This is one complete reading of the selected published work, not an independent replication.

## Representation and graph identity

The paper represents a procedural program as a collection of graphs. Each graph contains typed nodes with two broad property classes:

- **Values** are atomic numbers, colors, booleans, strings and similar data.
- **References** identify graphs or nodes. Input edges are stored as node-reference properties because an input has at most one source, while one output may feed many inputs.

Diffs are unordered dictionaries at three levels. A node diff contains changed property values; a graph diff contains node additions, deletions and diffs; a program diff contains graph additions, deletions and diffs. Metadata can use the same representation: comments/groups become typed nodes and positions/colors become properties. This is a snapshot model. It does not record the authoring command sequence, causal intention, editor heap, interpreter stack, timers, pending events or external effects.

Node and graph identifiers are not assumed stable across editing sessions. The paper explicitly rejects dependence on editor-assigned IDs because those IDs would have to remain stable through histories, undo/redo, copy/paste and drag/drop in every participating editor. It instead infers a **matching** from each edited snapshot back to the ancestor:

1. Match program graphs greedily by the difference in their counts of node types.
2. Within each matched graph, forbid cross-type node matches.
3. Score same-type nodes by the fraction of represented values and references that differ. References to objects already matched lower the cost of adjacent candidates; unresolved references initially differ.
4. Repeatedly accept the currently cheapest candidate, stopping at cost **0.65** for graphs and **0.35** for nodes. Unmatched version objects are additions and unmatched ancestor objects are deletions.

The procedure is a greedy approximation, not a globally optimal graph edit distance or recovered edit history. Same-type, same-property sequences can tie. The paper treats permutations of identical nodes in a chain as version-equivalent; it does not establish deterministic conceptual identity when tied objects matter for an external obligation.

## Paper-to-source correspondence

The separately selected public repository was read earlier at commit [`764c4aaabf98548f8f9f824fce8fa3e74e69943c`](https://github.com/edu-rinaldi/NodeGit/tree/764c4aaabf98548f8f9f824fce8fa3e74e69943c), dated 2023-12-06, one day after the publication date. Twenty-eight selected implementation/documentation files were read completely; seven acquired build/logging/timing/visualizer files, third-party dependencies, fixture bodies and the teaser remained outside that source reading. The current paper reading used that bounded source coverage rather than treating it as an execution or rereading the entire repository.

| Question | Published paper | Pinned public implementation | Status |
| --- | --- | --- | --- |
| Imported identity | IDs need not be stable across editing sessions; correspondence is inferred. | The Blender parser assigns fresh UUIDs to imported nodes/subgraphs. | Direct mechanism correspondence. |
| Node cost | Different types cannot match; changed values/references are divided by the average property counts, which the paper states are equal for same-type nodes. | Counts values, node/graph/texture references and input references, then divides by the ancestor property's count. | Equivalent only under the stated fixed-property-set/equal-count premise. |
| Graph cost | Absolute node-type-count differences divided by the average of ancestor/version node counts. | Divides by the **ancestor** node count. | Material formula difference when graph sizes differ; exact evaluation-build correspondence is unverified. |
| Greedy stopping | Accept current best cost strictly below 0.65/0.35. | Same thresholds and strict comparison. Iteration uses unordered sets and tie replacement/early exit. | Core correspondence, with implementation-order tie sensitivity. |
| Metadata | Users may enable or disable metadata versioning; Figure 5 demonstrates grouping, comments, minimizing and moving nodes. | Metadata participates in matching, but the public Blender diff command then unconditionally removes `x`, `y`, width and height changes from the emitted diff. | The inspected CLI is not the paper's demonstrated position-preserving mode. |
| Conflict merge | Same-node delete/edit and different concurrent values for the same property conflict; resolution is left to the user. | Checks those overlaps. If any conflict exists, the core leaves its result as the ancestor and the CLI emits the conflict list; it does not emit a partially patched document. | Same conflict predicate, narrower concrete conflict workflow than a full interactive resolver. |
| Equal additions | Not specified as a separate semantic coalescing rule. | The CLI removes identical added-node payloads from the second diff before merging. | Source-only wrapper policy. |

The public Blender adapter also gives node groups a type influenced by group name, encodes up to 16 inputs for a geometry-join special case, and reconstructs output with a separate socket/type description. These are concrete adaptation obligations. The paper does not cite this exact commit as its measured build, and the source packet contains only the Giyuu and Kiwi fixture families rather than the full 16-program evaluation archive. Source correspondence therefore strengthens method understanding without reproducing the reported results.

## Diff, merge, conflict, and undo semantics

After matching, a version-to-ancestor diff translates references to matched objects back to ancestor IDs. Whole unmatched nodes/graphs become additions or deletions; changed nodes carry only altered property/reference values. Patching copies an ancestor and applies additions, deletions and property updates.

Three-way merge computes one diff for each version against the shared ancestor. The paper calls the merge well defined when the two change sets are independent and therefore commute. It combines changes to different properties, and treats identical values as compatible. It reports conflicts for:

- deletion of a node/graph in one branch and modification of that same object in the other; or
- different concurrent values for the same node property/input connection.

The algorithm does not choose a winner. The paper leaves conflict resolution to the user, while the inspected CLI outputs conflicts instead of an automatically repaired or partially merged result. No conflict-resolution task is included in the evaluation.

The conflict predicate is local to overlapping changed IDs/properties. Neither the paper nor inspected source states a dependency-closure check for a deletion in one branch and a newly added object in the other branch that references the deleted object. The earlier source reading therefore retains a narrowly scoped inference: sequential patching can construct a dangling reference in such a case. This was not executed, its frequency is unknown, and it is not reported as a paper failure. A successful overlap check establishes compatibility of represented local changes, not acyclicity, renderability, intended program behavior or cross-artifact reference validity.

NodeGit has **no described undo/redo operation**. Its output is the net unordered delta between snapshots, not a reversible command log. The paper mentions undo/redo only to explain why editor IDs are an unattractive identity foundation. It does not show inverse-patch generation, history navigation, restoration of an editor session, or rollback of external effects. Figures 1–3 and 5–9 depict authoring snapshots and rendered results after offline integration; they are not observations of an in-progress runtime carried through a change.

## Evaluation allocation and assistance

The evaluation has three distinct parts and no recruited participants.

### Selected author-made edits

The authors select **16** publicly available Blender procedural programs representing shapes and materials. Ancestors contain 1–6 graphs, 26–266 nodes and 603–6,199 properties. Two independently edited versions are constructed for each program, giving **32 ancestor–version diffs and 16 three-way merges**. The authors describe tens to roughly 100 operations per version: node/edge additions and deletions, property changes and edge reconnections, chosen to make visible output changes and challenge diff/merge. They inspect whether diffs report their edits and whether merged programs include both edit sets, then render ancestors, versions and merges in Blender.

This is favorable author inspection of constructed non-conflicting examples. The paper supplies no blinded labeler, independent behavioral oracle, inter-rater check, exact task script, authoring time or conflict-resolution case. Table 1's graph/node/property counts describe snapshots and represented edit sizes, not person-time or collaboration effort.

### Randomized matching tests

Each of the same 16 programs receives two families of randomized **single-version correspondence** tests:

1. Modify node properties only, from 10% through 100% in ten-percentage-point steps while retaining graph structure.
2. Apply mixed property, edge and node operations at budgets from 10% through 100% of the graph's node count. Property modification, edge addition/deletion/modification and node addition/deletion are assigned equal probabilities, subject to producing structurally valid graphs.

The generator retains the known matching and the algorithm's output is compared with it. Each program/rate condition is repeated **100 times**. Read literally, this design implies 16,000 trials per family and 32,000 total, although the paper does not print that aggregate, release seeds or report uncertainty. The randomized graphs may be structurally valid while producing meaningless images; this tests matching recovery under generated perturbations, not semantic output, merge conflict handling, collaboration or maintenance.

The thresholds 0.65 and 0.35 were found “experimentally” for the authors' case. No training/validation split or out-of-sample threshold analysis is reported, so the randomized results should not be treated as a preregistered generalization test.

### Comparators and assistance

- **Git text merge:** the authors serialize nodes and edges as JSON dictionaries with one property per line, then apply Git to all Table 1 edits. This is a specified textual encoding, but no alternative canonical order, semantic driver or manual resolution workflow is tested.
- **Graph edit distance:** the authors run all 20 algorithms in the C++ library accompanying Blumenthal et al.'s survey on the same 32 ancestor/version pairs. Node properties/types become node labels and edges use the comparators' native representation. Because those methods do not support subgraphs/instancing, subgraphs are encoded as special nodes and **NodeGit's own matcher supplies the subgraph correspondence**. The paper reports only the four best-performing methods: Bipartite, Branch, Ring and SimulatedAnnealing. Their result is therefore a node-matching comparison conditional on author-provided subgraph assistance, not a complete end-to-end alternative on the native representation.

## Reported outcomes and cost

For all 32 selected diffs, the authors report correct edit detection; all 16 selected merges contain both edit sets under their inspection and render comparison. On one AMD 5975WX at 3.6 GHz, the C++ standard-library implementation takes **1–775 ms** per diff in Table 1. The authors say every merge is below **1 ms**, so merge times are omitted. These timings exclude Blender authoring, import/export, rendering, visual inspection, conflict repair and integration engineering.

All property-only randomized conditions recover the known matching. In the mixed-operation family, every condition for 15 programs succeeds. EuroPavement is exact through 40%; Table 2 reports failures in **2, 1, 1, 3, 4 and 7 of 100** repetitions at 50%, 60%, 70%, 80%, 90% and 100% edit budgets. Failed trials average 2.00 mismatches except 2.14 at 100%, out of 131–266 edited nodes. These are **18 failed trials across the six displayed 100-repetition high-edit cells**, with no failure below 50%. The p.9 prose describes exact matching through a 50% modification rate, whereas the table and its caption place failures at 50%; this reconstruction retains the table's explicit counts. The paper's practical-small-edit claim remains a claim about this generated distribution.

Git reports unexpected merge conflicts in **all 16** selected programs. The experiment does not time or attempt ordinary manual conflict repair, so it establishes false-conflict behavior for this serialization, not total-work superiority over a complete Git workflow.

On the same 32 ancestor/version pairs, summing Table 3 yields **107** mismatched nodes for Bipartite, **102** for Branch, **21** for Ring and **87** for SimulatedAnnealing; errors occur in 11, 11, 9 and 9 of the 32 pairs respectively. NodeGit reports zero on these selected pairs. Comparator times range from 1–149 ms (Bipartite), 1–287 ms (Branch), 211,247–92,645,545 ms (Ring), and 19–2,722 ms (SimulatedAnnealing), while NodeGit's corresponding Table 1 diffs range from 1–775 ms. This is strong relative evidence for typed, domain-specific matching on the selected programs. It does not establish universal superiority over the 16 unreported algorithms, unsupported subgraphs, other node editors, other edit distributions or complete collaboration workflows.

## Limits and evidence scope

The paper itself identifies ambiguity for same-type sequences with identical properties and possible impractical cost at tens of thousands of nodes. Additional limits follow from the method and reporting:

- fixed node types/property sets and small-to-moderate snapshot changes are part of the successful operating regime;
- the largest tested ancestor has 266 nodes, far below the stated tens-of-thousands concern;
- graph-cost normalization differs between the paper formula and inspected public source, and the paper does not bind its experimentally selected thresholds to this exact commit/build, so measured-code equivalence is unresolved;
- generated ground truth checks correspondence, while curated render inspection checks visible outcomes; neither is a final behavioral specification;
- no intentional merge-conflict benchmark, dependency-closure oracle, undo/history task, user study, long sequence, team handoff, authoring-time measure or total-labor measure is present;
- no compiler settings, Blender version, seeds, trial-level data, uncertainty, sensitivity analysis or independent reproduction is supplied;
- the public source's Blender integration and the comparator subgraph assistance both carry adaptation costs that the runtime tables omit.

## Prior access history and retained source record

Before the PDF became available, SC222 returned the exact DOI but only 1,053 abstract characters. ACM's PDF route returned 403 HTML, LibKey returned a 5,580-byte shell, OpenAlex exposed no PDF URL, and the Unimore and Sapienza records provided metadata without files. The author page bound the DOI to the repository. These remain accurate historical access facts; they no longer describe current body coverage. The verified publication PDF was already attached from the HKUST workspace route dated 12 October 2026; this reading made no Zotero mutation.

Existing canonical note **`SL8DRIBJ`**, version **5887**, was not changed. Source packet **`96989TR3`**, version **5884**, remains a 49,181-byte non-PDF attachment containing the 28 selected files, coverage manifest and old abstract-only text, SHA256 **`6d2df654aa4fa1793ba5cfa671275b3776649e4399801497fea28cf5f981874f`**. Its bounded source coverage and the paper's complete reading are different evidence units. The prior citation/search audit and decisions remain historical retrieval records; no new Scite inspection was performed for this completion.

## Lineage and consequence for Nu

[S283 NCCollab](S283-nccollab-collaboration-history.md) measures a bundled behavior-tree collaboration interface with communication, preview and document history. NodeGit has no comparable participant or undo evidence, so S283's completion-time and collaboration findings cannot be transferred to it.

[S284 LevelMerge](S284-levelmerge-scene-merge.md) uses durable graph IDs and explicit dependency propagation for Unity scene snapshots, then reports a small conflict-prone comparison. NodeGit instead infers identity for typed procedural graphs and evaluates matching at much larger randomized edit rates. These are alternative identity/conflict designs, not independent replications of one another.

[S285 SceneGit](S285-scenegit-reading-2026-10-15.md), from the same broader research lineage and sharing Pellacini authorship, provides domain-specific whole-scene correspondence, sparse version identities, merge timing and a bounded user study. NodeGit cites its dictionary-style diff representation but studies typed procedural node programs with a different corpus and evaluation. Shared authorship and conceptual lineage do not add independent support to either result.

For R11, NodeGit strengthens the requirement that a credible comparator need not inherit stable IDs: typed structural matching can recover ancestor identity and merge many represented edits efficiently. It also makes representation/adaptation cost explicit. A future comparison should record identity premises, supported edit classes, threshold/tie behavior, conflict and dependency policy, adapter effort, manual repair, fresh-load behavior and total team work.

NodeGit does not establish preservation of Nu's selected F# handle across a scene rename, running-state continuity, temporal/effect equivalence or net collaboration benefit. Its authoring snapshots remain distinct from live runtime state. It supports retaining graph-document diff/merge as a capable alternative and keeping behavioral/reference checks separate from a clean merge status. No experiment, source execution, candidate run or human study follows from this reading alone.

**Remaining exact gaps:** supplemental visualizations; all randomized inputs/seeds and expected matches; full evaluation fixtures; the exact measured source revision/build and graph-cost formula used; compiler/Blender configuration; conflict-resolution behavior and cost; cross-object validity tests; participant/team workflow evidence; and any running-state or undo contract.
