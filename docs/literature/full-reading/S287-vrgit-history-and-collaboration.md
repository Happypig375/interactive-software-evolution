# S287 — VRGit: operation history, selective reuse and collaborative authoring

**Work:** Lei Zhang, Ashutosh Agrawal, Steve Oney and Anhong Guo, *VRGit: A Version Control System for Collaborative Content Creation in Virtual Reality*, CHI 2023, 1–14. [DOI10.1145/3544548.3581136](https://doi.org/10.1145/3544548.3581136).

**Disposition:** complete selected-paper reading. VRGit demonstrates operation-history navigation, branching, previews and selective object reuse in a collaborative VR editor. Fourteen participants completed its instructed tasks and reported favorable usefulness, alongside navigation and control-awareness difficulties. This is exploratory usability evidence without a control condition. It adds an alternative way to exploit history; it does not estimate a Nu benefit, automatically merge all branch changes or establish preservation of a running game's behavior.

## Identity and actual coverage

The [author-hosted paper](https://raynez.art/papers/CHI23-VRGit.pdf), linked from [Lei Zhang's publication page](https://raynez.art/bio/), has **14 pages, 14,681,004 bytes**, SHA256 **`af586c49d702c31946e6bbc456784a2cd2b8439b3ef8ac34b5f41be8d9424dbc`**. All fourteen text pages and all fourteen rendered page images were inspected, including **seven figures, Table 1, 80 references and Appendix A's instruments**. All 112,025 extracted characters were read; column order and numerical/diagram interpretation were checked against the page images. Poppler emitted a Symbol-font warning, but the displayed comparison marks and text were legible. Extraction and rendering are inspection, not system execution.

The PDF identifies CHI 2023, the four authors and the exact DOI; its metadata dates creation to 2023-02-20. Crossref gives publication on 2023-04-19 and fourteen pages. This is a complete author-hosted publication-formatted copy; byte equivalence to a separately downloaded publisher copy was not tested. Native collection **`PKLXQNEE`** parent **`JML8HU52`** and note **`3IZN269C`** existed before selected reading. Attachment **`9SQPQ7CN`**, version5900, passed native byte/hash readback. Final object versions are in the search ledger.

The author links a [demonstration video](https://www.youtube.com/watch?v=xI7TAAJdlTA). The web reader failed with a cache miss, while an ordinary request obtained the HTML page. The media and audio were not acquired or reviewed; this is an explicit supplement gap, not proof that the video is inaccessible. No source code, application, raw response data or recorded sessions were acquired or executed. Copyrighted bodies, renders, extraction and local audit receipts remain ignored.

## Represented state and history operations

Sections 3.1–3.2, pp.4–6, instantiate the method as a fixed-scale apartment editor with premade furniture. The underlying directed acyclic graph records editing operations and their parameters; edges encode temporal order. Creation, transformation and deletion are the authoring operations. A separate displayed History Graph summarizes the underlying operations and uses miniatures of scene versions. These layers must not be conflated: a summarized node need not represent only one underlying operation.

| Operation | Paper's contract | Consequence for comparison with Nu |
| --- | --- | --- |
| Commit and display history, §3.2.1–2, Figs.3–4 | Record edits automatically. Group displayed history using idle thresholds, available display space and collaborator locations. Defaults are ten seconds alone and fifteen collaboratively, chosen anecdotally. Always expose versions occupied by collaborators. | The described “operation dependencies” use an idle-time heuristic. This does not establish semantic independence or a behavior-preserving grouping rule. |
| Navigate and branch, §3.2.1–2 | Entering a version changes the environment layout to that version. Branching copies the historical operation node, attaches the copy to its parent and switches the user to the new branch. | This reconstructs represented scene-edit history. The paper supplies no contract for migrating code, stack frames, pending game events/timers or irreversible external effects. |
| Compare, §3.2.1 and Table1 | Miniatures color additions green, transformations yellow and deletions red; users can inspect larger previews. Table1 explicitly qualifies its diff mark as visual comparison. | A visual comparison is a useful inspection aid; it is not a semantic equivalence or conflict oracle. |
| Reuse, §3.2.3, Fig.5 | Select an object in a version preview and bring it into the current version with its position, rotation and scale. Multiple previews permit selections from several versions. The illustrated reuse creates another commit. | Table1 qualifies its merge mark as content reuse. This is a different integration contract from NodeGit or LevelMerge's branch-diff combination; retaining every change is not its goal. |

The Appendix uses “merge objects” in survey questions. That wording does not override §3.2.3's selective-reuse mechanism. The paper's contrast with conventional whole-branch merging motivates its design; it is not an exhaustive account of all available Git selection workflows. No source reconstruction here establishes object-ID generation, concurrent same-object conflict arbitration or referential-closure checking.

## Collaboration and integration obligations

Sections 3.3–3.4, pp.6–8, allow users in the same version to edit together, see avatars/raycasts and speak. Users in separate versions retain awareness through mini-avatars in history and movable portals showing collaborators' first-person video. Previews offer a manipulable overview, while portals follow another person's view; participants valued both and described cases in which a preview was preferable.

Shared history moves the visualization from users' arms to a common location. One sharer controls navigation, branching and preview/reuse actions; sharees follow the resulting view and version changes. This explicit control allocation helps coordinate discussion but also produced confusion about who could act. It is not evidence of a fully symmetric concurrent-control protocol.

The described implementation uses Unity2020.2.7 with Oculus Quest/Rift, Photon Voice for audio, Firebase documents for avatars/operations and WebRTC-encoded portal video. Five synchronized operation types are named: creation, transformation, deletion, entering and branching. Shared-history operations flow from the sharer to sharees. Figure7 distinguishes these communication paths; it supplies no latency, consistency, recovery or resource-cost benchmark. Extending this authoring environment requires the represented-operation and collaboration services, not only retaining immutable snapshots. The paper explicitly leaves offline asynchronous use, larger teams/history, mesh-level operations and other task settings unresolved.

## Evaluation and scoped positive findings

Section4, pp.8–9, recruits **14 university participants, seven pairs**, ages20–28, all with prior VR experience; three pairs were friends and four were strangers. They receive $30 for approximately two hours. The collaborative session includes the first author acting as a client alongside the two participants. This is seven participant pairs with researcher involvement, not 21 independently recruited users or a field study of professional interior designers.

All participants receive about thirty minutes of introduction and atomic-task practice. An individual task of roughly fifteen minutes requires reproducing a displayed layout, returning to history, creating two branches and reusing an experimenter-selected object. After a break and collaboration instructions, a roughly thirty-minute task gives the two users different furnishing/arrangement information, incrementally every two minutes, to encourage communication. The researcher then requests a combined design and encourages shared-history use. These are deliberately elicited feature uses. The reported durations describe the protocol; they are not comparative task-time outcomes.

The study collects seven-point ratings and individual retrospective interviews. AppendixA contains three pre-task questions, eleven PartI rating items and twenty-one PartII items. The paper says recordings were transcribed and coded but does not supply a complete coding protocol, raw responses or all per-item distributions. Sections5–6 report that everyone completed the tasks. Representative means and standard deviations preserve both favorable and difficult aspects:

| Reported rating, seven-point scale | Mean (SD) |
| --- | ---: |
| Track design evolution / see consecutive-version changes | 6.2 (0.6) / 5.9 (1.0) |
| Navigate/enter versions: ease / usefulness | 4.4 (1.7) / 6.4 (0.7) |
| Create branches: ease / usefulness | 5.6 (1.2) / 6.1 (1.1) |
| Preview: ease / usefulness | 5.2 (1.7) / 6.3 (0.6) |
| Reuse objects: ease / usefulness | 5.6 (1.4) / 6.5 (0.7) |
| Portal usefulness / shared-history usefulness | 6.3 (0.9) / 6.4 (0.8) |
| Natural communication / collaboration enjoyment | 6.4 (0.6) / 5.6 (1.3) |

Interview accounts support perceived ease of comparing variants, returning to earlier designs, retaining selected arrangements and discussing a shared visual reference. They also identify controller-memory burden, difficulty navigating longer histories, restricted portal viewpoints and unclear sharing control. These are useful observed usability findings. Retrospective comparisons with Git/Photoshop are participant reports, not assigned comparison conditions. There is **no measured treatment contrast, net maintenance-time effect, design-quality advantage or correctness/consistency benchmark**. Section6.6 explicitly proposes a control condition and further correctness/scalability evaluation. Possible novelty and researcher-response effects are acknowledged; those limits do not erase successful task use or positive ratings.

## Consequence for the wider survey

Reuse [S283 NCCollab](S283-nccollab-collaboration-history.md), [S284 LevelMerge](S284-levelmerge-scene-merge.md) and [S286 NodeGit](S286-nodegit-source-and-access.md) with their distinct evidence scopes. VRGit adds a clear distinction among **retaining operations, showing history, selecting material for reuse, combining branch edits and preserving intended running behavior**. Favorable ease/usefulness for one of these cannot substitute for another's correctness or comparative lifecycle benefit.

For Nu, the useful question becomes which represented changes and collaboration obligations its actual mechanisms support, which users need them and what total work they save or introduce. A history representation alone does not answer that. The next consequential route is **Krauß et al.'s professional collaborative AR/VR development study, DOI10.1145/3411764.3445335**, recovered as reference40 and by exact search: its reported 26-professional population makes real workflow, tool handoff and integration burdens the specific next uncertainty. Register/reuse before body reading. The Ashtari2020 practice predecessor, modern CAD version-control practice, Spacetime, FlowMatic and creative-version-control work remain conditional dependencies, not a required reading quota. None of these discoveries establishes a Nu effect or authorizes construction.

## Discovery and audit boundary

SC224 requests limit20 and returns the one exact VRGit DOI. SC225's incoming graph reaches its twenty-edge cap; SC226 raises the graph cap to60 and returns46 edges/47 nodes without truncation or a low-coverage flag. All returned edges point from citing work to VRGit. Seven edges supply contexts; those describe related work, design precedents or workflow considerations, not a VRGit replication. One incoming DOI has no returned title. Three matching-title publication/preprint pairs remain separate identifiers pending edition binding.

All80 printed bibliography entries were screened at reference/context scope and aligned by reference number with the deposit's80 records;72 contain deposited DOIs. This is not independent DOI/title verification or primary reading of80 sources. SC227 requests limit20 for three practice-study DOIs and returns3/3, with a truncated Krauß abstract and three outgoing citation snippets. These are selection evidence only. W719–W721 inspect the author route and paper/video links; the ordinary PDF acquisition succeeds despite the web reader's size limit. The local considered-source roster retains repetitions, historical reuse and conditional/not-used decisions. The search ledger records the inspected citation-report result.

Audit **`nu_background_s287_20261008`** records174 occurrences,141 distinct source identities and dispositions2C/118D/21N. The175-file historical check finds12 matches: VRGit receives one material full-reading update and eleven unchanged screens are withheld. The130 submitted decisions comprise2 credited and128 not credited (110 deferred,18 outside the selected question), with129 reference/discovery screens and one full-paper reading. Receipt and inspected report each match all780 checked fields; zero skips, missing reasons, linkage warnings or truncation. The answer-scoped retrieved count is null. These are audit identities, not141 independently verified studies.

All experimental and worker holds remain. No model, candidate, engine, benchmark or reproduction was run.
