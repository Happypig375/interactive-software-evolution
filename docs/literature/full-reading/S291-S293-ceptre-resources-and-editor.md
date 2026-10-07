# S291–S293 — Ceptre: resource transitions, stages and editor usability

**S291:** Chris Martens, *Ceptre: A Language for Modeling Generative Interactive Systems*, AIIDE 11(1), 2015, 51–57. [DOI 10.1609/aiide.v11i1.12784](https://doi.org/10.1609/aiide.v11i1.12784).

**S292:** Chris Martens, Alexander Card, Henry Crain and Asha Khatri, *Modeling Game Mechanics With Ceptre*, IEEE Transactions on Games 16(2), 431–444, June 2024; published online July 2023. [DOI 10.1109/TG.2023.3292982](https://doi.org/10.1109/TG.2023.3292982).

**S293:** Alexander Card and Chris Martens, *The Ceptre Editor: A Structure Editor for Rule-Based System Simulation*, VL/HCC 2019, 133–137. [DOI 10.1109/VLHCC.2019.8818687](https://doi.org/10.1109/VLHCC.2019.8818687).

**Disposition:** all three selected main-paper editions are completely read, including every original page visually. S292 extends the language account and summarizes S293's eight-person study; it is not an independent usability replication. The original editor-image supplement, underlying study records, publisher byte equivalence and an executed implementation remain outside the completed coverage.

## What the alternative actually supplies

Ceptre represents a state as a multiset of ground predicates. A rule matches and consumes a subset, produces another subset and retains the unmatched remainder. Multiplicity matters: two otherwise identical resources can support different transitions. Types constrain terms and predicate arguments; they do not by themselves enforce domain rules such as a character having exactly one location. Initial-state construction and every applicable rule must preserve such an invariant.

The S291 examples use generic typed variables, resource consumption/production, unchanged premises and persistent facts. These are logical resource distinctions, not an assertion that the implementation stores immutable snapshots of the complete game world. The paper develops a Shakespeare storyworld and a skeletal dungeon crawler, with additional examples mentioned. Making an automatic combat stage interactive helps the author inspect behavior; scripted strategies permit exploration. These are useful demonstrations and author experience, without a controlled effort or runtime comparison. [S291 author edition, pp.1–7](https://www.cs.cmu.edu/~cmartens/ceptre.pdf).

Rules within a stage are unordered. If several transitions are enabled, a selected transition runs; automatic execution can choose randomly, while an interactive stage exposes choices to an external player. A token premise can restrict a turn to one action. Without that restriction, interactivity alone does not impose a one-action turn.

Stages group rules and run until quiescence, when none of the active stage's rules can fire. Explicit interstage rules then hand off control and can change state. Resource production and consumption define a causal trace: independent actions can have different orders, while competing actions share needed resources. A trace records represented logical dependencies; it does not automatically capture native handles, clocks, host I/O or an independently running engine's state. Neither paper supplies a general source-edit migration, pending-work transfer or external-effect rollback contract.

S292 adds an explicit operational account, formal properties, richer tutorial examples, a web editor and application discussion. Its simplified Minecraft rules omit the spatial crafting-grid requirement. Its Pandemic model deliberately uses fewer cities, one disease and shared player abilities. These examples show expressiveness under the stated model; they are not complete implementations of the named games. [S292 author manuscript, §§II–IV](https://www.convivial.tools/PapersPublic/ceptre-tog.pdf).

## The compositionality boundary matters

S292 §V.A gives a frame-like property: if a multiset can reach a result, adding extra resources permits the old trace while retaining those extras. This is an **existence** statement. Extra resources can enable additional transitions and interactions; the property does not promise identical behavior under every schedule or preserve a probability distribution.

The paper then states in §VI.3 that staged programs as a whole give up this compositionality. A rule's local meaning within one stage and the behavior of an entire staged system are different claims. Quiescence and stage switching depend on which rules and resources are present. Added behavior can therefore change when a phase ends even if each individual rewrite has a simple local meaning.

The finite-term fragment supports stronger reachability reasoning than the full language. Richer terms and relations trade that restricted decidability for expressiveness; analysis procedures for supported fragments remain future work in the journal account. A rule-language formalism is not evidence that all required game outcomes or temporal obligations were checked. This reading reconstructs the paper's argument; it does not independently mechanize the proof or run the interpreter.

**Nu consequence:** Ceptre is a concrete resource/phase alternative to the coordination mechanisms already reconstructed in Casanova, SGL, Join Token and Micro-Machinations. Compare the represented state, permitted transitions, scheduling choice and host boundary. Neither Ceptre's local composition property nor a coherent Nu world update establishes arbitrary whole-program preservation. This is mechanism overlap, not a historical-priority claim about Nu's origin.

## What the editor study supports

S293's editor uses a modified subset of Ceptre. Menus constrain predicate selection, argument number and term types. Naming introduces reusable program elements; subsequent menus refer to them. An explicit lock action checks a component before making it available for use elsewhere. An unfinished or invalid component remains unlocked. This is structured editing and immediate feedback, not proof that the chosen rules express the intended model.

Execution starts from the declared initial state and current rules. The user can select a transition, request a bounded number of random steps, or run toward quiescence if it is reached. This is not a stated policy for preserving a previous execution after arbitrary edits. S292 §IV.F explicitly says the web editor lacks stages, unlike the full textual implementation. Consequently, the editor study cannot establish that users learned staged coordination.

The original study recruits eight participants from a university campus. All have programming experience: mean 3.75 years, median 3.5, modes 2 and 4. A Blocks World tutorial has a 30-minute limit, followed by a 30-minute think-aloud extension session and an interview/demographic survey. The extensions appear in a stated order: add another robot arm; add a block to both its type/set and initial state; then add a rule that removes an alphabetically ordered stack so the model can quiesce. These are consecutive tasks after guided training, without a randomized treatment or comparator. [S293 accepted manuscript, §§V–VI, pp.3–4](https://par.nsf.gov/servlets/purl/10133864).

The favorable observations are specific:

- All eight solve the second-arm task correctly. Four finish by duplicating arm predicates/rules; four finish by parameterizing the arm through a new set and predicate argument. Both organizations are accepted. Six initially try duplication, so two later change approach.
- Seven complete the extension session within its time limit; one reaches the cutoff at the final prompt. The final quiescence rule is completed by six without significant assistance. Completion and unassisted completion are different endpoints.
- All eight choose to test the quiescence rule without being asked. Their explanations during construction/execution give the authors evidence of model understanding. Positive feedback and these concrete behaviors remain useful evidence of learnability in this setting.

The original paper mentions a language difficulty for one participant and hypothesizes negative transfer from AI planning for another difficulty. These are retained observations/interpretations, not grounds to remove participants or established causal effects. The paper does not provide participant-level timing/program records, a scoring rubric, a coded transcript table or an independent comparative maintenance outcome. Its proposed study with biological-domain experts is future work, not another completed evaluation.

## Preserve the differences between the two study accounts

S292 §V.B explicitly identifies S293 as the detailed previous report. Both describe eight participants and the same three Blocks World extensions. Count one study lineage, while preserving these unresolved differences:

| Detail | S293 original accepted manuscript | S292 later author manuscript | Disposition |
| --- | --- | --- | --- |
| Logic background | All seven who finish report a prior logic course; the noncompleter does not. | Most participants are described as lacking formal logic training. | Coursework and “formal training” are not operationally reconciled. Do not claim success predominantly without logic exposure or infer a causal benefit of coursework. |
| Tutorial timing | A tutorial limited to 30 minutes. | A 15-minute guided tutorial; all finish within 15 minutes. | A 30-minute cap and faster completion could coexist, but the records needed to bind these descriptions are absent. Do not silently substitute a common protocol. |
| Extension outcome | Seven finish the extension session; all eight solve the arm task; six complete the final rule without significant help. | Seven of eight complete each extension within 30 minutes. | Use the original task/assistance distinctions; the later summary is not a per-task timing table or independent replication. |

These differences narrow claims about prerequisites and timing, without erasing successful model changes or self-initiated testing. Learning a supported editor after training, proving a local semantic property and reducing net maintenance cost are separate outcomes.

## Exact editions, coverage and library state

| ID | Acquired primary edition | Complete main-paper coverage | Native parent / note / PDF |
| --- | --- | --- | --- |
| S291 | Seven-page CMU author PDF, 280,442 bytes; created 2015-11-07 | All seven text and visual pages, displayed rules, two unnumbered diagrams and 28 references; no appendix | `MHLFBNUB` / `APFEA5U7` / `7W36XMSS` |
| S292 | Fourteen-page author manuscript, 941,965 bytes; created 2023-07-04 | All fourteen text and visual pages, thirteen figures, two tables, six definitions, formal argument, footnotes and 73 references; no appendix | `YYK2JXJF` / `HWCKN24C` / `7BX8SLUI` |
| S293 | Five-page NSF accepted manuscript, 79,817 bytes; created 2019-07-30, modified 2020-02-09 | All five text and visual pages and 24 references; no main-paper figures, tables or appendix; the separately mentioned editor-image supplement is unread | `R3H6KMVF` / `ZWDF5A7G` / `P32BAMNQ` |

SHA256 identities:

- S291: `97028a04452ae87d8cd370eb7bded5c70329fd261b9a57613006d54c0da074ad`.
- S292: `ae66210fd0989461b49814913086921c1018b6d5ec9305601baf9f5b3caf58b4`.
- S293: `90579cbdbe33505f7de4fd22327a3d296df49533bf2f73c90c8d88d553129e93`.

Each record was created in native Zotero collection `PKLXQNEE` before its selected reading, after DOI/title/edition matching. Uploaded PDF bytes and hashes match the acquired files. Final note/version checks are recorded in the search ledger. Scite's metadata flags did not supply or deny an attempted body request; no Scite full-text request was made for these three papers. S291's ordinary publisher PDF request failed with a disconnected connection; its CMU route succeeded. S292's later publisher accepted-manuscript check returned HTTP 418 HTML, not a PDF. S293's publisher page showed a verification challenge; the ordinary NSF record and PDF succeeded. The original NCSU source route timed out. No challenge bypass, editor execution or contact with authors occurred.

Crossref, NSF and first-page metadata bind the selected identities. S292's four authors are verified despite Scite displaying only three; its online year and 2024 issue are one publication lineage. The selected author copies have not been byte-matched to the publishers' final PDFs. S293's original image supplement remains unavailable from the inspected routes; S292's later editor figures do not authenticate that earlier supplement. Private PDF/extraction/access receipts remain ignored by Git.

## Source-decision audit

The segment records 251 retrieval/reference occurrences and 148 normalized source units: three credited main-paper editions, 121 deferred dependencies and 24 sources outside the selected question. The 28, 73 and 24 printed references are screened at bibliography/context scope, not credited as full readings. Crossref's journal reference keys do not follow the author manuscript's printed ordering; identities are matched by title rather than key number. Fifty-three DOI metadata checks yield 48 titles directly and five HTTP errors; SC234 verifies those five identities. Printed title/year/edition differences remain in the local roster.

Comparison with 178 earlier decision files finds nine historical identities. Two have material full-reading updates and seven unchanged decisions are withheld. Scite answer `nu_background_s291_s293_20261008` records 141 decisions: three credited, 114 deferred and 24 not used. There are 138 title/abstract/reference-context stages and three full-text stages. The receipt and `citation_report` each preserve exact membership, decisions and all 846 source/provenance/reason/stage fields. Both report zero skips or missing-reason/linkage warnings; the report is not truncated and answer-scoped retrieval is null. These are audit units, not independent studies or field-completeness measures.

## Consequential continuation

The selected resource/stage method is now reconstructed. Apply the contract and editor outcome to B03/B05/B08/B12 and reassess the retained discovery/primary gaps against the actual Nu claims. Do not promote every cited language, formal foundation or adjacent authoring study automatically. S293's original supplement and study records would refine editor/version/prerequisite claims; without them, use the bounded statements above. Further literature alone cannot supply an unmeasured Nu effect, and no experimental or worker hold is lifted.
