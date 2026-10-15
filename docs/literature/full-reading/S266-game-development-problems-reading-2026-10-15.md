# S266 — Extended game-development postmortems: source shift, corpus lineage, and denominator failures

Claude Cardinal and Bruno Bouchard, *Evolution of Software Engineering Problems in Game Development: A Longitudinal Empirical Study with an Extended Dataset*, SSRN preprint, [DOI 10.2139/ssrn.7124688](https://doi.org/10.2139/ssrn.7124688).

**Disposition:** this is a complete reading of the selected **unreviewed preprint**, not a final publication. It adds 67 retained postmortems and 300 claimed coded problem instances to a reused 200-postmortem baseline. The contemporary material usefully broadens source contexts and shows that Reddit, Game Developer and GDC Vault produce markedly different problem profiles. That same source change prevents a clean time interpretation. Several displayed totals, percentages, effect-size denominators and AI-agreement claims do not reconcile. The work is therefore useful for task-family discovery and source-aware sampling, but it does not establish industry prevalence, causal longitudinal change, an independent replication of the earlier corpus, or measured labor savings from AI-assisted coding.

## Identity and actual coverage

Native Zotero parent **`7SLKDL8C`**, version **5724**, remains a `preprint` in collection **`PKLXQNEE`**. Existing attachment **`LIHKR9VA`**, version **6637**, resolves to `C:\Users\hadri\Zotero\storage\LIHKR9VA\7SLKDL8C.pdf`. It is **555,179 bytes**, **33 PDF pages**, SHA-256 **`e61da6b8da8f7f408bc1a6128583e3ae3b202852c28b88eb863189f5c2d81dc2`**. The body repeatedly states that it has not been peer reviewed and identifies SSRN abstract 7124688. The PDF metadata names Claude Cardinal, was created 14 July 2026 and modified 15 July 2026; metadata dates are file evidence, not a publication date. Existing child `GHETLQZF` remains an abstract-only text derivative.

All 33 pages were opened and read, including the author-information page, 28 numbered manuscript pages and complete references. Text extraction produced 72,038 characters and all pages parsed. The PDF contains no raster-image objects; its figures and tables are vector/text. Rendered originals were inspected for the collection/coding pipeline, **Figures 1–5**, **Tables 1–6**, statistical formulas, source-stratified results, threats, data notes and conclusion. Private extraction and renders are in `.artifacts/s266-reading-20261015/`; the copyrighted body is not added to Git. No supplement, released row-level dataset, candidate list, prompt, model log or coding workbook was available or read. No reproduction or recoding was run.

## Corpus lineage and units

The paper calls the work a replication and extension, but its empirical dependency is more specific:

| Component | Retained documents | Claimed coded problem instances | Source and period |
| --- | ---: | ---: | --- |
| Reused baseline | 200 | reported variously as 927, 1,000, and implicitly 1,000 in the 1,300 merged total | Gamasutra, described as 1998–2019 |
| Same-venue extension | 14 | 64 | Game Developer/former Gamasutra, actually 2020–2024 in the paper's source audit |
| New source | 25 from 145 candidates | 99 | Reddit, 2019–2025 |
| New source | 28 from 50 candidates | 137 | GDC Vault/YouTube talks, dates not enumerated |
| New material total | **67** | **300 claimed** | 2019–2025 |
| Merged document total | **267** | **1,300 claimed** | 1998–2025 |

The 267-postmortem figure is the reused 200 plus 67 new documents. Accordingly, the statement on p.14 that the “extension comprises 267 postmortems” describes the merged corpus, not 267 independently added postmortems. The design is an **expanded, partly source-changed corpus**, not an independent replication: the earlier records are directly reused in every merged comparison.

The earlier primary lineage matters. [S251](S251-game-problem-dataset.md) reports 1,035 entries for the same 200 titles in its January 2020 repository snapshot. [S250](S250-game-industry-problems.md) reports and passively reproduces **927 entries** for the later analysis, with the same 200 title identities after trimming two spaces. S266 says it downloaded the S250 replication package, checked records against the publication, observed divergences below 7.5%, and merged the recovered baseline with the new data (pp.27–28). It neither gives a row-level reconciliation nor explains why its group table uses a 1,000-instance baseline. The paper's promise that a merged dataset will preserve the baseline cannot presently be checked: data and supplements were anonymized for review and are promised only upon publication (p.28).

## Inclusion, de-duplication and coding

For the same venue, the authors queried Game Developer for 2019–2025 and say they removed duplicates and material that did not qualify as postmortems (pp.7–8). They provide no search string, dated candidate count, identity list, duplicate rule or excluded-item flow for that source. For Reddit and GDC Vault, Microsoft Copilot first identified potential documents; the authors then retained only accounts explicitly discussing what went right and wrong: **25/145 Reddit** and **28/50 GDC** candidates. Candidate identities, query/prompt, Copilot model/version, run date and duplicate handling across sources are absent. The resulting inclusion process is traceable only at aggregate level.

Every retained document then passed the same three-stage labeling protocol (pp.9–13; Figure 1):

1. Copilot proposed taxonomy-constrained labels and associated text spans; it could not add problem types or groups.
2. The first author reviewed every proposal and span.
3. The first author and one game-development expert with more than 20 years of experience, from engineer to CEO, discussed disagreements until consensus.

This gives a human-adjudicated final dataset, but not independent duplicate coding. The AI supplied precodes and did not make explicit reject decisions; the authors correctly say Cohen's kappa is therefore inapplicable. No independent second human labels, blinded decisions, preserved disagreement matrix or chance-corrected reliability estimate are reported. Constraining the model to the old taxonomy improves continuity while making the study unable to discover categories outside it. The paper explicitly names remote collaboration and generative-AI workflow problems as possible blind spots (p.26).

The claimed efficiency is also bounded. The authors say the AI provided a complete first pass and “substantially reduced” annotation effort, but report no elapsed time, person-minutes, comparison workflow, rejected proposals, token/API cost, prompt sensitivity run or stopping burden. This is evidence of an assisted workflow, not a measured productivity effect.

## What the displayed data support

For the **new source-stratified material**, the paper gives a useful descriptive decomposition (pp.24–26):

| Source | Production | Feature management | People management | Business |
| --- | ---: | ---: | ---: | ---: |
| Game Developer, `n=64` instances | 35.9% | 20.3% | 26.6% | 17.2% |
| Reddit, `n=99` | 28.3% | 11.1% | 11.1% | 49.5% |
| GDC Vault, `n=137` | 59.1% | 14.6% | 19.7% | 6.6% |

Marketing is **43.4% of Reddit instances**, compared with 12.5% in Game Developer and 5.1% in GDC Vault; design is 29.2% in GDC versus 12.5% and 11.1%. The authors therefore qualify the aggregate marketing increase as mainly Reddit-driven and directional rather than industry-wide. This is the paper's strongest comparative result because the source-conditioned denominators are explicit. It also reveals the core confound: the later period adds independent/small-studio Reddit accounts and established/AAA conference talks to a professionally edited baseline. Period and source/context change together.

Time coverage is uneven. The same-venue subset covers 2020–2024 and supplies no 2019 or 2025 document; Reddit spans 2019–2025 and contributes 12 problem instances from 2025. The text says the two most recent years are exclusively Reddit, but does not supply GDC dates that would let a reader verify that statement. Figures 4 and 5 plot annual **counts** with dashed second-order polynomial curves for aggregated technical/tool/bug problems and marketing/monetization/design problems. The authors call the curves visual indicators rather than predictive models. No coefficients, uncertainty bands, per-year document denominators or cluster-aware estimates are reported. Leave-one-postmortem-out jackknife, year-balanced bootstrap, Theil–Sen slopes, Kendall's tau and permutation-based trend tests are proposed for subsequent replications; they are not results of this study (pp.21–24).

The interpretive “risk displacement” account—mature technical infrastructure reduces visible low-level problems while design, coordination and market risks become salient—is a plausible hypothesis, not a tested causal mechanism. Source mixture, selected published postmortems, different document structures, changing numbers of problems per document and the absence of a source-balanced time comparison all permit alternatives.

## Arithmetic and reporting audit

Several paper-level inconsistencies materially limit the reported effect sizes. These are arithmetic checks against the displayed tables and figures, not a recoding of unavailable rows.

- **Baseline denominator:** Figure 2's 20 type counts sum to **927**, agreeing with S250. Table 3 instead reports baseline group counts `477+218+215+90 = 1,000`. Neither the table nor the data notes reconcile the 73-instance difference.
- **Extension type rows:** Figure 3's 18 displayed type counts sum to **297**, although the extension is repeatedly `N=300`. Documentation and security are absent from the figure, but the paper does not assign the missing three instances, so their categories cannot be inferred.
- **AI table totals:** Table 1's displayed AI column sums to **296** and its human-review column to **297**, while the printed total row says 300 for each. Again, no allocation for the omitted rows is supplied.
- **AI “agreement”:** the source paragraphs report 59/64 confirmed for Game Developer, 77/99 for Reddit and 129/137 for GDC Vault. These total **265/300 = 88.3%**, not the **83.4%** repeated in pp.19 and 28. Even 88.3% is proposal-to-final convergence under human adjudication, not independent accuracy or reliability.
- **Displayed percentages:** Table 2 gives Technical as count 24 but 7.30%; `24/300 = 8.00%`. Figure 3 and Table 1 also use 24. Table 4's percentage-point changes are not reproducible from its displayed type counts and the 927 baseline: Marketing is `53/300 - 61/927 = +11.09 pp`, not +10.57; Design is +9.25, not +8.43; feature creep is -2.58, not -4.37.
- **Type effect-size denominator:** the paper reports a 16-by-2 table, chi-square 105.45, and computes Cramer's `V=sqrt(105.45/1300)=0.285`. The displayed type totals are 927 for the baseline and 297 for the extension before restricting to 16 common types; a restricted table must be smaller still. `N=1300` is therefore unsupported for this displayed type comparison.
- **Group versus type inference:** the group result, chi-square(3)=155.93 and `V≈0.346`, can at least be traced to Table 3's separate 1,000+300 accounting. It does not repair the type denominator or establish that either baseline agrees with the released 927-entry S250 corpus.
- **Dependence:** inferential tests treat problem-instance counts as the observations while multiple instances are nested in each postmortem and postmorterms are nested in source. No cluster-aware standard errors, document-level resampling or source-balanced primary model is reported. The 10,000-permutation statement does not specify a permutation unit that resolves this dependence.

These discrepancies mean the exact magnitudes and significance claims should not be carried forward as validated. The qualitative source split and the direction of selected displayed proportions remain usable with their denominators stated.

## Consequence for Nu task provenance

S266 expands the practical source map behind [the R14 provenance record](../../nu-practice-and-task-provenance-2026-10-11.md). Its postmortems again place game change work across production, tools, testing, design, people, planning and business rather than source code alone. The new GDC/Reddit split is especially useful when choosing a task population: an independent developer's discoverability and resource-allocation burdens are materially different from an established studio's production/pipeline account. A future task should name the beneficiary, studio/source context, represented artifact and observed outcome instead of citing an aggregate postmortem rank as prevalence.

The paper does **not** show that any prepared Nu direction solves the reported problems, that technical work has become unimportant, or that a task from the added corpus is representative. Problem-instance shares are not shares of projects, severity, engineer-hours, failed deliveries or benefit from an intervention. Marketing and design concerns can motivate broader cost boundaries, while the selected Nu maintenance comparisons still need matched requirements, ordinary alternatives and behavioral outcomes.

For agent-assisted research, the coding protocol supplies a useful caution: constrained machine proposals followed by human adjudication can organize a corpus, but proposal acceptance is not independent validation, and missing prompt/run/effort records prevent a productivity conclusion. This supports preserving every assigned attempt, source identity and human correction in later work; it does not validate an autonomous candidate workflow or replace final scoring.

**Next consequential use:** integrate the source-conditioned task-family evidence and the denominator caveats into R14/background synthesis. Treat the 67-document addition as an expanded corpus sharing the S250/S251 lineage. If exact longitudinal magnitudes matter, first obtain the promised row-level release and reproduce document identities, de-duplication, the 927/1,000/1,300 mappings, category totals and document-level/source-balanced analyses. No experiment, new retrieval, Zotero mutation or independent replication is claimed here.
