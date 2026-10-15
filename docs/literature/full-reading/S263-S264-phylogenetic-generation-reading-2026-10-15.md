# S263/S264 — phylogenetic generation from a game-content family

**S263.** Jorge Chueca, Daniel Blasco, Carlos Cetina and Jaime Font, *Leveraging Phylogenetics in Software Product Families: The Case of Latent Content Generation in Video Games*, SPLC 2024, 12 pages, [DOI 10.1145/3646548.3672596](https://doi.org/10.1145/3646548.3672596).

**S264.** Samuel Navarro, Jorge Chueca, Daniel Blasco, Carlos Cetina and Jaime Font, *Software product families from a phylogenetics perspective for video game content generation*, *Journal of Systems and Software* 232 (February 2026), 112649, 16 pages, [DOI 10.1016/j.jss.2025.112649](https://doi.org/10.1016/j.jss.2025.112649). The final article was available online 15 October 2025 and carries a 2025 copyright date; the issue identity printed in the PDF is 2026.

**Disposition.** Complete reading of both published editions, 15 October 2026. S263 supplies a hybrid, developer-guided method for reconstructing hypothetical ancestors from an existing game-content family. S264 explicitly extends it with feature identification and injection from deeper ancestors. This is evidence about generating game content whose simulation metrics resemble one existing family. It is not a comparison of Nu scene-family authoring, proof of generic software reuse, or a programmer-productivity study.

## Identity and coverage

Native Zotero verification preceded reading and made no changes. Both parents are in collection `PKLXQNEE`.

| ID | Native record and stored PDF | Verified coverage |
| --- | --- | --- |
| S263 | Parent `VG8B7V8U` v5701; PDF child `UHXDE9LI` v6732; 1,399,877 bytes; MD5 `1a932a52fc4bcbb406c91fdc1441d10b`; SHA-256 `bc32696775592995593b7d3ee0b9e1513e64280bb61dbc0804768776818050ee` | All 12 PDF pages read from the published ACM edition. All pages rendered and visually inspected, including Figures 1–5, Tables 1–4, equations, footnotes and threats. Text extraction was used for searching and transcription after visual inspection. |
| S264 | Parent `9E4I7XE9` v5703; PDF child `RTCZRCB8` v6695; 2,195,022 bytes; MD5 `e04b803097035f1b839c1f1c68619836`; SHA-256 `10e3a0e3c6076774dae6d2281dc6a9298790f4655ed623aa3e1804fa6acf8000` | All 16 PDF pages read from the final JSS edition. All pages rendered and visually inspected, including Figures 1–7, Tables 1–6, equations, footnotes, threats, conclusion and references. Text extraction was supplementary. |

The rendered pages and layout-preserving text used for this reading are in ignored local artifacts at `.artifacts/s263-s264-reading-20261015/`. Hashes match `.artifacts/pdf-acquisition-20261015/native-audit.json`. This closes the former main-text and visual-coverage gap recorded in `S263-S264-content-generation-access.md`; it does not reproduce the released software, simulations or statistics.

## S263 method: family analysis plus manual reconstruction

The input is the 48 non-player enemies shipped in the commercial game Kromaia. They were originally produced with opportunistic copying and modification and are expressed in the SDML domain-specific language. S263 maps each NPC model to a character string: each hull, link, weapon or other element becomes a character whose value and order matter. It computes normalized pairwise Levenshtein distances and uses neighbour joining to infer a phylogenetic tree. Existing products are leaves; inner nodes are hypothetical common ancestors or gaps in the family (S263 PDF pp. 3–4, Figure 2).

“Latent Content Generation” (LCG) has two materially different parts:

1. **Latent Content Identification (LCI)** encodes products, computes the distance matrix and tree, and enumerates common ancestors. The journal clarification says that equal minimum-distance pairs are resolved randomly and new-cluster distances are averages (S264 PDF p. 4).
2. **Latent Content Reconstruction (LCR)** is manual. A professional Kromaia developer selects eligible ancestors using design intent, semantic coherence and implementation order, and reconstructs each selected ancestor from two descendants. Kromaia-specific rules retain the larger base anatomy, average hull counts and numeric parameters, repair links, favor older visual or weapon elements, choose or average behavior, and retain cosmetics only when shared. Some alternatives are selected randomly (S263 PDF pp. 4–5; S264 PDF pp. 5–6).

The tree therefore does not itself generate a production-ready NPC. The approach combines a generic-looking string-distance/tree stage, handcrafted encoding and family rules, expert selection, and manual content integration. S263’s claim that inferred content is “ensured” to remain in family scope is stronger than the evaluation: the study measures six simulation-derived distances from the family mean, not every design, visual, semantic or player-experience requirement.

## Evaluation and retained outcomes

S263 compares three sets of ten generated NPCs (PDF pp. 5–7, Figure 3):

- **PCG+R:** a published hybrid L-system/FI-2Pop evolutionary generator seeded with 20 randomly chosen family members;
- **PCG+L:** the same generator seeded with 20 descendants selected through the phylogenetic tree;
- **LCG:** ten manually reconstructed ancestors selected through the tree.

A nondeterministic simulated player made by the Kromaia team fights each new NPC 50 times. The same simulator also evaluates the original 48-member family. The six clamped metrics cover duel completion, duration, uncertainty, killer moves, permanence and lead changes; their average is the Overall score. Results are absolute differences from the original family mean, so lower is treated as better. Designer-supplied parameters include a 20-minute timeout, 10-minute target duration and a 30% health-difference threshold for killer moves (S263 PDF pp. 6–7).

LCG’s reported Overall distance is 0.01122, compared with 0.02865 for PCG+L and 0.02989 for PCG+R (S263 PDF p. 7, Table 1). Pairwise tests favor LCG over both baselines on S2–S6 and Overall. Overall Vargha–Delaney values are 26.55% versus PCG+L and 24.12% versus PCG+R; because smaller distances are favorable, these correspond to LCG winning 73.45% and 75.88% of pairwise observations. Overall Cliff deltas are -0.468916 (medium) and -0.517696 (large), respectively (S263 PDF pp. 8–9, Tables 2–4).

The negative control is consequential: PCG+L versus PCG+R differs significantly only on uncertainty, has a negligible Overall Cliff delta (-0.04898), and PCG+L is favorable in only 52.45% of Overall pairwise observations. Selecting phylogenetically related seeds alone therefore produces little measured advantage. The favorable LCG contrast bundles manual expert reconstruction and its domain rules with tree guidance; it cannot be attributed to phylogenetic inference alone (S263 PDF p. 9).

The article reports a roughly ten-minute phylogenetic phase, about 95% spent on the distance matrix. S263 does not report the human reconstruction time. It uses one 20-year Kromaia developer for ancestor selection, corroborated by another, rather than independently assigned authors or participants (S263 PDF p. 7).

## S264’s exact increment and overlap

S264 identifies itself as an extension of S263. Its comparison table retains the same product-family input, phylogenetic foundation, Kromaia case and manual reconstruction. It adds deep ancestors and **Feature-Injected Content Generation (FICG)**; it is not a fresh replication of LCG (S264 PDF pp. 1–2, Table 1).

The conference dataset and results are carried forward directly. S264 uses the same 48 original NPCs and reports the identical Scope, LCG, PCG+L and PCG+R means and deviations in Table 2. The new arm identifies five features and injects each into two selected hosts, yielding ten FICG NPCs. Thus only the FICG row and its comparisons are incremental; the earlier thirty generated NPCs and LCG/baseline findings must not be counted as a second experiment (S264 PDF pp. 7–10, Figures 6–7 and Table 2).

FICG is also hybrid rather than automatic (S264 PDF pp. 6–7, Figures 4–5):

1. an algorithm represents each non-root common ancestor of at least three products as the intersection/common factor of descendant genomes;
2. developers choose promising deep ancestors and interpret common genes as a feature rather than exhaustively examining all candidates;
3. the tool divides taxa into those with and without the feature;
4. a developer chooses a representative donor, whose SDML fragment is decoded;
5. a developer chooses a suitable host without the feature;
6. a transplantation routine finds donor/host boundaries and candidate destinations, while developers select connections and adjust visual, functional and general parameters to satisfy family rules.

Reported implementation timing makes the human boundary visible: about ten minutes for phylogenetic inference, five minutes for guided ancestor identification, two hours for manual reconstruction, fifteen minutes for guided event analysis, under one minute for extraction after representative selection, variable unreported time for manual host selection, and usually a few minutes for injection, with automated portions taking seconds. The simulated-player evaluation is said to take about 30 seconds, but the paper does not disaggregate this enough to support a total-compute comparison (S264 PDF p. 10).

FICG’s Overall distance is 0.01034, slightly below LCG’s 0.01122 and well below PCG+L/PCG+R (S264 PDF p. 2, Table 2). Against PCG+R, FICG is favorable in 78.55% of Overall pairwise comparisons and has a large Cliff delta of -0.570984; against PCG+L it is favorable in 75.13% with delta -0.502648 (S264 PDF pp. 11–12, Tables 5–6).

The direct FICG–LCG comparison is adverse to a broad incremental-superiority claim. Its Overall p-value is .0063, yet the Overall probability is 48.90% and Cliff delta is -0.021912, negligible. Duration, uncertainty and killer-move differences are not statistically significant; permanence has a small delta (-0.188512), and the large gain is confined to lead change (-0.531624). The journal increment supports finer-grained feature reuse and comparable family-scope scores, but not a practically meaningful Overall improvement over LCG on these data (S264 PDF pp. 11–12, Tables 4–6).

## Limits and reporting cautions

- The experimental unit is a generated NPC evaluated through repeated simulated duels. Fifty nondeterministic runs per NPC increase simulation observations, but there are only ten generated NPCs per arm and one commercial game family. Runs from the same NPC should not be treated as 500 independent product-development cases.
- The six metrics are behavioral proxies relative to a family mean. They do not measure novelty, visual coherence, fun, player acceptance, maintainability, correctness of arbitrary requirements or production readiness. Completion is essentially saturated for every arm.
- Both phylogenetic approaches depend on an existing family and expert-authored encodings, rules, selections and adjustments. The automated PCG baseline has a different human-work boundary. S264 expressly notes the missing purely human-driven baseline, so it cannot isolate whether the tree improves quality or efficiency over ordinary expert creation (S264 PDF p. 13).
- The same developers supply family knowledge, configuration and guided choices. Corroboration by a second Kromaia developer does not establish inter-rater reliability, novice access or transfer to another family. The authors call for replication on other games and content types.
- No participant productivity, total authoring work, learning, debugging, integration, downstream maintenance or reuse break-even point is measured. The journal’s local step timings omit method construction, encoding/rule development, host-selection time and repair/verification costs.
- S263 inaccurately describes a p-value as the probability that the null hypothesis is false. S264 corrects this wording incompletely to “probability of validating” the null, which is also not a valid p-value interpretation. The journal RQ2 prose says 24.22% where Table 5 reports 24.12%; the latter is consistent with the stated 75.88% complement. These defects do not reverse the tabled direction but counsel using the tables rather than the prose arithmetic.
- Both editions report the LCG lead-change deviation as `0.03169 ± 0.4389`; the unusually large deviation relative to the other rows is preserved as printed and was not repaired from inference.

## Consequence for R12

S263/S264 now provide a fully read generation comparator with an explicit division between automated family analysis and expert authoring. They show that an existing family can guide the creation of new configurations or feature-bearing products that resemble its observed gameplay distribution better than one evolutionary PCG baseline. They also show that tree guidance without reconstruction contributes little in the tested setup, while the favorable result includes expert domain rules and manual integration.

That boundary does not match R12’s selected Nu unit: a quiescent editor-authored entity tree with named propagation sources, configuration, family revision and vocabulary extension. LCG/FICG synthesize new game content from a 48-member family; they do not test propagation of a source revision into linked instances, retention of instance-specific values, child identity, saved history or runtime behavior after reconstruction. Opportunistic reuse in Kromaia motivates the family, but similarity-guided generation is not itself evidence that Nu’s propagation mechanism saves authoring work.

Use these papers only if a selected R12 comparison actually includes content generation. A matched comparison would have to count creation of the encoding, family rules and tree machinery; expert selection and manual reconstruction/injection; all integrations and repairs; and the reuse count at which those costs occur. It would also need equivalent acceptance criteria beyond distance from a family mean. The papers supply no Nu advantage, human-role allocation, agent-access result or programmer-productivity estimate.

The remaining consequential gaps are a pure expert-authoring baseline, another game/domain, a product-level independence analysis, direct measures of total work and maintainability, and reproduction of the released code/data. Public repository links are printed in both papers, but their contents were not acquired or executed in this reading.
