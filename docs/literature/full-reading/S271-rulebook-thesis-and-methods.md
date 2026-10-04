# S271 — Rulebook thesis, requirements and original evaluation methods

Wilson Kazuo Mizutani, *The Unlimited Rulebook: Architecting the Economy Mechanics of Games*, computer-science doctoral thesis, Universidade de São Paulo, 2021; advisor Fabio Kon. [DOI 10.11606/T.45.2021.tde-22122021-205515](https://doi.org/10.11606/T.45.2021.tde-22122021-205515). Main-agent reconstruction, 2026-10-05 HKT. **All 191 PDF pages read as text; 94 pages inspected visually, covering all 50 figures, 14 tables, three listings and both appendices.** All 99 references and 40 ludography entries read. The separate eleven-page interview protocol is read completely in text and visually. One thesis publication credit; related papers and reused cases are not independent replications. Page references below are PDF page numbers.

## Identity, access and actual coverage

Collection `PKLXQNEE` had 300 parents before registration; DOI/title/edition checks found no existing thesis match. Native parent **`VY3FT5TX`5745** and note **`YVLKA4TY`5746** preceded selected reading. Three attachments retain distinct identities:

| Attachment and source | Verified identity |
| --- | --- |
| `64YJKF87`, [author-hosted corrected thesis](https://www.ime.usp.br/~kazuo/thesis/Mizutani-The_Unlimited_Rulebook.pdf) | 191 pages, **26,090,775 bytes**; SHA-256 **`80ebc5d9828ba60aad5036b62228eed743d41d338d999e7240312bda369c9a9d`**; MD5 `11bcb72a16f687822798facdeabfe731`. PDF creation/modification 2022-03-31. |
| `EQTPC8GB`, [USP repository corrected thesis](https://www.teses.usp.br/teses/disponiveis/45/45134/tde-22122021-205515/publico/texto.pdf) | 191 pages, **26,722,768 bytes**; SHA-256 **`adac9d0bf1c0045797021a26ecdd74870fe811c8cd390d291f97f98fbc5df953`**; MD5 `bbd63b3e2e1b3ac384fba86ade0decd8`. PDF creation/modification 2021-12-06. |
| `4FSGB37H`, [public interview protocol](https://www.ime.usp.br/~kazuo/thesis/InterviewProtocol.pdf) | Eleven pages, **75,782 bytes**; SHA-256 **`dd0af95c7082325f5b0cd550a5e081e766c4412ca3489a6634b94f24cf75effa`**; MD5 `6f750e254080a5c36cb09820dd9b4c72`. Cover dated August 2020; no PDF creation timestamp. |

The thesis cover says September 2021; the corrected-version statement records defense on 20 October 2021. Crossref's January 2022 registration is not the thesis publication date. The original pre-defense submission is unacquired. Ordinary USP access first disconnected; a short curl attempt returned an incomplete 3,271,948-byte file. A longer ordinary request acquired all 26,722,768 bytes. The partial file was never credited as complete. The USP file opens normally despite its encryption metadata; no bypass was used.

Passive comparison of **all 191 pages**, using sorted text and rendered pixels, finds 190 identical pages by each comparison. Only page 2 differs: the committee member's surname changes from “Scachci” in the repository file to “Scacchi” in the author file. This supports equivalence of the inspected body and figures, while preserving different file hashes and metadata. It does not establish correspondence with the unacquired original submission.

Text coverage includes front matter, Chapters 1–7, Appendices A/B, references and ludography. Visual coverage includes every listed figure/table/listing and the fourteen-page Table B.1; it is not a claim that all 191 pages received visual inspection. Protocol colors and strike-throughs were inspected because extraction alone loses question revisions. Native bytes match the recorded hashes. Two initially mislabeled attachment titles were corrected with version guards, preserving their keys, parents, files and URLs. Bodies, extraction and local comparison outputs remain outside Git.

## What the thesis contributes and how the studies relate

Chapters 1–3 and 7 present reference-architecture knowledge for games with economy mechanics, particularly mechanics that amend other rules. The contribution synthesizes established architectural and game-design ideas. Page 155 explicitly rejects the implication that every constituent idea is unprecedented. Gregory, Plummer, predicate dispatch, adaptive object models, Inform7/Qud practice, Magic and Nomic are acknowledged inputs.

Three iterations revisit ProSA-RA's source investigation, architectural analysis, synthesis and evaluation. The 2019 requirements paper precedes [S269's 2020 conference architecture](S269-unlimited-rulebook-architecture.md); this thesis adds the third iteration and detailed methods; [S270's later journal account](S270-rulebook-effects-and-jam-games.md) develops the pattern and jam cases. The course participants and early proof of concept overlap S269. Legend of Slime already appears on page 156 and is the same case later included in S270. These are related publications, not additional independent trials.

Page 58 describes empirical evaluation as complementing a reference-architecture checklist, while page 126 says it replaced the embedded-systems checklist. Page 158 proposes future expert feedback using FERA. No completed FERA evaluation is reconstructed here. Likewise, the Backdoor Route architectural analysis and systematic Grimoire commit-history analysis are future work on page 158; a prior chapter's proposed validation role does not turn them into completed studies.

## Requirements: useful coverage, with interpretive provenance

Chapters 3–4 and Appendix B derive **33 requirements** across ten groups:

| Area | Requirement groups and counts | Consequence for the comparison |
| --- | --- | --- |
| Mechanics | Object model 3; simulation progress 4; behavior model 4; simulation generality 1 | Entity lifetimes, state composition, actions and rule amendment need explicit contracts. |
| Integration | Inter-system communication 4; runtime lifecycle 4; technical compatibility 3 | Events, references, asynchronous engine work, persistence checkpoints, world chunks and platform/data-format dependencies contribute to the design. |
| Iteration | Creative process 3; data-driven design 2; code evolution 5 | Builds, editors, hotloading, change propagation, testing and error handling belong in the cost account. |

The requirements come from selected publication sections, interviews, author experience and games matched to the evolving requirements. The authors did not play every listed game. Table B.1 provides publication/game/USPGameDev source columns; it does not give an interview-ID-to-requirement coding map. Blank cells are not evidence that an architecture lacks a property. This is an interpretive reference framework, not a representative industry vote or an independently exhaustive specification.

RCP3's hotloading requirement does not establish implemented migration of arbitrary code, schemas or suspended work. RCE5 combines compiler/static feedback, tests and runtime recovery; that proposal does not make a cleared diagnostic proof of a semantic obligation. Use these requirements to question Nu's actual coverage, without certifying that Nu or Rulebook implements all 33.

## Professional interviews and the public instrument

Pages 64–66 and 160–165 describe **four active professional developers from different companies**, recruited mainly through accessible contacts with an aim for varied settings. They report existing architecture and change practice, not an intervention adopting Rulebook. Experience is reported as four, eight, four and eight years.

| Published case | Architecture/change account | Favorable and adverse evidence retained |
| --- | --- | --- |
| **I01: mobile idle game**, team roughly 5–10; two-month initial development followed by over five years of updates | In-house engine fork, object-oriented structures, hardcoded tables, field-by-field copying and periodic resource properties | Familiar mechanisms support a long-lived product; rewrite cost is considered unaffordable, and hidden collateral API behavior burdens onboarding. |
| **I02: PC/console action RPG**, own team ten within a project over 200; approximately two years in progress | Legacy hierarchies, globals/singletons, modifier stacks, predicates and synchronous/asynchronous events | Experienced colleagues help newcomers despite stale documentation. Widespread state access, duplication and accumulated debt make refactoring difficult. |
| **I03: mobile real-time strategy/card game**, team eight | Cocos2d-x, ECS, JSON, a large object factory and commands scheduled ahead for deterministic behavior; no self-amending rules reported | Factory maintenance costs are acknowledged, but retaining it is judged cheaper than refactoring. Architectural culture improves as the project gains recognition. |
| **I04: PC MMORPG**, ten engineers | An inheritance-based prototype is discarded; the later Unity design uses ECS, interpreters and visual ability tools | Working-game enthusiasm delays redesign. The developer reports about a month to become accustomed to ECS; this is not a timed comparative result. The final implementation of some effects is unknown. |

Table 3.7 and Appendix A differ on some company sizes: I02 is printed as over 10,000 versus over 1,800; I03 as 500–100 versus 500–1,000. These discrepancies do not erase the architecture accounts, and are not silently resolved into precise population data. The appendix distinguishes unknown and inapplicable answers; missing details remain missing.

The eleven-page protocol asks for concrete addition workflows, actions and parameters, asynchronous feedback, redesign decisions, reasons to defer fixes, onboarding, testing and company culture. Its approximately one-hour target and invitation's 45–60 minutes are planned durations, not measured session lengths. Questions explicitly evolve after I01, including triggers, resource modifiers and rule modifiers. Visual revision marks remove some interview-setting advice and an earlier broad architecture question; the final instrument cannot be treated as uniform question exposure.

The protocol proposes a grounded-theory approach. The public thesis/protocol supply structured summaries rather than raw transcripts, a coding tree, a saturation account or intercoder results. Interview consent and anonymization are reported by the author; no transcripts, recordings, participant identities or private communications were accessed. No participant contact was made.

## Course evaluation: the original instruments narrow the cost claim

Pages 131–137 describe the **same six-person pilot and 28-person main course** summarized in S269. The public summer course ran for two months with two four-hour sessions a week and twenty available places; the semester undergraduate course had two two-hour sessions a week, forty places and senior computer-science students. Participation in the study was voluntary and separate from grades; the thesis reports institutional ethics approval for that study.

The detailed thesis adds information absent from the conference account: **team membership was randomized while balancing technical experience, and genre-first allocation was randomized**. Teams were intended to have three members. However, **architecture order was fixed: free/ad hoc implementation first, Rulebook second**. Genre allocation does not randomize the architectural treatment order. This corrects an inference that no allocation randomness was reported anywhere in the programme, without retroactively inventing detail in the conference paper.

Turn-based RPG and real-time/tower-defense tasks used supplied starting code without the Simulation State and Services. The second stage additionally supplied a Rulebook reference implementation and training. The architecture's initial construction cost is therefore outside the task comparison.

The quantitative outcomes are **three Likert self-reports**: difficulty implementing mechanics, helpfulness of the architecture and frequency of architectural changes. They are not logged development time or independently verified maintenance cost. The instrument also asks six profile questions and three open questions about help, hindrance and other comments. Most quantitative comparisons are inconclusive; slightly fewer reported architecture changes under Rulebook remain a favorable scoped result. Lack of a conclusive contrast is not an equivalence finding or evidence of zero benefit.

Figures 6.3–6.5 show genre-specific and pooled stacked responses without exact cell counts printed. No counts were inferred from bar pixels. The qualitative plots give predicate dispatch ten helpful mentions; learning burden eight hindering mentions; and the separation of records/rules four helpful versus six hindering mentions. The same design property can help reuse while complicating implementation. Printed percentages 34.5%, 27.6% and 20.7% imply a denominator of 29 for those counts, whereas the main-course participant total is 28. The public account does not resolve this; neither a twenty-ninth participant nor pooled pilot data is invented.

The author attributes poorer second-stage grades to converging deadlines and discusses the projects' short duration. That is an interpretation, not an isolated causal adjustment. Raw answers are not publicly released because of consent restrictions; the thesis offers access by request under appropriate terms. Published instruments/results are available, and no request or recruitment was undertaken.

This feedback materially changes the third iteration: a more object-oriented Ability/Effect/Rule design and permitted Direct Access reduce the earlier rigid requirement that every interaction pass through rules. The course is useful evidence of adoption friction and design revision even though it does not estimate net maintenance savings.

## Revised mechanism and temporal boundaries

Chapters 4–5 separate a relatively stable World/Time Schedule/Field/Behavior API, intermediate Effect/Primitive/Association changes, and frequently extended entity types/abilities/rules. These are intended dependency boundaries, not measured ordinal cost laws.

Two paths are allowed. **Direct Access** invokes effect resolution against the world; **Rule-Mediated Access** passes through ability handling and rule amendment. Direct access can simplify development while bypassing amendment policy and increasing coupling to field logic. The final account explicitly moves away from S269's pure predicate-dispatch description: pages 122–123 use **Rule Fields attached to entities, an effect-type mask and an optional residual predicate**. Preserve that iteration difference.

Effects describe intended changes. Rules can amend, resolve or produce further effects; changed effects can require dispatch reconsideration. Game-specific priority and repetition guards are not general confluence or termination proofs. Effect atomicity is relative to other effects. An ability can issue successive effects or span frames, with input/physics interleaving; an earlier effect can invalidate a later one.

Modifier-only previews reuse mechanic calculations but do not reserve a future world or simulate every future obligation. A **Stable Simulation Checkpoint** permits saving/loading between update steps; it does not specify schema migration, callback retirement or irreversible host-effect rollback. Reference validity is queried against the current world, with smart/generational handles discussed as alternatives. Partial-world updates impose propagation obligations; the actual Grimoire implementation simulates only the current map.

Command, direct imperative updates, interpreters, ECS and dynamic dispatch remain valid alternatives with different integration costs. An editor or data-driven rule language still needs new primitives when new behavior exceeds its vocabulary. Adding an effect attribute can propagate to ability definitions and editor tooling. None of this is D1's explicit-current-case enumeration versus equivalent catch-all experiment.

## Proofs of concept: actual benefits, actual costs

The early single-author Lua proof of concept, developed in November 2019, demonstrates five Magic scenarios involving such interactions as indestructibility, wither and counters. This is S269's already reconstructed prototype lineage. It reports locally successful rule additions; asynchronous input during effect resolution is difficult. Keeping rules in memory was a concern, explicitly not an observed problem in that prototype.

The third Grimoire version was developed mainly by the author from January to August 2021, with occasional contributions, **over 180 reported hours and eight intermediate releases**. Two earlier versions were abandoned amid architectural and team/pandemic difficulties. This is a situated development account, with no matched alternative or per-change comparative timing dataset. The linked public devlog has not been read in this reconstruction; the hour total remains the thesis's report.

Table 6.2 describes version `0.1`, matching S270's inspected Grimoire pin **`ddcf738cffe0598799773d7e382c379f7917d989`**. Reuse its seven completely read source files and their verified identities; no additional source execution or whole-repository inspection is claimed. Passive summation of all eighteen table rows verifies the printed **5,045 LOC, 604 methods and 186 classes**. The simulation subtotal is 4,350 LOC: 1,530 core plus 2,820 extensions; similarly 519 methods and 157 classes. These are implementation-size boundaries, not observed effort shares.

The text reports 23 entity types, 43 properties, twenty effect types and 42 abilities. The Rule row has **46 classes total = one core + 45 extensions**, while adjacent prose says 46 child classes and elsewhere 64 unique rules. Those inconsistent counts are retained rather than resolved by assumption. They do not negate the concrete reuse examples:

- Combining properties/rules creates monster variations; shared Undead behavior propagates through reuse. Five AI properties can be combined into the three-property behaviors of ten monsters.
- The Ability API largely shields consumers from added effects/rules. Migration still requires rebuilding interpreter nodes and abilities; custom fields add persistence work.
- New effect attribute types require ability-editor changes. New targeting modes need substantial UI states, code and debugging. Animation and map work remain important costs outside the simulation abstractions.
- Entity-restricted dispatch motivates a SenseEffect/AreaSensor workaround. Page 147, footnote 4, reports **actual severe performance problems** when effects were routed through every entity. No numeric benchmark or general performance law is supplied.
- Movement previews use existing effect logic instead of duplicating calculations. Page 149 also reports **a recursion problem** when a long-movement preview recursively asks about short movement. This is an author-reported implementation problem, not a locally reproduced failure.

The thesis's comparison with smaller interview games is qualitative. A small reusable core does not by itself show less total maintenance or more time spent on creativity. Conversely, absent a controlled cost estimate, the reported local reuse and preview benefits remain valid situated evidence.

## Consequence for Nu and the next action

The thesis closes the selected gaps in original course instruments, professional interviews, requirement provenance and iteration lineage. Its main contribution to this survey is a more concrete comparison: **which changes stay behind a stable boundary, which require new rule vocabulary or tooling, what happens to current state and pending work, and which costs were actually observed**. It narrows a broad claim of unprecedented Nu mechanisms while leaving Nu-specific empirical value unknown.

Use S269–S271 as one evolving programme with several kinds of evidence, alongside S225, SGL, Casanova and ECS. Do not count the thesis's course or Legend of Slime as new independent cases. The 33 requirements supply questions, the interviews supply practice accounts, the course supplies mixed self-reports, and Grimoire supplies an implemented mechanism and experience report. None is interchangeable with a comparative lifecycle effect.

Next follow S268's **independent architecture-evolution/conformance route**, starting with *Evolution and Evaluation of the Model-View-Controller Architecture in Games* (10.1109/GAS.2015.10), to establish how observed changes and evaluation measures differ from Rulebook's account. Subvis, cross-engine/consistency methods, the retained evaluation-method critiques, practice continuations, S266 access and temporal/type questions remain consequential independent frontiers. All construction, recruitment, additional-worker and engine/compiler/model/benchmark/candidate execution holds remain.
