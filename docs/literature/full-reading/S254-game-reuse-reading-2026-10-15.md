# S254 — Prefab reuse across two game studios and five projects

Jose Ignacio Trasobares, África Domingo, Rodrigo Casamayor, Daniel Blasco and Carlos Cetina, *A multiple case study on reuse in Game Software Engineering*, *Information and Software Technology* 185 (2025), article 107781. [DOI 10.1016/j.infsof.2025.107781](https://doi.org/10.1016/j.infsof.2025.107781).

**Complete final-publication reading, 2026-10-15:** all 14 journal-layout pages are read textually and inspected visually. Coverage includes Tables 1–5; Figures 1–7; every result, discussion, validity and conclusion section; publication dates and funding/competing-interest statements; and all 41 references. Figure 3's five full phylogenetic trees are inspected as overviews with their printed counts, and Figures 4–7's selected branches and labels are legible; this does not claim exhaustive reading of thousands of tiny Figure 3 leaf labels. Existing replication-package instruments and tree-count checks remain separately documented in [the earlier partial note](S254-game-reuse-cases-partial.md). No code or plugin was executed and no qualitative material was recoded.

## Final edition, native record and lineage

Before reading, Zotero parent **`GQVDG772`** version 5569 was verified in collection `PKLXQNEE` as the five-author `journalArticle`, volume 185, September 2025, article 107781, DOI `10.1016/j.infsof.2025.107781`. Existing publisher attachment **`UCRAGLXA`** version 6693 is **4,746,029 bytes**, 14 pages, SHA256 **`ca0c6a87f27ce065128e9436139b103e222359d4b07b1557b515c845289abf9b`**, unencrypted PDF 1.7. Page 1 visibly supplies the exact title/authors, final DOI, received date 4 October 2024, revised date 25 March 2025, acceptance 6 May and online availability 22 May 2025. No Zotero record or attachment was changed.

The final body substantively confirms the March 2025 indexed preprint reconstructed earlier while closing the publisher-layout and visual gaps. It is 14 pages rather than the preprint's 16 and is not byte-identical to the 12-page SSRN listing or indexed derivative. The final paper retains the same two studios, five projects, four participants, phase structure, prefab findings and replication-package route. It also retains several internal inconsistencies described below, so publication status does not resolve them silently. Private final extraction and 14 rendered pages are under `.artifacts/s253-s254-reading-20261015/`; source bytes and renders do not enter Git.

## Cases, people and project units

The multiple case design has two company contexts with embedded game units (Figures 1–2; Tables 3–5):

| Context | Company and games | Project facts in the final tables |
| --- | --- | --- |
| Kraken Empire | Kromaia; Toy Tactics | Founded 2011; four current developers, peak twelve; three own games plus work on 32 games. Kromaia used a proprietary C++ engine, two developers, 48 months and 145,000 lines. Toy Tactics used Unity/C#, twelve developers, 72 months and 128,000 lines. |
| Entalto Studios | NeonHAT; Grabitoons!; VTM: Heartless Lullaby | Founded 2021; six current developers, peak eight; three own games plus work on 13 games. All three selected projects used Unity; reported durations are ten, twelve and two months, with 89,138, 46,053 and 20,758 lines respectively. |

These are purposively selected small indie studios and projects across genres, engines and platforms. They are not five independent experiments, a matched Unity-versus-proprietary-engine comparison or a representative prevalence sample. Repeated questionnaires, trees, focus groups and observations about one project remain evidence about that project.

Four developers participated. KR1, a 40–50-year-old director/project leader, reports 20 years developing software and 18 developing games. KR2 is a 25–30-year-old developer with one reported software year and three game years. EN1 is a 25–30-year-old manager/lead developer with four years in both; EN2 is a 25–30-year-old developer with six years in both (Table 5). KR1 and EN1 participated in all phases; KR2 and EN2 in Phases II–III. These four viewpoints cover different roles and experience but do not estimate studio populations, designer productivity or newcomer learning.

## Three-phase method and actual evidence

Phase I sent a general questionnaire and consent form to one representative from each studio, KR1 and EN1, then used their responses to prepare semi-structured interviews. It supplied two questionnaire responses, interview transcripts and researchers' notes for general reuse questions.

Phase II analyzed the five project repositories with Phylogenix and sent each project tree with a game-specific questionnaire. One or two developers who had worked on each game interpreted its reuse patterns. The paper reports **seven specific responses**: one Kromaia, two Toy Tactics, one Grabitoons!, two VTM and one NeonHAT. Code and inferred trees support structural discussion; they are not runtime tests, verified maintenance outcomes or chronological histories.

Phase III held one focus group per company after the team prepared preliminary results. It also visited Entalto, where four employees were working; two had participated in the focus group. The visit used an observation sheet to understand work dynamics and daily tools. The final evidence inventory is thus two general responses/interviews, seven project responses, five source/tree analyses, two focus groups and one studio visit, not an unspecified large interview population (pp. 4–6, Table 2).

The authors report data-source, observer and methodological triangulation. Three researchers participated in interviews and focus groups with different management, recording/transcription and protocol roles; they debriefed after phases, and final conclusions/dissemination material went to participants for member checking (p. 12). The replication package provides instruments, consent/ethics materials, observation sheet, tree tool and trees. It does not provide complete interview/focus-group transcripts, all responses, coding decisions, project source snapshots or change outcomes.

The Phase I instruments explicitly prompted prefabs/scripts, clone-and-own, planned reuse, architecture tools, advantages and disadvantages, initial effort, claimed savings, project/team conditions and generative AI, as the earlier package reading records. The concepts did not all emerge without prompting. The study's static trees and directed questions are an elicitation package, not a neutral discovery instrument.

## Reported reuse mechanisms, benefits and costs

Participants named classes, scripts, design patterns, engine editors, IDEs, custom tools and especially **prefabs**. One studio's bespoke level editor let a designer author more races/levels without implementation detail and reportedly with fewer mistakes than hand authoring. Unity prefabs centralized configured GameObjects, properties, components and children; scripts could be shared across prefabs. The paper relates similar concepts to Unreal Blueprint Classes, Godot scenes and Kromaia's XML reusable units (pp. 7–9). These similarities support a cross-engine comparator family, not semantic equivalence among the systems.

Reported motivations include agility, faster or more efficient development, product quality, reduced late technical debt and easier maintenance. Reported costs include upfront design/implementation of reusable mechanisms, the risk that reuse work is inappropriate for a one-off element, pressure to ship an ad hoc solution, and unintended error propagation. Participants also emphasized team knowledge of the environment, prefabs, inheritance, composition and design patterns (pp. 7–8). These are experience accounts. The study does not measure saved hours, defect rates, completed changes, break-even reuse count or an assigned reuse intervention.

No participating subject reported using generative AI or automatic code generation for prefab elements, and the printed quote is negative about then-perceived code/art quality (pp. 7–8). This is evidence about four developers in the study period, not a current adoption estimate or capability comparison.

Within-game prefab reuse is the central unit. Participants described reusing configured objects, behavior, assets and level elements. Cross-project reuse was reported as only **2–5%** when asked about reuse from own projects, external sources or stores, with unique mechanics and artistic styles offered as reasons. Same-franchise or platform-version reuse was identified as plausible, but not analyzed as a completed comparison (p. 9). The percentage is a participant estimate with unresolved denominator, not source-measured reuse or saved effort. The replication instrument contains other project-specific percentages whose correspondence remains unresolved; none should replace the final 2–5% summary by assumption.

## What the tree discussion contributes

Figure 3 prints five inferred trees and counts: Kromaia 86 prefabs, Toy Tactics 2,036, NeonHAT 1,318, Grabitoons! 158 and VTM 85. The figures support visual inspection of differently shaped clusters; they do not establish chronological ancestry. The paper explicitly defines “evolution” as inferred shared/differentiating characteristics and states that tree paths are neither necessarily linear nor directly tied to temporal succession (p. 4).

Developers recognized related score objects, dog variants, walls and effects in Figures 4–6. They also found relations they did not understand, saw redundancy and recalled bugs/technical debt. Figure 7 highlights long NeonHAT branches that a developer thought might be reducible. Participants identified unused VFX and an abandoned portal mechanic as **dead prefabs** that add complexity and maintenance overhead (pp. 9–11). These are concrete qualitative observations aided by the visualization; no participant was assigned a repair, and no before/after change time, correctness or maintenance saving was measured.

The final publication preserves the earlier package discrepancies. Passive parsing of released Newick/SVG assets found 86, 2,036 and 158 leaves for Kromaia, Toy Tactics and Grabitoons!, agreeing with Figure 3, but 1,481 for NeonHAT versus the printed 1,318 and 84 for VTM versus the printed 85. The source/version or filtering cause is not established. Tree similarity, participant-perceived reuse percentage, chronological lineage and actual maintenance benefit remain different constructs.

## Final-edition inconsistencies and limits

Several reporting problems matter for participant-level or quantitative reuse claims:

- Phase II prose assigns EN identifiers to Kraken games and KR identifiers to Entalto games, reversing the explicit company/participant identities in Figures 1–2 and Tables 3–5. The seven response counts are retained, but individual attribution is not repaired from context.
- The validity section calls the involvement “approximately ten weeks” and then lists five, four and three weeks, totaling twelve.
- The Discussion prints the same technologies/tools wording for RQ1 and RQ2, even though the original RQ2 asks what distinguishes game reuse from other contexts; the subsequent answer addresses prefab distinctiveness.
- Figure 3/package prefab counts disagree for NeonHAT and VTM, and package prompts expose unreconciled percentage denominators.

The main external-validity limit is explicit: two small indie companies, five purposively selected projects and four active participants. Multiple evidence sources and member checking strengthen the situated account; they do not make the cases representative. The authors appeal to indie-release share for context, which does not establish that these studios, workflows or reuse practices represent the population of releases.

The study observes real repositories and studio accounts but does not compare reuse against no reuse, another authoring mechanism or an independently defined maintenance task. “Fewer mistakes,” easier maintenance, reduced debt and useful tree insights are reported or interpreted benefits. Runtime behavior, asset correctness, total team work and cross-project portability are not independently scored.

## Consequence for R12 and R14

S254 strengthens the practical basis for treating a configured entity/object tree as a consequential reuse unit. Game reuse includes properties, nested children, scripts, visual assets and editor-authored configuration. A credible Nu R12 comparator should therefore credit ordinary engine prefabs/scenes/Blueprints and helper/script composition, and should test matched behavior and intended instance variation rather than count declarations.

The evidence reinforces R12's separation among **configuration**, **family revision** and **vocabulary extension**. The favorable level-editor account concerns supported configuration by a designer. Upfront reusable-tool construction and team expertise belong in costs. Redundancy, propagated bugs, dead prefabs and misunderstood relationships show that family revision and cleanup can remain costly. The paper does not establish that Nu's propagation policy solves those problems, preserves author intent or reduces total work.

For R14, prefab relationships, external assets, editor configuration and project-specific mechanics broaden task provenance beyond source-only changes. The two studios provide real beneficiaries and adverse cases, but no common task frequency or independent effect. An authored prefab/entity-tree case remains a purposive mechanism test unless tied to a concrete maintenance decision and supported behavior. Cross-game reuse was uncommon in these accounts, so amortization should use actual declared variants within a project or family rather than hypothetical unlimited games.

The tree findings may justify relationship visibility as a diagnostic condition in a later selected case. A visualization event or recognized cluster is not a completed repair, and a static inferred relationship is not provenance or temporal evolution. Any comparison must measure independently specified new and retained behavior, asset/configuration correctness, assistance, integration, repair and all setup work.

This final reading resolves S254's publisher-body and main-figure gap while retaining raw-response, source-snapshot and package-correspondence limits. It adds no independent games beyond the already registered work lineage and author package. No code execution, participant study, new search or Zotero mutation was performed.
