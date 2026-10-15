# S262 — Phylogenix: configured-object analysis and integration

Samuel Navarro, Antonio Iglesias, Francisca Pérez, Carlos Cetina and Jaime Font, *Phylogenix: Bringing phylogenetics to Unity*, SPLC 2024 Volume B, pp. 38–41, [DOI 10.1145/3646548.3676604](https://doi.org/10.1145/3646548.3676604).

**Complete primary reading, 2026-10-15.** The four-page ACM version of record is read in full and every page is rendered and visually inspected. Coverage includes all body text, Figures 1–3, Table 1, footnotes, acknowledgments and all 32 references. This supersedes the final-edition and figure gaps in the 2026-10-04 reconstruction. That earlier work remains part of the record: all 960 indexed lines of the five-page author manuscript, its table, 31 references and demonstration appendix were read; the separate eight-page user guide received complete text and visual coverage; selected public source and the S254 replication package were inspected passively. No engine, plugin, viewer, source build, video, algorithm or experiment was executed.

The paper contributes an integrated way to organize prefab relationships for inspection. The inspected package also exposes consequential differences between the paper's binary/Manhattan/neighbor-joining description and the released implementation. Neither similarity nor a generated tree establishes historical ancestry, correct runtime behavior, a completed maintenance outcome or saved work.

## Identity, editions and coverage receipt

An earlier continuation misassigned DOI `10.1145/3715002` to this tool. That DOI identifies *Introducing Phylogenetics in Search-based Software Engineering: Phylogenetics-aware SBSE*, a distinct 2025 method lead. SC181/SC182, title search and Crossref resolved the correction before selected reading. The mistaken references and four native Blueprint notes were corrected in commit `4863e61`; the legitimate older SBSE reference remains separate.

Collection `PKLXQNEE` contained 291 parents before the original selection. Exact title/DOI searches in the collection and library found no existing Phylogenix parent. Parent `PKVMQLQ2` was created at version 5679 and note `E3FLLUFB` at version 5680 before selected body reading. On 2026-10-15 the parent was reverified natively at version **5688**, with the exact title, DOI and collection membership, before the new PDF was read. Its children were `LGLJ8WXT`, `E3FLLUFB`, `8U62S98R`, `3XKY2E46` and `AK8R55ZC`.

| Native attachment | Identity and actual scope |
| --- | --- |
| ACM version-of-record PDF **`LGLJ8WXT` v7115** | `C:/Users/hadri/Zotero/storage/LGLJ8WXT/PKVMQLQ2.pdf`; 1,978,099 bytes; four pages; SHA-256 `2980ef35ccff890303c576838d258c86f213c37179181bb4a701e74af7e2154e`. Page 1 visibly supplies the exact title, five authors, SPLC 2024 venue, pp. 38–41, four-page extent and DOI. All four extracted pages and all four 144 dpi renders were read; Figures 1–3 and Table 1 were inspected at full rendered resolution. |
| Guide PDF **`AK8R55ZC` v5682** | 674,738 bytes; SHA-256 `bdb43140086bc00c5991a8f621cda29fbcbdd75424a50eb6700b9783b3616ed0`; MD5 `431448dbad93189dda4bc7bd2d6f8bac`. Eight physical pages; all text and page visuals inspected, pp. 6 and 8 enlarged. Page 5 is predominantly an image, not an empty page. |
| Indexed manuscript text **`3XKY2E46` v5684** | 37,511 bytes; SHA-256 `0087f287f9fdd4887516d9c99cc70f1b8cf3bc9946c38ed863a5b0e20230880d`. Explicitly labeled tool-indexed text, not an original PDF. Lines 0–959 merge without gaps or conflicts; its three primary figures were unviewed in that edition. UTF-8 was recorded. |
| Selected pinned source **`8U62S98R` v5686** | Locally assembled ZIP of eight original C# files plus provenance, 11,705 bytes; SHA-256 `5b9fcdf9eb01ce0f06d69442dbc88fb7149f21b21aeec34172983bd1bfd5bcb4`. This is not a complete repository or author-issued release archive. |

The exact VOR was retrieved through the already authorized integration after the DOI route resolved to the ACM PDF viewer; the acquisition receipt is `.artifacts/s262-acquisition-20261015/acquisition-receipt.json`. Reading artifacts, including native reverification, page extractions and four renders, are under `.artifacts/s262-reading-20261015/`. Acquisition and identity checks are not counted as body reading.

## Final edition correspondence

The [indexed author manuscript](https://svit.usj.es/wp-content/uploads/2024/09/Navarro_SPLC_2024_PRE.pdf) is five pages with a placeholder DOI/ISBN and template received/revised/accepted dates. The ACM VOR is four pages, supplies the actual DOI/ISBN and publication venue details, and contains 32 references. Its core method and four-project account correspond closely to the manuscript, but several differences matter:

- The manuscript's fifth page is a demonstration plan. The VOR omits that appendix; it does not document an observed demonstration or provide a supplementary protocol.
- The manuscript says only that a video is available at a direct YouTube URL. The VOR says the video and source code are available through the [author landing](https://svit.usj.es/phylogenix/).
- The manuscript reports **1,319** NeonHAT prefabs; the VOR reports **1,318**. The other three Table 1 counts and all four reported analysis times agree.
- The VOR changes the heading from “Conclusions” to “Discussion and Conclusions” and replaces the short future-work paragraph. It adds proposed feature-model extraction, FAMA-based complexity analysis, tree-size/readability work, creative-decision language and visualizer support for more roles. These are future directions, not evaluated outcomes.
- The VOR adds Pablo Trinidad et al.'s FAMA reference as reference 30, shifting the phylogeny-method and market-report references to 31 and 32. It also removes the author's plan to upload the plugin to the Unity Asset Store and add more inference methods.

Thus the final edition closes the source and visual gap but does not supply a controlled study, source snapshot, build manifest, hardware protocol or supplement. The linked video remains unviewed. The exact Unity version, tool commit and project snapshots used for the four reported analyses are not identified.

## Published method and observed applications

Figure 1 and Section 4 describe this pipeline (VOR pp. 39–40):

1. scan a Unity project's prefabs and identify components such as Transform, Collider, Mesh and individual MonoBehaviours;
2. encode each prefab as a same-length sequence of ones and zeros for component presence or absence;
3. compute pairwise Manhattan distances, described as the number of differing genes, and assemble a distance matrix;
4. apply the neighbor-joining method to infer relationships; and
5. produce a rectangular or circular phylogenetic tree for exploration in a web viewer.

Figure 1 is a schematic flow, not a trace of one of the commercial projects. It depicts sample prefab component lists, binary encodings, a distance matrix and both rectangular and circular trees. A 400 dpi inspection exposes an unresolved internal inconsistency: its lower-triangle values are fractions (`0.75`, `0.33`, `0.5`), and every displayed diagonal cell is `1`, whereas Manhattan distance on binary vectors counts differences and self-distance is zero. The adjacent text supplies neither a special diagonal convention nor a normalization denominator. Ellipses omit vector entries, so the printed off-diagonal values cannot be reconstructed completely from this schematic. Treat the numbers as inconsistent or unexplained illustration, not evidence of the executed algorithm. Figure 2 shows the Unity editor panel with input/output folders, execute/cancel controls and filterable log categories. The paper says the C# plugin analyzes prefabs and performs inference while the web viewer supports exploration and image export (VOR p. 40).

Table 1 reports four applications:

| Game | Prefabs in ACM VOR | Project size | Reported analysis time |
| --- | ---: | ---: | ---: |
| VTM: Heartless Lullaby | 84 | 3.6 GB | 1 minute |
| Grabitoons! | 158 | 6.5 GB | 2 minutes |
| NeonHAT | 1,318 | 11 GB | 6 minutes |
| Toy Tactics | 2,036 | 134 GB | 25 minutes |

The paper calls these “case studies” and says the tool was validated on four commercial games. The reported empirical material is limited to the project descriptions, prefab counts, project sizes, one elapsed analysis time per project and the Grabitoons tree. Figure 3 visually shows a large tree and an enlarged branch in which the Canvas prefabs cluster. No participant sample, assigned task, interview, questionnaire, correctness assessment, tree-quality ground truth, maintenance change, behavior test, hardware specification, warm-up, repetition or timing uncertainty is reported. Input size and project content vary together, so the four times are not a controlled scaling or runtime comparison.

Retain the useful evidence that four commercial Unity projects were processed and that one resulting tree grouped the labeled Canvas prefabs. The article interprets the tree as an ordered structural view and a possible first step toward variability formalization. It does not verify ancestry or chronology. Latent-content generation is attributed to reference 9, [Chueca et al. 2024](https://doi.org/10.1145/3646548.3672596); no content is generated or evaluated in S262 itself.

## Guide and public-source coverage

The guide requires C# 9, .NET Standard 2.1 and prefab input; its example screenshot shows Unity 2022.3.27f1. It says all render pipelines are supported because the tool scans `.prefab` files, permits selecting another project's Assets folder, exposes background progress and logs, and stores tree and intermediate data in the chosen output folder. The guide's “one button” language still presupposes installation, compatible project settings, valid input/output selection, prefab availability and a viewer handoff. These requirements narrow the paper's generic “any Unity project” language without demonstrating incompatibility with other versions.

The [author landing](https://svit.usj.es/phylogenix/) links two public repositories. The 2026-10-04 reconstruction established:

- [Plugin](https://bitbucket.org/svitusj/phylogenix-plugin), pin `c54a2e9a896305289807b6cd5221cc0f82def1ce`, 8 July 2024: 51 entries, 34 files/17 directories, 18 directory/page requests. The guide and eight selected C# files were acquired and fully read: editor, runner, options, return structure, gene/gene-stripped/encoding structures and pipeline orchestration.
- [Viewer](https://bitbucket.org/svitusj/phylogenix-viewer), pin `d5ca4eb4006288f4eac5b3ada794f2c736ebe10d`, 8 July 2024: 105 entries, 74 files/31 directories, 32 directory/page requests. Inventory only; selected viewer bodies were not acquired or read.

The next source request returned 429, including one later retry without a `Retry-After` header, so further requests stopped. Seventeen of 26 initially selected files remain unacquired: ten plugin sources and seven viewer files. A later continuation could resume the saved list after the rate limit clears, skipping and hash-verifying the nine acquired files. No alternate account or access circumvention was used.

The already acquired [S254 replication package 14591668](https://zenodo.org/records/14591668), native parent `GQVDG772`/ZIP `UFTKNWMM`, provides a separate lawful source edition. Its `Phylogenix.unitypackage` SHA-256 is `a8f8c65548d83a8bebcf756e401054c3c3ef0b5cf84f4b3411c34af2b5a573b5`. Passive tar inspection found 32 assets, including 29 C# bodies. Twelve newly selected files were read completely: encoding generator; matrix calculator and three distances; pairing; Newick generation; online-viewer adapter; general/file-output utilities; and two pair structures. Six shared modules have identical decoded lines to the pinned repository after BOM/line-ending normalization. Editor/runner differences received bounded inspection; nine remaining C# bodies were unselected. None of the eight overlapping files is byte-identical, and two changed modules preclude treating the package as the exact pinned repository release.

## What the inspected package actually computes

| Source location within `Scripts/` | Static reconstruction and consequence |
| --- | --- |
| `Jobs/1Genetic/EncodingGenerator.cs`, lines 62–154, 162–193, 258–305 | Reads prefab YAML documents and records **component counts**. MonoBehaviour GUID lookup supplies script basenames; nested-prefab source references contribute prefab names. This represents selected serialized structure, not script bodies, field-value behavior or observed execution. Nested references are not recursively expanded into a verified behavioral dependency graph. |
| `Classes/DataStructures/GeneticEncoding.cs`, shared decoded text | Builds the union of component headers, transfers observed integer counts and supplies zero for absent entries. Outlier/percentile code is commented out. There is no active binarization in this inspected path. |
| `Jobs/2Matrix/MatrixCalculator.cs`, lines 79–84; `BaseGeneticDistance.cs`, lines 8–21 | The active distance is **d(x,y) = count of unequal component counts / number of headers**. For binary vectors this is scaled Manhattan distance; for counts, 1 versus 4 contributes one mismatch rather than a magnitude of three. The VOR's binary/Manhattan description therefore does not fully describe this package. |
| Two alternative distance classes and editor options | Alternative formulas exist, but the inspected calculator directly calls the base distance. The package editor's selection is not passed through its active `RunWithReturn` call. Existence of an option does not establish that reported outputs used it. |
| `Jobs/3Pairing/PairingProcess.cs`, lines 30–100, 103–167 | Despite the `FindMaxCorrelation` name, it chooses the smallest nonnegative pair distance, merges the pair and replaces distances by the arithmetic mean of the two cluster distances. This inspected path has no row-total correction. Record this reconstruction separately from the VOR's neighbor-joining label; the original 1987 method is a bibliographic dependency, not independently reproduced here. |
| `Jobs/4Output/NewickGenerator.cs`, lines 77–102 | Recursively serializes merged pairs, sanitizes selected punctuation, assigns half the pair distance to leaves and emits pair distances on internal groups. Displayed edge lengths are not elapsed development time or independently verified ancestry. |

These are source-derived observations about the acquired S254 package, not evidence that a particular historical run used those bytes. Missing pinned encoding/pairing files prevent extending every detail to the July repository. The discrepancies do not show that the tool lacks practical value: related configured objects can still be brought together for inspection. They do mean that binary encoding, Manhattan distance and neighbor joining cannot be credited to the inspected released package without exact build correspondence.

Both inspected pipelines produce genetics, matrix, pair and Newick files. The package's editor reads output and posts it to a hosted `/api/tree` endpoint; its browser-open line is commented. The separate online-viewer helper logs a Base64-bearing URL while its own browser-open call is also commented. The pinned repository editor instead opens a different viewer landing and directs manual drag-and-drop. This is a concrete deployment and data-boundary difference, not a reproduced failure or a claim about the current hosted service. No project data was uploaded during reading. Parsing, names/GUIDs, output files, visualization and hosted-service assumptions belong in the integration account.

## Shared-study and data lineage

The four S262 games recur in S254's later five-game study; Kromaia is S254's additional proprietary-engine case. Shared game identities do not create four independent replications or prove identical project snapshots. S254 adds developer questionnaires, interviews, focus groups and one studio observation, but its trees and counts still belong to this shared Phylogenix lineage.

The exact count relationships are now:

- VTM: S262 VOR and manuscript **84**; S254 printed figure **85**; released tree **84**.
- NeonHAT: S262 VOR **1,318**; S262 manuscript **1,319**; S254 printed figure **1,318**; released tree **1,481**.
- Grabitoons: **158** across the S262 VOR, manuscript, S254 figure and released tree.
- Toy Tactics: **2,036** across the S262 VOR, manuscript, S254 figure and released tree.

The project versions, filters and reasons for the VTM/NeonHAT differences remain unresolved; no typo or snapshot explanation is invented. S254's positive participant observations retain their qualitative scope, while its dead-prefab, redundancy and misunderstood-relation findings remain adverse evidence. Tree similarity, participant-perceived reuse, chronological lineage and completed maintenance benefit are distinct constructs.

S263/S264 use the same phylogenetic idea and overlapping authors, but a different primary family and representation: 48 Kromaia NPCs expressed in SDML, normalized Levenshtein distance and expert-guided latent-content reconstruction/injection. S262 does not evaluate those generation procedures. S263/S264's favorable LCG/FICG outcomes therefore cannot be counted as S262 validation, and S262's four Unity projects are not additional generated-content datasets. Conversely, S262's released package discrepancies do not establish which source bytes produced the Kromaia results. Preserve S263/S264's same-dataset carry-forward, near-null seed-selection result and bundled expert reconstruction advantage separately.

## Consequences for R12 and R06

For R12, S262 provides a credible **diagnostic/organization comparator**, not a propagation or authoring-benefit comparator. Existing Unity tooling can extract configured prefab structure and display relationships across a project. A Nu comparison should credit that useful overview and ordinary Unity prefabs, scenes, editor configuration and helper composition. It should ask whether a selected maintenance or family-revision task needs relationship discovery, then measure the actual edit, retained instance variation, child/target identity, matched behavior, repair and verification. A recognized cluster or exported tree is not a completed change.

The VOR does not test source revision propagation, retention of instance-specific values, vocabulary extension, runtime-lifetime behavior, total authoring work or break-even reuse count. S263/S264's content generation has a different work boundary and bundles expert rules and manual reconstruction. None of these papers transfers a Nu benefit.

For R06, Table 1 is insufficient as a performance comparator. The four single reported times lack hardware, build, tool/source identity, repetition, variance, warm-up, phase breakdown and matched useful work; project gigabytes and prefab counts vary together, and extraction, inference, file I/O and viewer handoff are not separated. At most, the table shows reported end-to-end analysis completing in 1–25 minutes for four named projects. If relationship analysis becomes part of a selected Nu workflow, count installation/configuration, parsing, intermediate storage, tree generation, viewer transfer, inspection and any manual reconciliation as development costs, while measuring runtime/state-retention costs under R06's own matched policy contract.

The final VOR closes S262's primary-body and figure gap. It leaves exact reported-build/source correspondence, viewer bodies, video, project snapshots, hardware/timing protocol and reproduction open. Those gaps matter only if a selected comparison depends on them; they do not erase the paper's useful structural overview or justify another generic source crawl.
