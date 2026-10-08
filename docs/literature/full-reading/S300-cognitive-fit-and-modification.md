# S300 — Comprehension and modification progress depend on the task

Teresa M. Shaft and Iris Vessey, *The Role of Cognitive Fit in the Relationship Between Software Comprehension and Modification*, MIS Quarterly 30(1), 2006, pp. 29–55. [DOI 10.2307/25148716](https://doi.org/10.2307/25148716); [institutional PDF](https://shareok.org/bitstreams/c581914e-1780-4afc-be7a-d21a4e9d0111/download).

**Coverage:** all 27 journal-layout pages are read textually and visually, including eight figures, five numbered tables, eight footnotes, the printed references and both appendices. Appendix A supplies four task specifications; Appendix B supplies their four scoring rubrics. Original programs, complete question sets, individual responses, analysis code and raw execution records are not acquired. This is reconstruction of one professional experiment, not a new experiment or independent statistical reproduction.

## The question and the manipulation

The paper treats maintenance as interacting comprehension and modification activities. Its cognitive-fit theory predicts that additional comprehension is associated with better modification performance when the maintainer's dominant understanding emphasizes the knowledge needed by the task. With a mismatch, the two activities may compete for attention (pp. 31–37, Figures 1–5). Domain knowledge is expected to support a functional/domain model, while unfamiliar domains are expected to induce attention to program control flow. These mental representations and the proposed attention mechanism are inferred from the manipulation and outcomes, not directly observed.

The main study uses **24 IT professionals**, each performing the same kind of enhancement in two domains, giving **48 repeated observations**, not 48 independent maintainers. Participants develop or maintain COBOL accounting applications; mean professional IS experience is 10.7 years, with no hydrology/scientific-domain experience. They are randomly assigned to function or control-flow modifications, twelve per type. Domain order and pre/post question-set order are counterbalanced. Accounting is familiar and hydrology unfamiliar for everyone (pp. 37, 41).

Thus the two fit conditions are familiar accounting with a function enhancement and unfamiliar hydrology with a control-flow enhancement. The other two combinations are mismatches. A familiarity rating supports the domain manipulation. Familiarity is nevertheless tied to these particular domains/programs; it is not randomized independently within each program.

The original programs contain about 417 and 416 source lines and derive from operational payroll and water-quality programs. The researchers improve naming, organization and, for hydrology, structure before use. They compare size, data density, decision density and perceived difficulty. These checks support their intended comparison without establishing equivalence of every semantic demand. Table 1 prints 150 accounting procedure lines while the prose and relevant Table 2 arithmetic use 160; Table 2 also prints `1060` in one original-program cell. These are reporting discrepancies, not observed differences between participant artifacts.

## What participants did and what was scored

After practice, each domain session supplies **15 minutes of initial study**, an untimed comprehension questionnaire without source access, **35 minutes of modification**, and a different untimed comprehension questionnaire, again without source access (pp. 41–42). Participants have source, a one-page change specification, sample inputs/outputs and listings with record-format changes already supplied. The pilot led the researchers to preimplement those time-consuming DATA DIVISION changes; WORKING-STORAGE changes remain the participant's responsibility. This preparation increased progress within the allotted time and is part of the task boundary.

Control-flow tasks add a reporting control break: budget-code subtotals/FICA for accounting, or per-well aggregate statistics for hydrology. Function tasks add address-file updates and mismatch reporting, or threshold-based water recheck messages. Appendix A expressly asks for the new outputs while preserving other outputs. Participants can compile, link, run and inspect results; practice demonstrates that workflow. Availability of those actions is distinct from an independently recorded behavioral verdict for every submitted change.

Each comprehension set has twenty yes/no questions: five each for function, data flow, control flow and state. Two sets per domain are counterbalanced; reported reliability values range .60–.83, averaging .72 (pp. 39–40). The normalized change score is `(final − initial)/(100 − initial)` for improvement and `(final − initial)/initial` for decline. It is a fraction of possible improvement or decline, not simply final understanding or raw percentage-point gain. The authors report similar hypothesis results with ordinary difference scores. A separate assistant scores questionnaires, and those scores are unavailable to the researchers while they score modifications.

Modification performance is a **100-point progress rubric**, not elapsed time to successful completion (p. 43; Appendix B). Implemented subtasks receive credit; a subtask not entered online can earn up to 75% credit from handwritten changes. The rubrics include recognition and intermediate work as well as functional operations. Errors are not explicitly deducted because the authors regard the lost progress as their penalty; they report few errors and little additional quality variation. Consequently, these scores should not be relabeled correct-program percentages, delivered defect rates or completed-change success.

The first author assigns scores. As a validity check, that author and a hypothesis-blind assistant separately rank five submissions per domain/task cell, and the rankings correlate .82–1.00 with rubric ranks. This is a useful check on judged progress; the entire scoring procedure is not independently blinded, and this comparison does not validate a separate runtime oracle.

## Preserve the positive, negative and null findings

The mixed-model analysis includes domain, task type, measured comprehension change and their interactions, accounting for repeated observations. The reported three-way interaction is **F(1,22)=8.77, p=.007**; a rank-transformed analysis reports **F(1,22)=8.62, p=.008** (pp. 43–45, Table 5). Figure 6 gives the following within-condition correlations. The table also includes Table 4's mean progress scores to keep slope and average outcome distinct:

| Domain and task | Proposed fit | Correlation of comprehension change with progress | Mean progress /100 |
| --- | --- | --- | --- |
| Accounting, function | Fit | +.52 | 50.75 |
| Hydrology, control flow | Fit | +.49 | 38.00 |
| Accounting, control flow | Mismatch | −.35 | 54.08 |
| Hydrology, function | Mismatch | −.30 | 39.92 |

The interaction and directional correlations support the paper's task-dependent account. They are not four separately established significant effects or evidence that the fit groups have uniformly higher average progress. Ten observations across nine maintainers show comprehension declines and are retained, across all four conditions. The authors suggest task-focused attention as an explanation, but do not directly measure that mechanism.

The main-effects-only model finds domain familiarity associated with progress, while comprehension change and task type alone are not significant. Substituting initial or final comprehension for change does not yield significant comprehension terms in the reported alternative models (pp. 45–47). These are inconclusive results for those predictors in this study, not proof that prior knowledge never helps. Reported model-fit comparisons and small-sample/rank checks are author analyses; no raw-data replication is claimed here.

## What can transfer to a Nu value claim

The study provides substantive professional evidence against treating a higher general comprehension score as a universally favorable maintenance proxy. Its positive fit-condition relationships deserve preservation alongside its negative mismatch relationships. The important practical implication is to align the understanding being supported with the actual change, while measuring change performance as its own outcome.

Our inference is narrower than saying that more understanding causes harm. **Comprehension change is measured during the modification and is not an assigned treatment.** Progress and comprehension can both depend on attention allocation within the same time allowance. Mental representations and dual-task interference are not directly observed. Random task assignment does not turn the comprehension–progress association into an isolated causal effect of comprehension, nor does it establish a language or architecture effect.

The setting is two prepared COBOL enhancement programs with short fixed work periods and experienced accounting maintainers. It supplies no Nu/F#/C# comparison, coding-agent effect, live-game temporal guarantee, completed-change timing or net lifecycle-cost estimate. A separate population, task, representation and outcome comparison would be needed for those claims. Full instruments and raw records are specified gaps; they are not evidence against the observed scoped result. No contact with authors or new data collection is performed.

For B01/B10/B11/B12, combine this result with [S83's task-dependent maintenance study](S83-program-structure-maintenance.md), the linked S155/S156 document-task evidence and professional workflow studies. Keep **representation → actual understanding → modification progress → verified new and retained behavior → total cost** distinct. In a future authorized Nu comparison, comprehension could explain an outcome, but conditioning on achieved comprehension should not be presented as the pure total effect of the assigned source/tool treatment. [S299's preservation contract](S299-modular-reactive-verification.md) and [S298's substitution/checking boundary](S298-interaction-typing.md) establish different links in that chain; neither supplies this human result, and this study supplies neither formal guarantee.

## Edition and native evidence

The institution supplies a complete 27-page journal-layout file with printed pages 29–55, March 2006, not an abstract or a newly independent study. The download redirects to the institution's content endpoint. It is **463,424 bytes**, SHA256 `6ce4d3b93909ae19a32de1c8c1fcba61bc526e301ac551a2a6dd51bc6006e9d1`, MD5 `2578f6c269cf05462d5b8ab86e8bfbc9`; extraction contains 119,175 characters. No PDF hyperlinks supply the omitted experimental packet. The printed question-set footnote offers author contact, which is not an acquired supplement or permission to send a message.

Before reading, native Zotero confirms parent **`B6V32YJI`** version 6032, note **`FQ5PNFUT`** version 6033, collection `PKLXQNEE` and sole PDF **`H85I5WLF`** version 6041, with exact stored bytes/hashes. Final native versions and the source-decision audit are in the [search ledger](../nu-background-searches-2026-09-30.md). Copyrighted bodies, extraction, renders and API snapshots remain outside public Git. All construction and experimental holds remain.
