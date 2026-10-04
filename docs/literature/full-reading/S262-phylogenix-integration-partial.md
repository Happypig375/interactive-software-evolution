# S262 — Phylogenix: configured-object analysis and integration

Samuel Navarro, Antonio Iglesias, Francisca Pérez, Carlos Cetina and Jaime Font, *Phylogenix: Bringing phylogenetics to Unity*, SPLC2024 Volume B, pp.38–41, [DOI10.1145/3646548.3676604](https://doi.org/10.1145/3646548.3676604). Main-agent reconstruction, 2026-10-04. **Partial primary reading:** all960 indexed lines of the five-page author manuscript, including its table,31 references and demonstration appendix, are read; its three figures remain unviewed. The separate eight-page user guide has complete text/visual coverage. Selected public source and the existing S254 package are inspected passively. No engine, plugin, viewer, author algorithm or experiment is executed.

The useful contribution is an integrated way to organize prefab relationships for inspection. The inspected package also exposes a consequential difference between the published method description and released implementation. Neither similarity nor a generated tree establishes historical ancestry, correct behavior or saved maintenance work.

## Identity, editions and native holdings

An earlier continuation misassigned DOI10.1145/3715002 to this tool. That DOI identifies *Introducing Phylogenetics in Search-based Software Engineering: Phylogenetics-aware SBSE*, a distinct2025 method lead. SC181/SC182, title search and Crossref resolve the correction before selected reading. The mistaken references and four native Blueprint notes were corrected in commit4863e61; the legitimate older SBSE reference remains separate.

Collection`PKLXQNEE` contained291 parents before selection. Exact title/DOI searches in the collection and library found no existing Phylogenix parent. Native **`PKVMQLQ2`5679** and note **`E3FLLUFB`5680** were created before selected body reading. Subsequent attachments preserve those keys and membership:

| Native attachment | Identity and actual scope |
| --- | --- |
| Guide PDF **`AK8R55ZC`5682** |674,738bytes; SHA-256`bdb43140086bc00c5991a8f621cda29fbcbdd75424a50eb6700b9783b3616ed0`; MD5`431448dbad93189dda4bc7bd2d6f8bac`. Eight physical pages; all text and page visuals inspected, pp.6/8 enlarged. Page5 is predominantly an image, not an empty page. |
| Indexed manuscript text **`3XKY2E46`5684** |37,511bytes; SHA-256`0087f287f9fdd4887516d9c99cc70f1b8cf3bc9946c38ed863a5b0e20230880d`. Explicitly labeled tool-indexed text, not original PDF. Lines0–959 merge without gaps/conflicts; three primary figures unviewed. UTF-8 recorded. |
| Selected pinned source **`8U62S98R`5686** |Locally assembled ZIP of eight original C# files plus provenance,11,705bytes; SHA-256`5b9fcdf9eb01ce0f06d69442dbc88fb7149f21b21aeec34172983bd1bfd5bcb4`. This is not a complete repository or author-issued release archive. |

The [indexed author manuscript](https://svit.usj.es/wp-content/uploads/2024/09/Navarro_SPLC_2024_PRE.pdf) has five pages, placeholder DOI/ISBN and template received/revised/accepted dates. Crossref identifies the2September2024 four-page publication and32 references, including an extra reference30 absent from the indexed31-reference list. Final-body correspondence is unverified. Ordinary requests to the observed PDF and short alias return403; a filename-derived migrated API candidate also returns403. Two PDF screenshot attempts fail with cache misses. The linked video is not viewed; AppendixA describes the demonstration plan, not an observed session.

## Published method and observed applications

The manuscript describes component-presence bit vectors, pairwise Manhattan distance, neighbor joining and a Newick/tree viewer. Table1 reports four applications:

| Game | Prefabs | Project size | Reported analysis time |
| --- | ---: | ---: | ---: |
| VTM: Heartless Lullaby |84|3.6GB|1minute|
| Grabitoons! |158|6.5GB|2minutes|
| NeonHAT |1,319|11GB|6minutes|
| Toy Tactics |2,036|134GB|25minutes|

Retain these useful reported applications and the described Canvas cluster in Grabitoons. The inspected text supplies no hardware/repeated-run uncertainty, controlled maintenance comparator or independently verified ancestry. Latent-content generation is attributed to reference9, [Chueca etal.2024](https://doi.org/10.1145/3646548.3672596); it is not a generated-content experiment conducted in this tool paper.

## Public-source coverage and correspondence

The [author landing](https://svit.usj.es/phylogenix/) links two public repositories. Metadata and complete directory inventories resolve:

- [Plugin](https://bitbucket.org/svitusj/phylogenix-plugin), pin`c54a2e9a896305289807b6cd5221cc0f82def1ce`,8July2024:51 entries,34 files/17 directories,18 directory/page requests. The guide and eight selected C# files are acquired and fully read: editor, runner, options, return structure, gene/gene-stripped/encoding structures and pipeline orchestration.
- [Viewer](https://bitbucket.org/svitusj/phylogenix-viewer), pin`d5ca4eb4006288f4eac5b3ada794f2c736ebe10d`,8July2024:105 entries,74 files/31 directories,32 directory/page requests. Inventory only; selected viewer bodies are not acquired/read.

The next source request returns429, including one later retry without a Retry-After header. Further requests stop. Seventeen of26 initially selected files remain unacquired: ten plugin sources and seven viewer files. The next permissible source continuation is to resume the saved list after the rate limit clears, skipping and hash-verifying the nine acquired files. No alternate account or access circumvention is used.

The already acquired [S254 replication package14591668](https://zenodo.org/records/14591668), native parent`GQVDG772`/ZIP`UFTKNWMM`, provides a separate lawful source edition. Its `Phylogenix.unitypackage` SHA-256 is`a8f8c65548d83a8bebcf756e401054c3c3ef0b5cf84f4b3411c34af2b5a573b5`. Passive tar inspection finds32 assets, including29 C# bodies. Twelve newly selected files are read completely: encoding generator; matrix calculator and three distances; pairing; Newick generation; online-viewer adapter; general/file-output utilities; and two pair structures. Six shared modules have identical decoded lines to the pinned repository after BOM/line-ending normalization. Editor/runner differences receive bounded inspection; nine remaining C# bodies are unselected. None of the eight overlapping files is byte-identical, and the two changed modules preclude treating the package as that exact repository release.

## What the inspected package actually computes

| Source location within `Scripts/` | Static reconstruction and consequence |
| --- | --- |
| `Jobs/1Genetic/EncodingGenerator.cs`,62–154,162–193,258–305 | Reads prefab YAML documents and records **component counts**. MonoBehaviour GUID lookup supplies script basenames; nested-prefab source references contribute prefab names. This represents selected serialized structure, not script bodies, field-value behavior or observed execution. Nested references are not recursively expanded into a verified behavioral dependency graph. |
| `Classes/DataStructures/GeneticEncoding.cs`, shared decoded text | Builds the union of component headers, transfers observed integer counts and supplies zero for absent entries. Outlier/percentile code is commented out. There is no active binarization in this inspected path. |
| `Jobs/2Matrix/MatrixCalculator.cs`,79–84; `BaseGeneticDistance.cs`,8–21 | The active distance is **d(x,y)=count of unequal component counts / number of headers**. For binary vectors this is scaled Manhattan distance; for counts,1versus4 contributes one mismatch, not a magnitude of three. Thus the binary/Manhattan description does not fully describe this package. |
| Two alternative distance classes and editor options | Alternative formulas exist, but the inspected calculator directly calls the base distance. The package editor's selection is not passed through its active `RunWithReturn` call. Existence of an option does not establish that these outputs used it. |
| `Jobs/3Pairing/PairingProcess.cs`,30–100,103–167 | Despite the `FindMaxCorrelation` name, it chooses the smallest nonnegative pair distance, merges the pair and replaces distances by the arithmetic mean of the two cluster distances. This inspected path has no row-total correction. Record this direct algorithm reconstruction separately from the manuscript's neighbor-joining label; the original1987 method is a bibliographic dependency, not independently reread or reproduced here. |
| `Jobs/4Output/NewickGenerator.cs`,77–102 | Recursively serializes merged pairs, sanitizes selected punctuation, assigns half the pair distance to leaves and emits pair distances on internal groups. Do not read displayed edge lengths as elapsed development time or independently verified ancestry. |

These are source-derived observations about the acquired S254 package, not evidence that a particular historical run used these bytes. The still-missing pinned encoding/pairing files prevent extending every detail to the July repository. Nor do these observations establish that the tool fails to provide useful organization: related configured objects can still be brought together for inspection. The unresolved questions concern exact method correspondence, interpretation and measured consequences.

## Integration and empirical lineage

The guide requires C#9, .NET Standard2.1 and prefab input; its example screenshot shows Unity2022.3.27f1. It permits selecting another project's assets, with outputs and progress inside the editor. These requirements narrow the paper's generic compatibility language without demonstrating incompatibility with another version.

Both inspected pipelines produce genetics, matrix, pair and Newick files. The package's editor reads the output and posts it to a hosted `/api/tree` endpoint; its browser-open line is commented. The separate online-viewer helper logs a Base64-bearing URL while its own browser-open call is also commented. The pinned repository editor instead opens a different viewer landing and directs manual drag-and-drop. This is a concrete deployment/data-boundary difference, not a reproduced failure or a claim about the current hosted service. No project data is uploaded during this reading. Parsing, names/GUIDs, output files, visualization and hosted-service assumptions belong in the integration account.

The four commercial games recur in S254's later five-game study; Kromaia is the additional proprietary-engine case. Shared game identities are not four new independent cases or proof of identical project snapshots. S262's VTM84 matches the released tree's84 but differs from S254's printed85. NeonHAT is1,319 here,1,318 in S254's figure and1,481 in the released tree. Grabitoons158 and Toy Tactics2,036 agree across these counts. The versions/reasons remain unresolved; no typo/filter explanation is invented. S254's positive participant observations retain their qualitative scope.

## Consequence for Nu

For B03/B04/B10/B12, an adequate comparison includes configured objects and assets, extraction/identity assumptions, cross-tool handoffs and deployment boundaries. A successful source edit or well-typed world does not by itself account for those obligations. Conversely, this existing Unity tooling already offers a useful structural overview; Nu's value needs a concrete change or diagnostic advantage under an explicit work boundary.

S262 narrows an unread-method gap while leaving primary figures, final edition and selected source correspondence open. It contributes no measured Nu benefit and does not close a theme. Follow the direct latent-content primary10.1145/3646548.3672596 and resolve the journal/SSRN lineage10.1016/j.jss.2025.112649 /10.2139/ssrn.5137169 before crediting generative outcomes. Independent Unity-build, temporal/type and contemporary-practice routes remain available under unchanged experimental holds.
