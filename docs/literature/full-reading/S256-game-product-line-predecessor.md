# S256 — Game product-line predecessor and shared experiment

Jose Ignacio Trasobares, África Domingo, Lorena Arcega and Carlos Cetina, *Evaluating the Benefits of Software Product Lines in Game Software Engineering*, SPLC 2022, Volume A, pp. 120–130, [DOI 10.1145/3546932.3546998](https://doi.org/10.1145/3546932.3546998). Main-agent reconstruction, 2026-10-04. **Complete selected author edition:** all 11 PDF pages, five figures, four tables, equations 1–3 and 38 references. Publisher-copy correspondence remains unverified; the 2023 JISBD same-title dissemination is not another experiment.

This is the original 28-person model-driven experiment reused in [S255](S255-game-product-lines-comparison-partial.md). Product-line composition improves rubric-based correctness, while efficiency and satisfaction differences are inconclusive. Reading the predecessor and checking the released file lineage strengthens the interpretation of one experiment; it does not add another sample or independent replication.

## Identity, access and holdings

Collection `PKLXQNEE` contained 281 parents before selection. Collection DOI/title and library DOI/title/author checks found no match. Native parent **`T8Z46UUP`5580** and note **`6VEUIXL4`5581** preceded selected reading. The current [author PDF](https://svit.usj.es/api/media/file/Trasobares_SPLC_2022_PRE.pdf) succeeds through an ordinary request with a browser user-agent; the old WordPress route returns 404, and the attempted ACM download returns 403. No institutional access, purchase or author contact is assumed.

| Native attachment | Bytes and SHA-256 |
| --- | --- |
| PDF `IIQALBY9`5583 | 1,036,801; `074f861a850fdee7ade3d9a694a06e4376d2cbf1c124a796882ffe2089b81024` |
| Statistical analysis ZIP `64SVDQLM`5587 | 6,189,171; `dd93a6878d6eb9586de6d2b264cb1fd9153a201751d7e5ebff37ac480a1a7faf` |
| Experimental objects ZIP `26JVG6RF`5589 | 2,458,828; `addfd8e9f3efd8a13cf699812f5637f12eab232d47c72ece6faf8e9e8d79fb14` |
| Results ZIP `GX3HNTQR`5591 | 60,095,320; `b7cfd556584fdf13aa1e478e89d2ae5d0edda0bcb258115f7fbc0820fc45c0ad` |

The PDF metadata records generation on 27 July 2022; its title, authors, conference and DOI match the selected work. All pages were read textually and inspected in three contact sheets; mechanism, result and table pages 2, 3, 6, 7 and 8 were additionally inspected at full-page resolution. The [replication package](https://zenodo.org/records/14674528) explicitly supplements this DOI: version 14674528, concept 14674527, metadata publication date 12 September 2022, actual record creation 16 January 2025. All three declared MD5 values and native stored SHA-256 values match. Web access fails, while the ordinary public metadata/file API succeeds. These are acquisitions and passive checks, not historical-release equivalence or experimental reproduction.

## Mechanism, assignment and outcomes

Kromaia's SDML describes boss hulls, links, vulnerable points, weapons and shields, with models interpreted into C++ runtime objects. That game architecture provides the task domain. The comparison itself gives participants prepared models and representations:

- **Clone and Own:** adapt existing SDML boss examples and submit a complete graphical model.
- **Product line:** use a supplied initial model, feature fragments and permitted substitutions. Figure 3 shows nested variation points: choosing one fragment can expose further points to fill. The task instructions accept feature-to-hole assignments without a complete drawing.

Both approaches reconstruct bosses from gameplay videos. Participants can consult training material, examples and domain information; only the product-line treatment receives its particular variability specification. This is a representation/support bundle. Neither arbitrary expressive equivalence nor tool/library setup cost is held constant or measured.

The study invites 20 professionals: 13 participate and complete. Of 20 invited students, 16 agree and 15 complete tasks/forms. The analyzed cohort therefore contains 13 professionals and 15 students, plus a separate two-person pilot excluded from the experiment. One incomplete student is visible in the recruitment account; the released analysis input has 56 task rows, two per included person. No invented outcome or missingness reason is assigned to the incomplete case.

Random assignment places people in CaO→SPL or SPL→CaO sequences. Everyone performs task 1 before task 2; method order is counterbalanced, task order is fixed. Professionals attend online and students in person, with one session per group. Experience, cohort and setting therefore cannot be cleanly separated. An observed period effect can include task difficulty and practice; it is not an isolated learning estimate.

Correctness is a correction-template score out of 100, applied after submission. Efficiency is correctness divided by recorded task minutes. Satisfaction uses averaged TAM items for ease of use, usefulness and intention to use. The paper says a game engineer prepared the tasks/templates; no distinct item-level scoring rubric or adjudication record was located in the package inventory and inspected materials. The shared forms establish handwritten/model submissions, without a requirement to compile, integrate or test a running boss.

| Outcome, CaO → SPL | Result and scope |
| --- | --- |
| Correctness | 51.875 → 64.132 points: +12.257 points, about 23.63% relative; reported p=.028. Table 3 and the summary workbook give d≈−.506 with CaO-minus-SPL orientation. |
| Correctness per minute | 3.415 → 3.293; reported p=.678. Inconclusive, not evidence of equivalence. |
| Mean recorded minutes | 18.429 → 20.679: about 12.21% longer with SPL. These are the shared raw-input means, not a separate experiment. |
| Ease of use / usefulness / intention | 3.542→3.786 / 3.799→3.701 / 3.304→3.268; reported p=.192/.684/.993. Preserve all three inconclusive contrasts. |

The selected mixed models include subject-level repeated observations and different fixed-factor combinations for performance and satisfaction. The authors choose among models using residual checks and AIC/BIC. The paper's statement that a 95% confidence level minimizes low power is insufficient; confidence level does not establish power. The observational experience contrast and model-selection/multiple-outcome context constrain causal interpretation. No statistical model is rerun.

The focal means and hypothesis results match S255's MDD results and the already-inspected shared input. Figure 4 retains increased SPL spread and low scores; Figure 5 retains similar efficiency distributions. There is no success/outlier filtering in our descriptive check. The focus-group explanation—that extracting the required boss from video consumes time in both approaches—is useful participant testimony, without an independently timed mechanism decomposition. Suggested content variation and difficulty balancing are future uses, not measured player-quality or balancing effects.

## What the package comparison resolves

The three ZIPs contain **85 files: five XLSX, one SAV, 17 SPV, eight PDF and 54 standalone images**. Hash comparison finds **78 byte-identical files** in S255's journal package, including both original/input workbooks, the SDML explanation, both task forms, focus questions/notes and all 56 participant task submissions. This independently binds released evidence to the shared MDD cohort. Previously recorded material coverage is reused; submissions remain inventoried rather than individually read or rescored.

Seven files differ: three analysis workbooks, one SAV, two SPV and one 25-page training PDF. The three workbooks are passively parsed; selected coverage comprises the first descriptive workbook's two compact outcome/effect tables, the hypothesis workbook's result rows 1–10, and metadata/header screening elsewhere. The focal p-values match Table 4. No SPSS data/output is decoded or run and no spreadsheet formula is executed.

Two bounded discrepancies matter for lineage, without erasing the principal outcomes:

- The original Table 2 repeats both sequence means as 4.5 for CaO efficiency and 3.27 for SPL. The non-`_MDD` workbook's compact table repeats those cells. Shared raw rows instead give G1/G2 means 2.470/4.504 for CaO and 3.310/3.273 for SPL, with 15/13 people per sequence. The 2023 table corrects these sequence cells. The overall means remain consistent. Table 3/workbook also give correctness d≈−.506 rather than the −.516 mentioned once in prose.
- `SPL_vs_CaO_Estudiantes.pdf` in the nominal 2022 package teaches **C++/feature-tree tasks**, although the 2022 experiment is SDML-based. All 25 extracted pages are read; pages 15, 17, 24 and 25 are visually inspected. Twenty-two page texts match the later CDD training deck after alphanumeric normalization, with changed schedule/access instructions and an extra final page. It cannot establish which training was delivered in 2022. The unchanged SDML explanation, forms and data provide the bound MDD evidence. The reason for the later package mixture is unknown.

These are checks of the released versions, not claims about an undisclosed earlier archive. All hashes, inventories and extraction bodies remain in ignored local artifacts; only this reconstruction is committed.

## Consequence and next action

For Nu, the combined S255/S256 result is a useful positive precedent for supplied domain choices: they can improve specification of supported content while leaving total time, expressiveness, requirements discovery and integration unresolved. It does not establish that graphical models outperform code generally, that game product lines cannot improve efficiency, or that D1's explicit-case convention beats an equivalent catch-all. One family of prepared boss tasks cannot settle lifecycle benefit.

The predecessor method and sample linkage are now reconstructed. Distinct scoring-template access, historical package fidelity and overlap between the later CDD people and prior Kromaia studies remain separate limits. Next inspect the retained **2025 Unreal model/code experiment**, DOI 10.1109/MODELS67397.2025.00016, to establish its actual tools, tasks, feedback and outcomes. Phylogenix, modern practice and temporal/state frontiers remain open by consequence. No construction, runtime, author code, statistical fit, model worker or experiment is executed.
