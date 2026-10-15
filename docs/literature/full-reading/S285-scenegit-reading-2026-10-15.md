# S285 - SceneGit: fine-grained scene correspondence, merge, and scoped collaboration evidence

**Work:** Edoardo Carra and Fabio Pellacini, *SceneGit: A Practical System for Diffing and Merging 3D Environments*. ACM Transactions on Graphics 38(6), article 159, 15 pages, November 2019. [DOI 10.1145/3355089.3356550](https://doi.org/10.1145/3355089.3356550).

**Disposition:** the complete primary article closes S285's body-access and method gap. SceneGit supplies a concrete semantic scene-versioning treatment: it converts whole scenes to a common sparse representation, infers fine-grained correspondence, and merges non-overlapping snapshot changes while exposing conflicts for later manual repair. Its scale tests are favorable. Its user study supports perceived edit visibility and acceptance in a bounded offline workflow, but has no comparator, reports no conflicts, and measures neither delivery time nor total team work. The result strengthens R11's comparator and diagnostic design without establishing dedicated Nu merge support, running-state preservation, or a reason to reopen a human study.

## Identity and actual coverage

Native Zotero parent **`53D9GIMM`**, version **5880**, remains in collection **`PKLXQNEE`** with the exact DOI, title, volume 38, issue 6 and publication date. Attached PDF **`6556W8FI`**, version **6631**, is titled *Full text PDF - retrieved via HKUST workspace (12 October 2026)* and resolves to `53D9GIMM.pdf`. The file is **67,513,366 bytes**, SHA256 **`be79bc0e13f4e49daee7975f461e2b3499a1888218d1e1b805adc33b6f10470e`**. Its first page and running headers identify the exact work, authors, DOI and ACM TOG 38(6), article 159 edition. The earlier abstract-only attachment **`7V6ABH46`** remains correctly labeled and is not this PDF.

All **15 pages** were parsed and read, including all sections and references. Page-level extraction returned text on every page. Original rendered pages **1, 6-8 and 10-15** were inspected at full rendered resolution; together they cover **Figures 1-12**, **Tables 1-2**, the data-model and algorithm diagrams, all result montages, the animation plots and the complete user-study method/results pages. Pages 2-5 and 9 contain the remaining prose but no additional numbered figure or table. There is no appendix in the paper. The authors say the edited scenes and study questionnaire are in supplemental material; no supplement, implementation, raw participant data or scene archive is attached or read, and no reproduction was run. Copyrighted PDF text and page renders remain in ignored `.artifacts/s285-reading-20261015/`, outside Git.

## Representation and identity

SceneGit versions the **whole scene**, rather than independent files, so that represented references can survive integration. It converts OBJ and glTF inputs to a common representation:

- A scene is an unordered hash table of objects. Each object has a type, arbitrary named properties and references to other objects. The represented object references form a directed acyclic graph; a transform hierarchy is stored through parent references.
- Polygon meshes have separately identified vertices and faces, including distinct face-varying topologies for properties such as positions and texture coordinates. Textures are coordinate-indexed sparse grids. Animations are ordered sets of identified keyframes.
- A repository identifier is a pair of **version ID and element ID**. References use these identifiers rather than in-memory pointers. Additions carry a version identifier; updates and deletions use the matched ancestor identifier. Changes are sparse hash tables in which a null value represents deletion.
- Scene conversion initially assigns counters to shape, texture and animation elements. Scene objects use their authored name when it is available and unique, otherwise a counter. The version tag makes identifiers repository-wide. This does not mean source assets already contain durable UUIDs: correspondence with the ancestor is inferred at diff time, after which the ancestor identity is assigned to a matched version element.

This is a structural snapshot representation. It records represented properties and references, not editing commands, author intent, external source-code handles, runtime heaps, pending events or effects. OBJ/glTF adaptation also reconstructs files from the common representation; preserving original byte layout is not a goal.

## Diff and correspondence procedure

Diff takes an ancestor and one edited scene and returns additions, deletions and updates that reconstruct the version when applied as a set. A fast content hash first prunes unchanged objects. The expensive step is correspondence, for which SceneGit uses distinct heuristics by data domain rather than a globally optimal graph edit:

| Domain | Correspondence rule | Consequence and premise |
| --- | --- | --- |
| Scene objects | Match the generated identifier, normally based on an authored unique name. For unmatched add/delete candidates, detect renames by identical properties. Transform groups with otherwise ambiguous local properties are greedily paired using property equality plus subtree bounding-box center and size. | Names and property equality are heuristics, not author-intended identity. A rename combined with other property edits may not satisfy the described exact-property rename rule. Greedy pairing does not establish a globally optimal match. |
| Mesh vertices and faces | Match exactly unchanged vertices with hashes of concatenated properties. For remaining vertices, greedily choose nearest candidates within a radius based on average edge length, using Euclidean property distances and cosine distance for normals. Rewrite face indices through vertex matches, then match faces. | Small local edits are favored. Remeshing, large moves or almost-total change become updates or add/delete pairs and may prevent a useful concurrent merge. |
| Textures | Use texel coordinates as identifiers. | The regular domain is assumed stable. Image resizing is not recognized as an operation; resampled pixels become many changed values. |
| Animations | Minimize string edit distance over ordered keyframes. | Keyframe order is preserved, and the related-work discussion explicitly assumes keyframes are not switched during editing. |
| Properties and references | Compare atomic property values and translated object identities after object matching. | Equality exposes represented value changes. It does not evaluate application semantics or cross-artifact obligations. |

After matching, additions are keyed by version IDs, while deletions and updates are keyed by ancestor IDs. The paper intentionally favors speed and generality over minimum change size. It describes false update/add-delete classification as conservative because edits remain exposed, while acknowledging larger repositories and less precise conflicts. That claim is about represented values under supported conversion; it does not prove correct conceptual correspondence for every edit.

## Merge, conflicts, and validity boundary

Patching copies the ancestor and applies one complete unordered change set. The authors treat the source version as well formed and apply the set atomically, so intermediate reference consistency is not checked.

Three-way merge diffs each version against a common ancestor. For each object, the two changes are independent when their changed-key intersection is empty. Same-key overlap detects concurrent updates and update/delete cases. Non-overlapping sets are applied together; unique version IDs keep independent additions distinct. The paper attributes the resulting structural validity to repository-wide identifiers and whole-scene representation.

Conflict handling is deliberately non-semantic. If one operation on an object conflicts, **all operations on that object are marked conflicted**. SceneGit does not choose a winner or synthesize a domain-specific resolution. It outputs three tagged object copies representing the ancestor and both versions so that an artist can repair the conflict in an ordinary modeling package. Fine granularity is expected to make these cases rare.

These rules sharpen several limits relevant to R11:

1. A successful key-disjoint merge establishes represented structural compatibility, not intended gameplay or cross-file reference behavior. The described intersection test does not give a dependency-closure rule for deleting one object while another changed object gains a reference to it. R11's C4 deletion/reference observation therefore remains necessary; no failure is claimed without a direct construction.
2. Independent additions carry different version identities. The paper does not specify semantic coalescing for two branches that independently create the same intended object.
3. Conflict output is a diagnostic and repair input, not a correct integrated scene. R11 must count the artist/integrator's resolution, reload and behavior verification.
4. Object names, properties, subtree bounds, mesh locality, fixed texture domains, ordered keyframes and well-formed converted input are validity assumptions. Almost-total edits are a stated limitation: they give unhelpful visualizations and fail to merge with any other edit on the object.
5. The method operates on quiescent snapshots. It contains no live editor reconciliation, running simulation, pending input/timer, heap-identity or external-effect preservation contract.

## Engineering evaluation and comparator limits

The authors create two independently edited versions for each of **12 scenes** spanning indoor/outdoor environments, single large meshes, large scene graphs and animation. Edits were made in Blender and Photoshop and included parameter adjustment, painting, sculpting, low-poly modeling, additions/deletions, instancing, layout and scripting. Inputs use OBJ and glTF. Rendered results and false-color provenance displays are used to inspect whether both edits appear without visible path-tracing artifacts.

Table 1 reports one pair of diff timings and one merge timing per scene on a four-core 3.5 GHz iMac with 32 GB RAM. Ancestors reach roughly **400,000 objects, 27.8 million polygons and 1 billion texels**. Individual diffs range from effectively zero to **15.68 seconds** and merges from **0.01 to 9.21 seconds**. Repository ancestors range from **21 MB to 2.7 GB**, with sparse version changes much smaller than their scenes. There are no repetitions, variances, independent correctness labels or complete workflow times for editor load, conversion, manual inspection and repair.

Table 2 supplies targeted algorithm comparisons:

- On two mesh cases, SceneGit reports the same detected edits as MeshGit with substantially smaller repositories and times. MeshGit is about 200 times slower on the smaller case and more than 1,500 times slower on the larger reported case; a separate large edit was stopped after 12 hours. SceneGit uses a stricter same-element conflict rule and can flag conflicts that MeshGit separates geometrically/topologically.
- For the Paris hierarchy, JsonDiffPatch leaves **18,667 of 18,980 nodes** improperly edited and therefore marked conflicted by the authors after format conversion.
- On Bistro and Paris file snapshots, Git and Plastic SCM produce much larger changes and **170-18,411** reported conflicts, whereas SceneGit reports zero for those selected edits.

These are favorable algorithm/fixture results, not a comparison of complete collaborative workflows. The Git/Plastic conditions do not include ordinary communication, semantic manual repair and accepted behavior verification. JsonDiffPatch required an adapter and author classification of improperly edited nodes. MeshGit covers only meshes. LevelMerge is cited but not compared experimentally, so its dependency handling and small conflict-task study remain separate evidence rather than a defeated baseline. The selected examples, edits and visual checks are not a prevalence sample or an independent replication.

## User study

The study recruits **16 users**, described only as novice or proficient users of 3D design tools. Sessions pair users of the same reported skill level; counts, recruitment route, skill criteria, demographics, assignment and training are not supplied. The design appears to yield eight pairs, but the paper does not state the number of independent pairs explicitly or report pair-level results.

Each pair edits three large scenes: bedroom, kitchen and teaser. Before a scene, the pair briefly agrees on the desired final look. Each person then edits an ancestor independently for **15 minutes**, without communication, and must change at least one shape, material and scene node. SceneGit diffs and merges the two versions. Users see a composite diff/merge image and answer three five-point agreement questions: whether highlights correspond to their edits, whether the rendered merge respects their edits, and whether the workflow simplified collaboration. A final binary question asks whether they would want the system integrated into a collaborative environment.

The paper reports that all 16 users strongly agreed that highlights represented their edits and that merged scenes respected them. All agreed that SceneGit simplified combination, including 14 who strongly agreed. All 16 answered yes to integration. The paper says the Likert results reject a null hypothesis at **p < 0.05**, but does not identify the statistical test, null distribution, treatment of the three repeated scene sessions, correction for multiple questions, or uncertainty. It reports no conflict in any study merge.

This is positive subjective evidence for edit visibility, perceived result fidelity and willingness to use the workflow after brief bounded tasks. It does **not** compare SceneGit against another tool or ordinary manual integration; measure completion time, person-minutes, defect rate or retained behavior; test conflict resolution; or separate the effect of visualization from structural merge. The initial meeting and enforced silent editing are part of the tested package, not a general conclusion that communication is unnecessary. The uninspected supplement is needed for the exact questionnaire and scene materials; raw/participant-level responses are unavailable.

## Consequence for R11

SceneGit changes R11's literature status from an unread promising method to a **complete primary treatment reconstruction**. It shows that source assets need not already carry stable UUIDs: a system can assign repository identities at ingest and use domain-specific matching to carry ancestor identity into edited snapshots. A credible future comparator may therefore include semantic scene conversion, inferred correspondence, fine-grained provenance and conflict visualization. Adaptation work, format coverage and manual resolution belong in the cost boundary.

It does not make the current Nu case trivial. Nu's selected title scene is serialized separately from F# event handles; SceneGit's represented scene references do not include those code-level paths. R11 C2 still needs the Start rename, presentation edit and F# handle to converge as one accepted behavior. Its specified scene split fits the described rename heuristic only if the rename branch leaves the object's other represented properties identical; a branch that bundles rename with presentation changes is not covered by that exact-property rule. C3 remains an explicit negotiation/resolution task because SceneGit declines to choose among conflicting same-property values. C4 remains a cross-artifact dependency check rather than an assumed consequence of successful scene merge.

The study supports retaining provenance visualization and user-perceived edit visibility as secondary observations, while keeping textual conflict status, fresh load, identity/reference consistency and behavior as separate outcomes. It gives no basis to replace total-team work with a Likert rating, to prohibit communication in an ordinary comparator, or to promote R11 ahead of the higher-priority maintenance studies. No dedicated Nu merge facility is established; SceneGit would be an external treatment with an adapter and verification cost. Human comparison remains deferred until a consequential practical decision, feasible implementation and separately justified participant design exist.

**Next consequential use:** update the R11 contract and synthesis to replace the access-gap statement with this bounded method/evaluation evidence. Preserve LevelMerge's final-edition gap and NodeGit's paper/evaluation gap. If R11 is later promoted, first decide whether a SceneGit-like semantic merge is sufficiently applicable to Nu's serialized UI plus F# handle boundary to justify an adapter; otherwise retain ordinary Git, communication and manual reconciliation as the credible comparator. No experiment, participant study or candidate run follows from this reading alone.
