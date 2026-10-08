# S289–S290 — Game-development practice: reported process, adaptation and value

**S289:** Timothy McKenzie, Miguel Morales Trujillo and Simon Hoermann, *Software Engineering Practices and Methods in the Game Development Industry*, CHI PLAY EA 2019, pp. 181–193. [DOI 10.1145/3341215.3354647](https://doi.org/10.1145/3341215.3354647).

**S290:** Tim McKenzie, Miguel Morales-Trujillo, Stephan Lukosch and Simon Hoermann, *Is Agile Not Agile Enough? A Study on How Agile is Applied and Misapplied in the Video Game Development Industry*, ICSSP/ICGSE 2021, pp. 94–105. [DOI 10.1109/ICSSP-ICGSE52873.2021.00019](https://doi.org/10.1109/ICSSP-ICGSE52873.2021.00019).

**Completed 2026-10-08:** all 13 S289 and 12 S290 publication pages are read textually and visually, including all figures, tables, sidebars, acknowledgments and 38/50 references. The newly supplied PDFs resolve the previous original-visual/file gaps. The former partial-reading filename is retained for stable links; its earlier account remains in Git history. These are two linked publications whose participant overlap is unreported, not evidence of 20 independent studios. Neither study, its data nor its analysis is reproduced here.

## S289: survey design and measured construct

From an 84-studio creative-media frame, the researchers contact 30 eligible New Zealand studios, receive 15 replies and retain 12 meeting the minimum of five full-time staff (pp. 183–185). The online survey runs from 14 April to 31 May 2019 and asks about a representative project. Context questions precede eight practice subsections and perceived framework alignment. Senior engineers, a Scrum Master and a psychometrics/survey expert review the survey; a senior developer and industry expert pilot it.

Practice answers receive mostly unit weights, divided among multiple correct options. The resulting adherence score is compared with respondents' own perceived alignment. **Both measures are self-reported:** the study does not independently observe workflows or establish an outcome effect of adherence. The complete question/options packet, scoring map, missing-answer rule and raw export are not supplied by the PDF.

Ten studios answer the methodology question and all ten name Scrum. The text also reports 50% Kanban and 33% FDD, subsequently discussing five and three users respectively. The FDD denominator remains unclear. The discussion explicitly lacks the reasons for the adaptations and recognizes the small response count and uncertain population transfer (pp. 189–190).

## S289: supplied PDF completion and all six figures

Figure 1 (p. 185) plots ten labeled studios: S1, S2, S3, S5, S6, S7, S9, S10, S11 and S12. All perception points exceed the questionnaire-derived Scrum score; S6 is the only one within the stated ±7.5-percentage-point choice interval. The plot does not print exact underlying scores. Do not manufacture precise values from point positions.

Figures 2–4 (pp. 186–188) expose Scrum, Kanban and FDD practice response matrices. Figure 2's caption makes a blank ambiguous: either no answer or a Scrum-related option not selected. Its sprint-review row contains nine Yes responses, while seven studios supply review-topic details; the prose says seven conduct reviews. No explicit reduction rule reconciles these counts. All twelve entries for cross-functional Scrum teams are No, but the text recognizes potential ambiguity in respondents' understanding of that term. Figure 3 includes S12 answering Sometimes for WIP limits without identifying which five rows belong to self-declared Kanban users. That cell cannot alone settle the subgroup claim of no WIP-limit use. Figure 4 shows mixed roles, artifacts, modeling, prototypes and feature lists; a framework label does not identify the whole process.

Figure 5 (p. 188) reports estimated effort in six bins, from zero through 81–100%, for ten development practices. These are neither logged hours nor mutually exclusive parts of a fixed time budget. The test-driven-development row sums to eleven responses; the other nine rows sum to twelve. Five studios place continuous integration in the highest bin, while six report zero colocation effort. Such distributions describe reported practice, not assigned treatments or measured productivity.

Figure 6 (p. 189) reports use of metrics or practices: acceptance criteria 25%, story points 17%, end-user prototyping 50%, velocity 25%, completed-feature counts 50%, iteration pass/fail 8%, blocker counts 8%, on-time-shipping measurement 67%, iteration burndown 50%, and epic/release burndown 42%. **The 67% figure counts studios reporting a metric, not projects delivered on time.**

This is useful evidence that a claimed framework can differ from the activities reported under it. The article does not establish that stricter conformity improves game quality or net development work. Its possible explanations involving leadership and team dynamics remain hypotheses; adapted practice need not be ineffective practice.

## S290: interview and analysis procedure

The later study interviews one senior leader from each of eight New Zealand studios with at least five full-time staff (§IV, pp. 96–97). Recruitment uses email, industry events and community Slack/Discord channels; no invitation denominator establishes a response probability. Six context questions and three adaptation questions are printed, followed by lists of core Scrum, Kanban and FDD practices for the frameworks participants say they use. S289 informs that choice. The full framework checklist is not reproduced as an instrument packet.

Senior engineers outside game development and a Scrum coach iteratively review the script; ethics approval is reported. In-person or video sessions typically last 40–60 minutes, with two recording tools and immediately reviewed written notes. Relevant passages are selectively transcribed with voice typing, speech tics removed and bracketed clarity edits. Participants receive a week to correct their account. This does not establish that everyone replied or that complete verbatim transcripts were analyzed.

General Inductive Approach analysis proceeds from categories through themes to a model, using NVivo 12 and Excel. Another researcher performs parallel independent coding, with similarities and differences discussed to consensus; two stakeholder-check rounds involve several participants. These are checks within one study, not independent replications. No inter-rater statistic, complete codebook or transcript corpus is acquired. The limitations also state that the primary researcher collected and analyzed the data alone without blinding, followed by the reported team/stakeholder checks (§VI).

The interview was not piloted, and actual studio workflows were not observed. Marketing, HR and sales are outside the development-process focus; contextual factors can explain reported difficulties. The precise collection window and overlap with S289's sample are unreported. Eight studios are described as about 27% of the country's studios and employing about half its game-development workforce at that time, but the minimum-size criterion omits the numerous smallest studios. Those fractions do not establish a representative probability sample. The PDF supplies no quantitative comparison of delivered quality, development cost or change time.

## S290: useful adaptations and continuing costs

The five themes (§V, pp. 97–102) explain why studios choose agile, how they adapt it, how roles change, how development phases differ, and how experience shapes adoption. Participants value flexibility, experimentation, familiarity and ownership. Feature creep, pivots, weak shared vision, unclear responsibility and management bypasses can undermine those benefits. Only two studios are described as using the full Scrum events, artifacts and practices. Informal play-build reviews, specialist meetings, varying retrospectives and hybrid producer/team-lead roles often replace textbook arrangements. Small studios report difficulty funding a dedicated Scrum Master; omitted WIP metrics or cadences can reflect perceived utility as well as limited training.

**Figure 1 (p. 99)** synthesizes two overlapping production tracks: Scrum-like development and Kanban-like art/asset work. Concept work seeks a playable idea with rapid prototypes; preproduction combines prototyping, tools and assets; production combines feature creation/testing with asset creation/quality control; postproduction combines additional content with bug fixing. The milestone boxes are explicitly examples, not a measured schedule or mandatory linear process. The prose allows phases to overlap or recur. Kanban also supports incoming fixes, and participants describe Scrumban combining continuous urgent work with iterative content delivery. This is favorable experience about fit to different work, not evidence that one hybrid is universally optimal.

**Table I (p. 101)** preserves important countercases rather than reducing the study to conformity versus problems:

| Studio | Reported framework | Retrospective / action on issues / Scrum Master | Reported issues or resolution |
| --- | --- | --- | --- |
| 1 | Agile → ScrumBut | No / No / Producer | Communication; knowledge siloing |
| 2 | Agile | No / No / Developer lead | Communication; accountability; shared game vision; agile experience |
| 3 | Agile/Kanban | No / No / Product owner/developer lead | Crunch in the past |
| 4 | Agile | Yes / No / Producer | Communication; accountability; process commitment |
| 5 | Scrumban | Yes / No / None | Communication problems reported solved by colocation and chat systems |
| 6 | Scrum | Yes / Yes / Yes | Process commitment; shared understanding; knowledge siloing |
| 7 | ScrumBut | Yes / Yes / Producer | Team diversity; shared game vision |
| 8 | Scrum → Scrumban | Yes / Yes / Yes | Shared understanding; knowledge siloing; process commitment |

Arrows in the framework column mark changes over time, not assigned treatments or additional observations. Studio headcounts and Scrum-team sizes also differ: studios 7 and 8 split 45 and 28 people into teams of 3–10 and 5–9 respectively. Do not label all 45 people one Scrum team.

The discussion describes Scrum-aligned studios as having no communication issues, but rows 6 and 8 still list knowledge silos and shared-understanding problems. Absence of one coded label does not establish absence of related difficulties. Studio 3 lacks retrospectives without a Communication label; studio 5 reports a resolution without a dedicated Scrum Master or formal action-on-issues entry. Preserve these cases alongside positive accounts of training, retrospectives and role clarity. Retrospective leadership interviews support plausible explanations; they do not identify training as the causal root of all difficulties or establish inevitable conflicts.

## Publication lineage and implications for Nu

S290 cites S289 as its predecessor and sometimes retells its perception result more broadly as overestimation of Scrum and Kanban. The original S289 figure establishes the ten-studio Scrum comparison; Kanban estimates vary. Keep that original scope. S289 cites the 2017 Scrum Guide and its team-size convention, whereas S290 cites the 2020 guide. A changed reference edition is not evidence that the observed studios changed their team sizes. Likewise, the two publications do not establish 20 distinct studio cases.

**Inference for B01/B08/B10/B11/B12:** evaluate what a representation and workflow enable for particular users, changes and production phases. Reported adherence is not delivered quality, a declared programming model is not the information developers can use, and a formal role is not an observed coordination outcome. These papers complement [S288](S288-collaborative-arvr-practice.md) by making adaptations and division of work concrete. Preserve favorable experience with continuous asset/fix work, iterative features and communication tools, while charging learning, integration and coordination to the relevant cost boundary. None estimates Nu's comparative benefit.

## Native attachments and exact coverage

Both existing records and membership in collection `PKLXQNEE` were checked before the supplied-PDF readings. Every page was inspected textually and visually; S289's dense figures on PDF pages 5–9 received additional enlarged inspection. The readings include all introductions, methods, results, discussions, limitations, acknowledgments and reference sections. There are no appended raw instruments or datasets.

| Work | Verified objects before reading | Original PDF identity | Coverage |
| --- | --- | --- | --- |
| S289 | Parent `YVX3P3PL`5951; note `UJSZWP6M`5956; PDF `SVBGAZ6C`6094 | 935,454 bytes; SHA256 `182427308fec198ef0857f2cc96adbba49c67dbdc1ee52dfceffb13a3db87314`; MD5 `a116bcaa363137a04ac65d2a294278ee` | 13 pages, printed 181–193; six figures, sidebars and 38 references; 38,669 extracted characters |
| S290 | Parent `X82JZW8N`5953; note `KJ8JQXVX`5957; PDF `47PMHUDQ`6093 | 476,073 bytes; SHA256 `2e8127142f6f857317d19b347f7cd34d13ac1c2c772a27f9c2b241ba8c45e0a7`; MD5 `ccfcb0b356c17c319943c21814e4e43f` | 12 pages, printed 94–105; Figure 1, Table I and 50 references; 71,056 extracted characters |

S289's actual first page confirms three authors. The author-project entry's extra Lukosch name is not adopted. Its platform count of 39 references differs from the 38 printed entries; Crossref deposits 36, omitting printed entries 5 and 22, with five doubled-hyphen DOI strings retained separately from printed identities in the earlier audit. S290's publisher layout confirms four authors and the 2021 conference DOI; Scite's three-author display is incomplete. The former repository accepted-manuscript bytes remain unavailable, so **no byte equivalence between accepted and publisher editions is claimed**. The publisher PDF now governs this reconstruction.

The earlier indexed readings assembled all returned body text but lacked original PDF visuals. Their extraction hashes, denied access attempts and partial citation stages remain in the historical note/ledger; no repeated failed download is counted now. S289's PDF has 92 hyperlink annotations, mainly reference/metadata links; these were inventoried, not all visited or credited as read sources. S290 has no PDF hyperlinks. No separate raw-response, transcript, complete-instrument or supplementary-analysis packet is acquired. Private PDFs, text extractions and renders remain outside Git.

## Audit and remaining work

The earlier answer-scoped audit `nu_background_s289_s290_20261008` covered both printed bibliographies and retrieval routes at their actual partial scope: 194 occurrences, 139 normalized units, 121 submitted decisions after historical deduplication. It is not rerun as fresh screening. The supplied attachments are material full-text updates to these two source decisions; their final note versions and the combined attachment-completion audit are recorded in the [search ledger](../nu-background-searches-2026-09-30.md).

The original visual/file gaps are resolved. Complete instruments, scoring/raw records, observed workflows and participant overlap remain distinct evidence limits. Follow the exact Finnish or Musil process methods only if they can change a selected comparator or cost claim; there is no automatic practice-paper queue. The [coverage map](../nu-background-survey-2026-09-30.md#coverage-map) integrates these findings. All construction, worker and experimental holds remain.
