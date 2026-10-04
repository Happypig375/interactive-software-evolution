# Game-postmortem dataset lineage and bounded data check

Main-agent passive inspection,2026-10-04, supporting [S250](S250-game-industry-problems.md) and [S251](S251-game-problem-dataset.md). This checks released identity, rows and printed aggregates with our own CSV/XML parsing and arithmetic. No author code, workbook formulas/macros, model, compiler or benchmark is executed. No independent recoding, causal replication, full original-report reading or full workbook visual audit is claimed.

## Acquired sources and coverage

[The paper-linked repository](https://github.com/game-dev-database/postmortem-problems) has16 returned commits. Its complete recursive tree is not truncated. The latest pin is **`5be5c16e7d04a9fbea8d8fb7273d5afd89452715`**,19July2020; the preceding18July commit describes refactoring problems/catalogue. Current acquisition is seven root README/CSV files. The tree's postmortem PDFs are inventoried but not downloaded or read. Two historical dataset CSVs and the README-linked public Google workbook were additionally acquired.

| Source | Bytes / SHA-256 | Actual inspection |
| --- | --- | --- |
| Initial dataset at `ee29e7ed0d6a725adcdd607caff2172af1071a66`,18December2019 | 1,194,234 / `c0be3091dab371e805136f959056c4d6bec373f28f261084e4fc14732b221978` | Headers, row/type/group/year counts; no full quotation reading. |
| Dataset at `a2efd1719e5ba1917918c955facfb82dd6f91343`,28January2020 | 1,196,556 / `f5e9843ef366b3b95d800f5a98ad1a06928968784214a0c949b27bb2ecbbbc61` | All row metadata counted; all20 Figure4 type counts, three Figure3 group counts and medians compared with S251. |
| Dataset at latest pin | 1,142,342 / `28bd487d40537d8674670718d4fc908c34de60a3756bc6c8313822323bf3f682` | All row metadata counted; all20 S250 type counts, four group counts and six platform intersections compared. Five complete quoted entries read:106,381,393,543,898. |
| [Public workbook export](https://docs.google.com/spreadsheets/d/1my2J234AI3kt_H0GRQBxl-w1-h0mh5DqVbsmaVNwW9o/edit),4October2026 | 1,418,172 / `b3e4213955b22e9bfebda710d99d50cd72e18c862b1421589547d0a8574fc740` | All45 worksheet names, nonempty-row counts and opening metadata inspected; all105 rows of `all` summary read; bounded headers/examples in design/team/technical/tools sheets. Cached values and stored formulas only, no recalculation or complete quotation/visual inspection. This is a dated live export, not a publication-pinned workbook. |

Native supplement **`EQ2GLCU6`5542**, under S251 parent **`WW4E5L3C`**, stores these sources with the other root CSVs, README, commit metadata and an identity manifest: **2,281,271bytes**, SHA-256 `4ccef2f7cb9f8559db812ca943903b1fa912d74940d28b9c96c845019be2dc79`. Native stored bytes were read back and hashed; existing parent/note/PDF versions and memberships were preserved. Bodies, spreadsheets and extracted passages remain outside public Git.

The web reader could not open the Google sheet; its ordinary public XLSX export succeeded. An unavailable optional `openpyxl` import initially prevented parsing, not acquisition. Standard-library ZIP/XML parsing then read the saved file without installation or execution of workbook content. This is not an access-blocked dataset.

## What reconciles

The January snapshot has1,035 rows. All20 type counts and group totals468 management/466 production/101 business exactly match S251; median entries per title5 and per year48 also match. The first December snapshot already has1,035 rows, but some assignments differ: management470/production464, for example. A matching total alone would not identify the publication's category version.

The latest snapshot has927 rows. All20 Figure3(b) counts match S250 after explicitly aligning its `game-design` label to CSV `design`. Groups are425 production,197 people management,218 feature management and87 business. Platform intersections are351 PC only,123 console only,97 mobile only,231 PC+console,47 PC+mobile and78 all three, exactly matching Figure4. These are problem entries attached to games with those platforms, not927 independent games or platform-specific defect measurements.

Each selected snapshot has200 title/name identities and199 literal source URLs. Trimming two trailing title spaces makes **all200 titles common to the January and latest snapshots**. The papers therefore describe an evolving200-title corpus, not two independent200-game replications. The exact semantic disposition of all changed/deleted quotations is not reconstructed.

## What remains discrepant

| Boundary | Finding and disposition |
| --- | --- |
| Date coverage | Both historical and latest CSVs include1997 and2019, while S251 says1998–2018. S250 uses1997–2019. A larger nominal date range does not prove newly added games. |
| S251 platform counts | January data give PC783/console479/mobile254 versus787/475/254 in prose; all-three90 agrees. Preserve the four-entry discrepancy. |
| S250 type percentages | Technical116/927=12.51%, design112/927=12.08%, team84/927=9.06%; the figure gives11/11/8%. Top three sum33.66%, not prose30%. The printed labels are compatible with rounding against the old1,035 denominator. This is an inferred stale-denominator possibility, not observed plotting-code behavior. |
| Trend denominator | S250 §3.2 uses problem counts per year; §8.1 says postmortem counts per year. Own latest-data check gives2018 marketing3/16=18.75%, consistent with the plotted point; it does not reproduce fitted curves or resolve every statement. |
| Root-cause packet | Workbook `all` has105 summary rows with cached N total951; its separate coding sheets retain multiple labels, unresolved cells and older1,035-row working data. The journal's environmental-team48 row is absent from that summary. Journal Table8 duplicates three feature-creep rows; the workbook lists different additional subtypes instead. Treat the workbook as an intermediate working source; no exact final105-subtype frequency reproduction is claimed. |
| Traceability | Source URLs and coded quotations enable follow-up, but199 URLs for200 titles and the absent S249 appendix do not certify all original identities or corpus overlap with S249. |

The selected quotations materially refine the practice synthesis. Row106 distinguishes fast shipped loading from unchanged slow developer loading and substantial implementation work. Row381 connects mechanic alternatives to animations, dialogue and balancing. Row898 distinguishes the engine's available capability from the developer's time/skill. Row543 reports testability costs at framework boundaries. Row393 explicitly includes unit/game tests and an automated build/deployment pipeline, contradicting a blanket absence-of-automation reading of this released corpus. These are coded retrospective passages, with no independently measured comparator.

The aggregate production/management balance, useful problem taxonomy and favorable/adverse accounts remain evidence despite these release/display differences. Unknown Nu benefit is not resolved by reconciling a denominator; a denominator mismatch also does not erase a source-located practitioner experience. Continue the independent adoption/change frontier and retain exact final-workbook/edition correspondence as a separate gap.
