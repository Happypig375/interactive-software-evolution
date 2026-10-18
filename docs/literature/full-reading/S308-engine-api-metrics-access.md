# S308 — game-engine API metrics: methods and artifact boundary

**Complete primary reading, 2026-10-18:** all 17 journal pages, eleven figures,
four tables, formulas and 42 references are covered. The earlier access and
artifact checks below remain historical evidence. This reading closes the
corpus/method gap; it does not establish developer-outcome validation or a
measured Nu usability effect.

Venigalla and Chimalakonda, *On the comprehension of application programming
interface usability in game engines*, Software: Practice and Experience
51(8), 1728–1744, DOI [10.1002/spe.2985](https://onlinelibrary.wiley.com/doi/10.1002/spe.2985).
First online 13 May 2021; issue August 2021. Before selected reading, native
Zotero parent `GUADYRFC` v7245 was registered as `journalArticle` in
`PKLXQNEE`, citation key `Venigalla2021GameEngineAPIUsability`. The acquisition
October 15 check left that object unchanged with no PDF children. This published record
is not a preprint.

## Completed method and decision consequence, 2026-10-18

The paper selects the highest-star 100 primarily C++ repositories found by
the GitHub keyword `game engine`, manually checks descriptions and removes
five forks. All repositories were downloaded on May 10, 2020 (§§2.2, 4).
This is a purposive historical corpus, not a representative sample of current
engines or their users. No exact per-engine revision manifest is supplied.

Separate Python calculators operate on `.cpp` files, then average each
metric over files in a repository (§§2.3–2.4). That is not a verified public
API/header extraction boundary. The chosen documentation threshold is 50
words, the preferred maximum parameter count is four, and significant name
fragments occur more than twice. Six score ranges receive usability labels
after inspection of the results (§2.5, Table 3). The authors call these
Likert ratings, but they are assigned metric categories, not participant
responses. The aggregate is described as an equally weighted mean of eight
metrics (§§2.5, 3, 7).

Reported structural results favor method-name distinctness, parameter-list
consistency and parameter complexity; grouping and thread-status documentation
score poorly. Table 3 assigns 69/95 repositories to aggregate 0.5–0.7,
23 to 0.3–0.5, two to 0.1–0.3 and one to 0.7–0.9. The text's approximately
3% “better” characterization is not the exact one-of-95 table count. These
are score distributions, not observed task success or developer difficulty.
Selected stars/forks comparisons do not establish a consistent association;
the authors leave that analysis, developer-calibrated thresholds and weights
to future work (§§3–4, 7). No developer task or outcome validation is reported.

### The metric names do not guarantee the same construct

Comparison with the completed [S309 derivation](S309-structural-api-usability.md)
exposes consequential operational changes, not merely another language sample:

| Boundary | S309 | S308's published specification |
| --- | --- | --- |
| Unit and aggregation | Public declarations, per-class API and system class mean | `.cpp` files and repository file mean; public-only filtering not established |
| AESI | Depth/height of declared exception classes; no-exception methods excluded using a sentinel | Method length and line distance from throw to catch (§2.1); 46 repositories return no exception blocks (§3) |
| ADI | Documentation word threshold 10 | Threshold 50; comments inside a method and between preceding/current methods assigned to the current one, without semantic interpretation |
| AMGI | Mean over significant keyword scores; alphabetically ordered declarations in its evaluation | Table 2 divides the keyword-score sum by the number of methods; calculator describes runs of method declarations |

There are also internal specification gaps. ATSI's set definition requires
both `thread` and `safe`, while the calculator description says either
substring (§§2.1, 2.3). Table 2 prints APLCI as an unnormalized sum despite
the stated 0–1 range. The 46 no-exception reports are not accompanied by an
explicit missing-case aggregation rule, although Table 3 classifies all 95
repositories for AESI. Without the executed calculators, these are unresolved
definition/implementation correspondences; they do not identify which exact
calculation produced the results. The earlier workbook sum/mean mismatch
also remains unresolved.

R01/R07/R20 should therefore specify the interface a task actually exposes
before adopting any metric. Neither a C++ implementation-file score nor its
Java predecessor validates an F#/GDScript usability scale. Retain the useful
structural hypotheses about naming, parameters and documentation, but measure
correct completed work, learning, assistance and total cost independently.
An adoption or readiness conclusion needs relevant outcome evidence, not an
engine ranking with inherited metric names.

## Earlier decision and abstract coverage, 2026-10-15

R01/R07/R20 need to distinguish source-level API observations from correct
completed work, learning and adoption cost. The primary abstract describes
eight structural metrics applied to 95 primarily C++ public engine
repositories. Its roughly one-quarter minimum-usability statement is the
authors' metric-based characterization; it is not an observed failure rate
among developers. The abstract does not settle the corpus selection,
measurement implementation, threshold rationale or developer-outcome
validation. Those remain body-reading questions, not established absences.

Scite's outgoing graph binds S308 as the citing source and
[S309, Rama and Kak](S309-structural-api-usability.md), as the cited metric
origin. The returned contexts say S308 adapted the eight measures to C++
after their application to seven Java projects. They are selected citation
contexts, not the complete methods section. The graph's mentioning labels
do not establish validity. S309 is therefore the consequential accessible
primary-method dependency; its edition and reading coverage are recorded
separately.

## Earlier acquisition and coverage, 2026-10-15

The requested `remote-zotero-pdfs` integration followed the supplied
institutional LibKey route to Wiley's ePDF URL but returned an unknown state
without an attributable PDF. A second direct-publisher attempt failed before
binding its task tab because the helper found 123 enabled Edge address bars.
That is an integration-state failure, not a demonstrated access denial.

Direct LibKey inspection returned HTTP 200 with a 5,580-byte JavaScript shell.
The publisher's PDF target returned HTTP 403. No visible user verification
challenge was established, and no request to clear one is justified by these
results. An exact-title PDF search found publisher and request-only
ResearchGate routes, without a verified downloadable author copy.

Scite `read_fulltext`, offset 0 and requested length 8,000, returned
`source=abstract`, `contentDenied=true`, 1,547 of 1,547 characters and
`hasMore=false`. All returned abstract text was read. No journal page,
figure, table, equation or supplement is credited as read. Private route,
native-object and tool receipts remain under
`.artifacts/s308-engine-api-20261015/`.

## Bounded companion-results inspection, 2026-10-15

The author's [profile](https://akhilasrimanasa.github.io/) lists the exact
paper, and the same account owns
[API-Usability-in-Game-Engines-95-repos](https://github.com/AkhilaSriManasa/API-Usability-in-Game-Engines-95-repos/tree/797f55baed26a0844f4ae2476e0833790aa5bb2b).
The topic, 95 rows and all eight metric labels support a strong companion
attribution. The accessible publisher, institution and author pages do not
provide an explicit paper-to-repository citation; that link remains an
inference pending the body at that checkpoint. **Resolved October 18:** the
paper's footnote on p.1734 and conclusion explicitly link this repository.
The attribution is now verified; completeness of the release does not follow.

At revision `797f55baed26a0844f4ae2476e0833790aa5bb2b`, the whole tree has
three files: a README, a results workbook and a plots PDF. The README and
workbook container were inspected; the plots PDF was inventoried only.
The 26,496-byte workbook has SHA-256
`a1bf498c62ea8e003d795ec5731501a0b17cf55c3b5bd71c58286322e3786b9f`.
Its results sheet has one header and 95 unique engine-name rows, eight
metric columns and a score column. J2:J96 uses the shared formula
`SUM(B2:I2)`, whereas the README calls the aggregate an average. The GitHub
About field says 100 repositories; the name, README and workbook say 95.
The subsequently read paper explains 100 selected versus 95 retained engines
by fork exclusion, but repeatedly describes a mean rather than this workbook
sum. No recomputation or ranking reproduction is claimed.

No owner/repository URLs, exact engine revisions, extraction implementation,
tests or build instructions occur in that three-file tree. The workbook
names resemble checkout directories and do not uniquely bind source
snapshots. No metric was recomputed and no engine ranking was reproduced.

The related [GE526 conference record](https://2021.msrconf.org/details/msr-2021-data-showcase/14/GE526-A-Dataset-of-Open-Source-Game-Engines)
links a public [OSF corpus](https://osf.io/f3bs8/). Its README and two small
identity tables were inspected as provenance candidates, not its commit,
issue or release bodies. A deliberately narrow name comparison found
22 unique and three ambiguous matches against the 526-row repository table,
and five against the 101-row threshold list. It only trims whitespace,
removes terminal `-master`/`-develop` and ignores case. Renames and other
transformations remain unexamined. Neither those partial matches nor shared
authors establish that GE526 is the exact S308 corpus.

## Completed acquisition and coverage, 2026-10-18

The requested `A:/research-workflow-evaluation/integrations/remote-zotero-pdfs`
first reached an unresolved LibKey ePDF route, then bound direct publisher
task `20261018T151817-5cf2b2df`. Its visible browser check was left untouched;
subsequent observation showed the same tab cleared without agent interaction.
The integration then acquired the exact 17-page publisher PDF and attached
it as `EKKWNFZM` v7352 to unchanged parent `GUADYRFC` v7245. The parent,
membership, edition and stored/downloaded byte correspondence were independently
rechecked before selected reading. There is no pending user verification.

The PDF has 2,170,380 bytes, SHA-256
`74dffb1e1685b4e69bed4c6b85090f9dbbc264cb33d4aa29c6334833845a5492`.
All 17 text pages and all 17 MuPDF page renders were read, with Table 4
additionally viewed rotated. Native-order extraction avoided whitespace from
the publisher margin watermark; MuPDF images resolved the Poppler Symbol-font
warning. Coverage includes every displayed formula, Figures 1–11, Tables 1–4,
threats, conclusion and all references. The previously inventoried companion
plots PDF was not separately read. No calculator, source dataset, developer
study or empirical result was reproduced. Private acquisition, native identity,
text and visual evidence is under `.artifacts/s308-engine-api-20261018/`.

## Remaining consequential dependencies

Retain structural scores as hypotheses about particular interface demands
until the relevant validation, task and language boundary is established.
C++ engine-core declarations need not be the F#/GDScript interface a Nu or
Godot user actually edits. A score, a reproducible score and a validated
developer outcome are separate claims.

The selected body and its metric origin are now read. If a proposed Nu
comparison needs one of these scores, first resolve that score's actual
calculator, exact source scope, missingness and outcome validation; the
three-file companion tree and GE526 comparison do not supply them. Otherwise
proceed with the prepared task/behavior/work outcomes rather than expanding
an API-ranking exercise. No participant or experimental candidate allocation
changes, and the broader survey remains open at its declared scope.
