# S249 — Game postmortems: reported benefits, change costs and adoption

Michael Washburn Jr., Pavithra Sathiyanarayanan, Meiyappan Nagappan, Thomas Zimmermann and Christian Bird, *What went right and what went wrong: an analysis of 155 postmortems from game development*, ICSE Companion/SEIP 2016, pp280–289, [DOI10.1145/2889160.2889253](https://doi.org/10.1145/2889160.2889253). Main-agent reading, 2026-10-04: **all ten author-copy pages, text and visuals**, including three figures, every category/example and all22 references. The separately cited MSR-TR-2016-6 appendix remains unacquired. No original postmortem corpus, independent recoding or intervention is claimed.

The study supplies both favorable and adverse practitioner experience. It helps identify what game-development changes involve: mechanics, assets, feedback, platform limits, coordination and learning an engine. Its category frequencies measure mentions in selected retrospective accounts; they do not estimate a language, architecture or Nu effect.

## Identity and access

Native DOI/title/edition checks covered1,280 top-level/274 collection records before registering this segment. Parent **`NMHTBG3Q`5529**, note **`TFJS4948`5530** existed before selected reading. Attachment **`TFXK47H6`5536** is the [Microsoft author PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/06/washburn-icse-2016-2.pdf): **841,918bytes**, SHA-256 `6fbdf1c61751010aac94bafddc85040e432c80ba894b4a280f5cc343a5f14993`, MD5 `44a084aeb03b17167d8699b194ac2b3c`. Native stored bytes match. Crossref and the paper agree on the DOI/title/page range; final publisher-byte equivalence is not certified. Christian Bird's and Thomas Zimmermann's author PDFs download with the same hash, so they add no edition or reading.

Reference6 identifies an appendix dated February2016, MSR-TR-2016-6, at [legacy Microsoft record262289](https://research.microsoft.com/apps/pubs/?id=262289). Ordinary retrieval redirects to Microsoft's research home page, with no appendix. A constructed publication slug returns404; exact report/title searches return noise and primary mirrors. The current primary landing links only the paper, and the author's current homepage directs readers to bibliographies. These bounded routes do not establish that the appendix no longer exists. Its raw coding/context data and the paper's internal discrepancies remain unresolved. No author contact or access purchase occurs.

## Sampling, coding and units

Sections2–4, pp2–3, describe **215 listed reports,60 excluded,155 included**. Exclusions cover conference recollections, single-tool/technology accounts and narrow process accounts; included reports describe whole-game development with positive and negative sections. This selection is consequential: engine-specific adoption problems may be excluded by design. Section2 gives1998–2015, while §3 describes listings before January2014; the exact cutoff remains discrepant.

Two named analysts begin with12 categories adapted from an earlier24-report study, iteratively discuss additions and revisit earlier coding. The described first three weeks total **2×(3+10+15)=56**, whereas the text says60 reports were analyzed when categories stabilized. Subsequent work proceeds at about40 reports/week combined, with weekly agreement discussions. The paper does not establish independent duplicate coding of all155 reports or report an interrater coefficient.

The final22 categories comprise product7, development6, resources4, customer-facing4 and other1. A category is present or absent within each report's positive/negative account; several categories can occur, and one can appear on both sides. Frequencies therefore are neither mutually exclusive problem shares nor independently measured success rates. Not mentioning a topic does not establish that it was absent.

Context is incomplete: platform87%, development duration73%, team size81%, publisher90% reported. Among known cases,62.14% target multiple platforms,74% have at most20 developers and74.4% use an external publisher. These are availability-conditioned descriptions. “Product evolution” concerns changes to the **game concept**, not all engine/API/code maintenance.

## Results and concrete change families

Sections5–8, pp3–9, preserve positive and adverse examples. They are developer reports selected and interpreted by the researchers, not independently observed timings or controlled comparisons.

| Source/example | What the account supports | Boundary relevant to Nu |
| --- | --- | --- |
| Tower Bloxx, p4 | A senior programmer/designer pair reports a feedback cycle below three hours while finding the intended mechanics. | A useful iteration outcome for a particular process bundle; no language/live-state control or total-cost estimate. |
| RoboBlitz, pp4–5 | Building levels before settling mechanics makes later movement/feature changes burdensome. | A small source edit can propagate into levels, assets and balancing. |
| Dead Head Fred / ViciousEngine, p5 | Existing engine facilities reportedly suffice for the game's features without game-specific engine changes. | Favorable reuse experience; [S250](S250-game-industry-problems.md)'s coded account of the same game also records art, dialogue and balancing work after design changes. These can coexist. |
| Stubbs the Zombie / licensed Halo engine, p5 | Sparse documentation and a steep learning curve slow adoption. | Available engine functionality does not imply low integration/learning cost. |
| Galactic Civilizations, pp4/8 | Omitting multiplayer frees effort and avoids synchronization/latency obligations. | This changes requirements. It is not a same-behavior optimization or permission to remove required behavior in a comparison. |
| Splinter Cell, pp4/6–7 | Extensive preparation, technical design documents and extra resources accompany a reported four-month Xbox-to-PS2 port. | Preserve the positive result and its preparation/resource bundle; no equal-resource comparator. |
| Operation Flashpoint and Big Mutha Truckers, p5 | Missing intent/implementation documentation causes recovery work; excessive documentation in the wrong form also fails to help. Other accounts favor verbal iteration. | Documentation fit and maintenance matter; neither maximal nor minimal documentation is universally supported. |
| Zoo Tycoon: Marine Mania, p6 | Overlooked animations and underwater movement complicate scheduling. | Behavioral change crosses code and asset boundaries. |
| BioShock, pp4/6 | External feedback reveals a poor concept and prompts redesign. | Satisfying the current implementation specification and discovering a valuable player experience are different outcomes. |

The prose's leading positive mentions are design50%, process43%, team40%, art39%; leading negative mentions are obstacles37%, schedule25%, process24%, design22%. Figures2–3, pp7–8, visually appear somewhat higher for several corresponding bars. No exact bar digitization or silently repaired denominator is claimed; the missing appendix prevents reconciliation. The finding that both process and design can be helpful or troublesome survives that numerical uncertainty.

Section7, p9, compares small/large teams, publishing arrangements and platforms descriptively. For example, self-published versus publisher-supported games report tools positively17% versus40%, while negative mentions are17% in both. These are selected-report frequencies, with no formal tests or controls for resources, genre, time and team composition. They do not identify the effect of a publisher. A team-size paragraph also changes its label from design to team mid-comparison; retain that wording ambiguity rather than reinterpret its25% value.

## Synthesis consequence

For B01/B06/B07/B10/B12, this is positive practice motivation for faster feedback, reuse and well-matched documentation, together with concrete adoption and change-propagation costs. It supports separating **edit-to-feedback time, completed integrated change, preserved behavior, asset work and player-value discovery**. It does not tell us which Nu mechanism improves those endpoints, their population prevalence, or the effect size to use for a proposed experiment.

[S250](S250-game-industry-problems.md) and [S251](S251-game-problem-dataset.md) extend the postmortem-method comparison but reuse a different linked corpus. Their later labels must not overwrite this primary's22 categories or its obstacles37% finding. The next consequential independent route is professional game-development practice and engine adoption; the absent appendix is an access/data gap, distinct from unmeasured Nu benefit. All construction/model/worker holds persist.
