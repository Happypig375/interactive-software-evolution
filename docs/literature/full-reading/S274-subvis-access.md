# S274 — SuBViS: complete primary reading

Daniel MacCormick and Loutfouz Zaman, *SuBViS: The Use of Subjunctive Visual Programming Environments for Exploring Alternatives in Game Development*, FDG 2019, pp. 1–11, [DOI 10.1145/3337722.3337740](https://doi.org/10.1145/3337722.3337740). Complete primary reading, 2026-10-15 HKT.

## Identity, edition, and coverage

Native parent **`BDIULBB9` v5774** and imported attachment **`SPFK8U3V` v6730** were re-fetched before reading. The attachment is the eleven-page published ACM conference paper: 725,534 bytes, PDF 1.7, SHA-256 **`9cbda76d1bc12d4c66b8b5b3fdf0a4571f292cec3bad45f0f1d4bf19b2d31659`**. Its title, authors, venue, dates, pagination, and DOI match the registered record on page 1.

All eleven physical pages were read. Visual coverage includes all ten numbered figures and Table 1: the Blueprint graphs and tab controls in Figures 1–8, the prepared target/crate scenes in Figure 9, the full response-distribution chart in Figure 10, and the participant-order matrix in Table 1. There is no appendix. References on page 11 were checked for the method lineage. No engine, source, prototype, or participant procedure was reproduced.

## What SuBViS represents

SuBViS modifies Unreal Engine's source and turns a Blueprint from a single-state document into a multi-state graph. It exposes the same tab-like create/delete/select interaction at two scopes (pp. 3–4):

- A **node alternative** duplicates the active node state. Each state stores values in the node's input fields and enough output-connection information to reproduce its outgoing connections. Later edits to one state do not affect the others. The intended use is a small parameter or expression change, such as colour values.
- A **graph alternative** duplicates every node in the active graph into an independent graph state. The user may then add/delete nodes, rewire connections, or replace the whole algorithm.
- The scopes can be nested, but node alternatives in one graph alternative are independent of node alternatives in another. The currently active graph/node combination alone is compiled; inactive alternatives are not compiled (p. 4).

This is versioned authoring state, not retained running-game state. The study exposed that switching the visible alternative did not change behaviour while the game was running, switching did not mark the Blueprint dirty for automatic compilation, and participants had to stop and manually compile (pp. 9–10). Multiple alternatives also could not be viewed side by side at runtime. The paper proposes parallel game instances as future work; it does not implement live state transfer, runtime hot swapping, or reconstruction of an actor's transient state.

The FPS use case is a worked demonstration, not an observed team study (pp. 4–7). Four graph alternatives preserve static, clockwise-circle, alternating-circle, and square target movement; three node alternatives preserve green, cyan, and magenta hit-feedback values. The authors contrast these with Blueprint duplication, inheritance, conditional branches, and instance-editable variables. Their communication claim is hypothetical: quick tab switching could reduce demonstration downtime, but the paper measures neither communication nor team work.

## Preliminary study

The study's stated aims were to gather initial impressions and choose a design for a later evaluation, rather than estimate production benefit (p. 7).

- **Participants:** four unpaid men from technical undergraduate/graduate programmes, ages 20–25 (M 22.5, SD 2). They reported strong traditional-programming experience (M 6.25/7), flowchart experience (M 5.25/7), little Unreal experience (M 2.00/7), and mixed Unity experience; all used Unity regularly (p. 7).
- **Apparatus and assistance:** a Windows workstation with dual monitors; both displays were recorded. Participants completed a short Unreal tutorial. Each prepared Blueprint began with no behaviour but included optional hint nodes and an organizer area. The investigator demonstrated relevant operations, collected think-aloud comments, and took notes (pp. 7–8).
- **Assignment:** every participant used SuBViS for one task and base Unreal for the other. The four cells counterbalanced system order and target/crate order exactly once (Table 1, p. 8). The first task required three investigator-specified behaviours; the second required three participant-chosen behaviours. Thus system, object, order, and constrained/open task were balanced across four people but not repeated within the same person/task.
- **Outcomes:** after each task participants rated efficiency, ease of use, future use, and overall impression on seven-point items. Observation, think-aloud, and a final semi-structured interview supplied the remaining evidence. Sessions averaged about 1.5 hours (p. 8). The paper reports no completion-time comparison, error/correctness measure, code-quality measure, or inferential test.

Figure 10 shows SuBViS rated equal to or above base Unreal in all four categories, but only four responses contribute to each row and exact means are not tabulated (p. 8). The strongest useful findings are behavioral and adverse as well as favorable:

- Participants used node alternatives only twice, for a particle-system parameter and a magnet-force sign/value. P3 judged them useful mainly for the few nodes with many parameters (pp. 8–9).
- All four understood the browser-tab metaphor; requested changes included names, a smaller delete control, and tutorial widgets (p. 9).
- In base Unreal they either connected all alternatives into one behaviour or rewired conditional execution. In SuBViS two workflows emerged: modify the duplicated prior graph, or delete the copy and start a substantially different graph. The latter group wanted a choice between “copy active” and “start blank” (p. 9).
- Safe trial-and-error and preservation of earlier graph work were valued. This supports a perceived authoring-safety mechanism, not an objective productivity effect (p. 9).
- Every participant encountered the missing automatic-recompile behavior at least once. One participant repeatedly switched tabs while the old runtime behaviour continued. Lack of simultaneous runtime comparison was another observed limitation (pp. 9–10).

The authors therefore recommend a larger longitudinal study with experienced users working creatively over weeks. They explicitly say the tiny sample and participants' initial Unreal learning limit confident conclusions (p. 10).

## Relationship to BPAlt and scoped implications

BPAlt (S275) cites SuBViS as its earlier node-based game-development work. The shared second author and explicit citation establish tool-lineage continuity. BPAlt is nevertheless a different implementation and separately reports a ten-person study, while SuBViS reports four participants. Neither paper identifies participants or states whether any person appeared in both studies, so person-level overlap is unknown. The papers do not present BPAlt as an independent replication, and the two samples must not be pooled.

For the Nu agenda, SuBViS is a concrete alternative-authoring comparator for R12/R20: it shows that copying an active representation can reduce fear of destructive graph edits while introducing representation-management and compilation costs. Its negative observations are directly useful for R10/R03 boundaries: an editor selection is not a runtime switch, and preserved graph variants are not preserved execution state. The study does not establish merge correctness, whole-program behavior, retained runtime state, team handoff benefit, longitudinal productivity, or a professional deployment effect.

## Preserved access history

The 2026-10-05 reconstruction had only abstract and metadata coverage. Scite's exact-DOI request returned one record but its body endpoint returned zero characters with `contentDenied: true`; the ordinary ACM PDF route returned 403/HTML, and OpenAlex exposed only the closed publisher location. Exact-title/author searches found author listings and a public abstract but no body. Native text attachment **`S8HMSM2F` v5768** preserves that abstract-only capture (1,275 bytes; SHA-256 **`a61777be55796439be9b4567dcab229862d888f8d5dc3aa2309bb88e765eac42`**). Those historical denials remain accurate for those dated routes; the later imported PDF supersedes the old current-access gap.
