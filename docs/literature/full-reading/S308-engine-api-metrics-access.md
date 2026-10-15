# S308 — game-engine API metrics: access and artifact boundary

**Status, 2026-10-15:** the journal body remains unread. Publisher metadata,
the complete returned abstract, selected outgoing citation contexts and a
bounded author-artifact inspection are covered. None supplies full-paper
credit or a measured Nu usability effect.

Venigalla and Chimalakonda, *On the comprehension of application programming
interface usability in game engines*, Software: Practice and Experience
51(8), 1728–1744, DOI [10.1002/spe.2985](https://onlinelibrary.wiley.com/doi/10.1002/spe.2985).
First online 13 May 2021; issue August 2021. Before selected reading, native
Zotero parent `GUADYRFC` v7245 was registered as `journalArticle` in
`PKLXQNEE`, citation key `Venigalla2021GameEngineAPIUsability`. The acquisition
check left that object unchanged with no PDF children. This published record
is not a preprint.

## Decision and actual understanding

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

## Acquisition and coverage

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

## Bounded companion-results inspection

The author's [profile](https://akhilasrimanasa.github.io/) lists the exact
paper, and the same account owns
[API-Usability-in-Game-Engines-95-repos](https://github.com/AkhilaSriManasa/API-Usability-in-Game-Engines-95-repos/tree/797f55baed26a0844f4ae2476e0833790aa5bb2b).
The topic, 95 rows and all eight metric labels support a strong companion
attribution. The accessible publisher, institution and author pages do not
provide an explicit paper-to-repository citation; that link remains an
inference pending the body. Do not present the repository as a verified
complete publication package.

At revision `797f55baed26a0844f4ae2476e0833790aa5bb2b`, the whole tree has
three files: a README, a results workbook and a plots PDF. The README and
workbook container were inspected; the plots PDF was inventoried only.
The 26,496-byte workbook has SHA-256
`a1bf498c62ea8e003d795ec5731501a0b17cf55c3b5bd71c58286322e3786b9f`.
Its results sheet has one header and 95 unique engine-name rows, eight
metric columns and a score column. J2:J96 uses the shared formula
`SUM(B2:I2)`, whereas the README calls the aggregate an average. The GitHub
About field says 100 repositories; the name, README and workbook say 95.
These are artifact inconsistencies; the unread paper may explain its own
aggregation and population.

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

## Consequence and executable next step

Retain structural scores as hypotheses about particular interface demands
until the relevant validation, task and language boundary is established.
C++ engine-core declarations need not be the F#/GDScript interface a Nu or
Godot user actually edits. A score, a reproducible score and a validated
developer outcome are separate claims.

Use S309's primary derivation to resolve what these measures actually
quantify. To close S308, acquire its exact journal body through a working
authorized publisher/author route, then inspect corpus selection, thresholds,
missingness, aggregation, implementation and validation, including any
artifact footnote. Do not infer those answers from the companion workbook
or substitute GE526's population. This access gap does not require stopping
independent consequential literature or justify running an API-ranking,
participant or candidate experiment.
