# S265 — Unity build configuration: power, frames and artifact correspondence

José Miguel Aragón-Jurado, Ruck Thawonmas, Patricia Ruiz and Bernabé Dorronsoro, *Native code, greener games? Investigating energy efficiency in Unity builds*, **Entertainment Computing 57** (2026), 101132, May 2026; online 30 April 2026. [DOI 10.1016/j.entcom.2026.101132](https://doi.org/10.1016/j.entcom.2026.101132). Full publisher-PDF reading completed 15 October 2026, extending the 4 October indexed-text/artifact reconstruction. No engine, compiler, benchmark or author analysis code was executed.

## Identity and coverage

The native Zotero parent **`DMZN5HBS` version 5709** is the journal article with the exact title, four authors, date `2026-05`, DOI and collection `PKLXQNEE`. Its attachment **`4QRS6N42` version 6691**, titled *Full text PDF — retrieved via HKUST workspace (12 October 2026)*, resolves to `DMZN5HBS.pdf`: 3,165,249 bytes, SHA-256 **`55888c06e3f3906b9f10bfa716918b20c94630af5e4d4c4aa7c1208ddb3a9a4a`**, PDF 1.7, 15 pages, unencrypted. PDF metadata names the article, journal/issue/article number, first author and DOI; page 1 agrees on title, authors, DOI, final pagination and submission/revision/acceptance dates (16 November 2025 / 12 March 2026 / 22 April 2026). This verifies the final publisher edition rather than only correspondence to the earlier ResearchGate/indexed text.

All **15/15 original pages** were rendered and visually read. Coverage includes all four tables, Figs. 1–7, equations, footnotes, threats, data statement and references. The visual pass specifically inspected the methodology and GPEEQ schematics (Figs. 1–3, pp. 4 and 6), all five NPSK panels (Fig. 4, p. 8), the GPEEQ panels (Fig. 5, p. 10), the exact win-count bars (Fig. 6, p. 11), and every displayed Spearman coefficient/significance weight (Fig. 7, p. 12). The private receipt at `.artifacts/s265-reading-20261015/coverage-receipt.md` records the render and extraction hashes. The article's Appendix A only points to DOI-hosted supplementary material (p. 13); no supplement or raw four-game benchmark bundle is present locally, so the statistical analyses are not reproduced.

Two earlier native attachments remain useful and unchanged:

| Native attachment | Exact identity and role |
| --- | --- |
| Indexed text **`XLR9VRH5` version 5705** | 117,303-byte UTF-8 text; SHA-256 `ff14cfb16ba72ab7f997a1f75ff1d6c451e18af03629afc297d0edad688a51f5`. Its 2,861 selected lines supplied complete searchable body text but not the figures. |
| Selected artifact **`ZJQTP8T4` version 5707** | 724,897-byte locally assembled 46-file ZIP; SHA-256 `9e9917d3617c766e55f72a7e1ef64bfe8d82a719747223edf9a4db504b40cc38`. It preserves a bounded selection from the public repository, not an author-issued replication package. |

## What is measured: power, not run energy

The article repeatedly uses “energy consumption” and “energy usage,” including in the research questions and procedure (pp. 2–3). The implemented and reported observations are narrower:

- `powermetrics` supplies **average CPU and GPU power** and clock frequencies at the system level, not per-process measurements (p. 5). The released shell script averages matching CPU/GPU power samples and defines total power as their sum. It contains no time integration, wall-plug measurement, whole-device energy observation, or compilation-energy measurement.
- Power Up is the ratio `P_optimized / P_baseline`; GPEEQ uses this power ratio jointly with the analogous average-FPS ratio (Eq. 1–2, pp. 3–4). Its “energy-efficient/equivalent” labels therefore classify average power and FPS groups. “Equivalent” means that NPSK did not distinguish the configurations at the selected confidence level and placed them in the same group; it is not an equivalence test or a predeclared tolerance.
- Equation 3 defines `E_frame = P_avg / FPS` (p. 4). The dimensions are correctly J/frame when watts are J/s and FPS is frames/s, but this is a **derived average energy per rendered frame**. It is not a measured whole-run joule total, and the unreleased FPS-monitor/replay implementation prevents verification that the two averages share an exact observation window and useful-work denominator.
- The paper sometimes calls CPU+GPU sum “total average power consumption of the device” (pp. 9–11). The released data establish CPU+GPU sum, not coverage of display, memory, storage, networking or the complete device. Maximum screen brightness was held constant, but display power was not included in the released total.

Thus the favorable findings support configuration-dependent CPU+GPU power and derived J/frame differences under these workloads. They do not establish whole-device or lifecycle energy savings, compilation energy, battery life, or equal delivered gameplay.

## Design, comparator, hardware and workloads

The study keeps each backend's default configuration and changes only selected compilation parameters (p. 3). It evaluates **14 builds**: Mono and Development Mono; and IL2CPP Faster Build or Faster Runtime, each crossed with Debug/Release/Master and with/without Development (`FB-D/R/M`, `Dev-FB-D/R/M`, `FR-D/R/M`, `Dev-FR-D/R/M`; Table 1, p. 6). GPEEQ uses **Development Mono** as the common non-optimized baseline (p. 9), leaving 13 alternatives per game and **65 classified game/configuration cells**. Each configuration/game cell has 30 fresh executions, with application/runtime restart, minimized background activity, a warm execution, CPU/GPU preconditioning and maximum screen brightness (pp. 3–5). These controls do not make the five games or 65 cells independent replications of a single treatment effect.

Hardware/software is one MacBook Pro with an Apple M3 Pro (5 performance CPU cores, 6 efficiency cores, 14-core integrated GPU), macOS Sequoia 15.5, Unity 6 `6000.0.45f1`, and macOS `powermetrics` (p. 5). Memory capacity, exact MacBook model/power mode and external power instrumentation are not reported. A separate FPS-monitor check on FPSGame/Development Mono reports an average-total-power difference below 1.75% and no Mann–Whitney U significance at 95% across 30 independent runs (p. 5); non-significance does not establish negligible or equivalent overhead.

The fixed-window automated workloads are source-located on p. 6:

| Project | Automated work and nominal duration |
| --- | --- |
| FantasyKingdom | Continuous environment traversal with camera rotation; 5 minutes. |
| BossRoom | First-level automated gameplay; 3 minutes. |
| FPSGame | Eliminate all enemies on the map; 1 minute. |
| Platformer | Full playthrough reaching the goal; approximately 1.5 minutes. |
| Roguelike | Progress through levels until player death; 1 minute. |

Fig. 3 shows capture by an `InputRecorder`, a recorded-gameplay CSV, and frame-by-frame replay by an `InputReplayer`. The repository omits the project `Assets`, recorder/replayer, FPS monitor and shipped executables, so deterministic scheduling, matched trajectories, elapsed-time averaging and final-state equivalence remain assertions rather than reconstructed behavior. Fixed time within a game does not make workloads, durations or useful output comparable across games.

Tables 2–3 (p. 7) characterize rather than balance those workloads. Exact static counts are:

| Project | CPU allocation patterns | Dynamic-object uses | Read/write meshes | Non-batch SRP shaders |
| --- | ---: | ---: | ---: | ---: |
| FantasyKingdom | 16,047 | 90 | 58 | 44 |
| BossRoom | 13,148 | 121 | 0 | 0 |
| FPSGame | 9,423 | 111 | 75 | 120 |
| Platformer | 14,071 | 88 | 0 | 0 |
| Roguelike | 16,351 | 106 | 0 | 18 |

Table 3 labels FantasyKingdom's GPU/shared-dependency load Very High/Very High, FPSGame's High/High, BossRoom's Med-Low/High, Platformer's Med-Low/Medium and Roguelike's Medium/Medium; its CPU labels range from Medium to Med-High. The paper says all five use only official Unity modules/standard packages and no third-party static libraries. At the pinned public commit, however, BossRoom's manifest also declares ParrelSync and VContainer. This makes the blanket package description too broad; it does not itself show that either dependency was exercised or contributed native code to the benchmark.

## Exact publisher results and statistics

NPSK at a 95% confidence level ranks configurations separately for CPU power, GPU power, their sum and FPS; rank 1 is best in the desired direction (pp. 5, 8). The paper says NPSK clusters medians using significance and practical relevance without normality/equal-variance assumptions. The supplement/package needed to verify package version, effect-size settings, all p-values and the claimed power analysis is absent. The released R script calls `sk_esd(model_performance)` only for the FantasyKingdom matrices and was not executed here.

Table 4 (p. 9) gives the exact best NPSK group for derived `P_avg/FPS`:

| Project | Configurations in the best group |
| --- | --- |
| FantasyKingdom | Dev-FR-R, FB-R, FB-M, FR-R, FR-M, Mono |
| BossRoom | FR-M |
| FPSGame | FB-M |
| Platformer | FB-M |
| Roguelike | FB-R, FR-R, Mono |

Fig. 5 and its prose (pp. 9–10) classify **34/65** alternatives as lower-power “energy-efficient”: 27 Category 1 (lower power, higher FPS; 79.41% of 34), one Category 2 (lower power, no detected FPS difference; 2.94%), and six Category 3 (lower power, lower FPS; 17.65%). This retains the favorable result while showing that only 27/65 cells combine both favorable directions. The same figure/prose classify **46** alternatives as higher-FPS, seven of them Category 4 with no detected power difference, giving the reported `7/46 = 15.22%`.

The original publisher PDF exposes a precise internal/release mismatch. Fig. 5(e) places **Roguelike Dev-FB-D in C6** (higher power, higher FPS), whereas Fig. 6's frame-up bar gives Dev-FB-D only one higher-FPS game. The released literal sign table marks Dev-FB-D higher-FPS for Platformer but lower-FPS for Roguelike, which would put that Roguelike cell in C8 and yields **45** higher-FPS cells and `7/45 = 15.56%`. All other Fig. 5 higher-FPS placements reconcile with the Fig. 6 counts. Thus the paper's prose and Fig. 5 agree on 46, while the paper's own Fig. 6 and pinned released classification agree on 45; the PDF closes the visual gap but does not adjudicate the underlying measurement.

Exact Fig. 6 counts (overall-power, CPU-power, GPU-power decreases and FPS increases across five games) are:

| Build | Overall | CPU | GPU | FPS |
| --- | ---: | ---: | ---: | ---: |
| FR-R | 5 | 5 | 4 | 5 |
| FB-R | 5 | 5 | 4 | 4 |
| FR-M | 4 | 4 | 4 | 4 |
| Mono | 4 | 4 | 4 | 4 |
| FB-M | 4 | 4 | 3 | 4 |
| Dev-FR-R | 4 | 3 | 4 | 5 |
| Dev-FR-M | 2 | 2 | 2 | 5 |
| Dev-FB-M | 2 | 2 | 2 | 4 |
| FR-D | 2 | 1 | 1 | 2 |
| FB-D | 2 | 0 | 2 | 1 |
| Dev-FB-R | 0 | 1 | 2 | 4 |
| Dev-FR-D | 0 | 0 | 3 | 2 |
| Dev-FB-D | 0 | 0 | 2 | 1 |

FR-R is the only configuration with favorable overall power and FPS in all five Fig. 6 game counts; FB-R lowers overall power in five but increases FPS in four. Development Release/Master variants can have five FPS wins without consistent overall-power wins. No configuration lowers GPU power in all five games. These are win counts, not effect sizes, and each denominator is five heterogeneous projects.

Fig. 7 (p. 12) reports Spearman correlations across the 30 executions of each compiled build. Bold entries are the paper's `p < 0.05` cells:

| Build | FantasyKingdom | BossRoom | FPSGame | Platformer | Roguelike |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dev-FB-D | **−0.6595** | **+0.6650** | **+0.4155** | **+0.6300** | **+0.5343** |
| FB-D | −0.2900 | **+0.7001** | **+0.5993** | −0.1155 | −0.0216 |
| Dev-FB-R | −0.2626 | **−0.7800** | +0.1163 | **+0.5461** | +0.1335 |
| FB-R | −0.1834 | **+0.3782** | **+0.5386** | −0.1045 | +0.1436 |
| Dev-FB-M | **−0.6358** | +0.2819 | **−0.4702** | +0.3156 | +0.2457 |
| FB-M | **−0.7373** | **+0.5753** | **+0.4565** | +0.1102 | −0.1313 |
| Dev-FR-D | −0.2473 | **+0.6426** | **+0.4729** | **+0.4379** | +0.1886 |
| FR-D | **−0.4639** | **+0.6836** | **+0.5397** | **+0.5041** | +0.2039 |
| Dev-FR-R | −0.2081 | +0.1478 | −0.0564 | −0.2090 | −0.0747 |
| FR-R | **−0.6497** | −0.0301 | **+0.6700** | −0.0202 | −0.3520 |
| Dev-FR-M | **−0.4145** | **+0.4914** | −0.1095 | −0.3343 | +0.0536 |
| FR-M | −0.2647 | **+0.4141** | **+0.4072** | +0.2162 | +0.0660 |
| Dev-Mono | **−0.5773** | +0.2770 | +0.1396 | +0.1312 | −0.0614 |
| Mono | −0.1249 | +0.1136 | **+0.5900** | +0.0999 | −0.3005 |

The two prose examples agree with the figure: FantasyKingdom FB-M `ρ = −0.7373, p = 3.36×10⁻⁶`; BossRoom FR-D `ρ = +0.6836, p = 6.07×10⁻⁵` (p. 11). Signs and significance vary by build and game; the authors explicitly call the correlations exploratory and non-causal. This is adverse evidence against treating faster execution as a general proxy for lower power.

## Reconciliation with the pinned released material

The prior bounded source audit remains unchanged. The public repository is pinned at commit **`7498de8ea2a1cb3f633eff1da8b39e470af72fe1`** (11 August 2025, *Final scripts*). Its recursive tree had 426 entries; the selected 46 files cover provenance/README, four measurement or analysis scripts, five editor-version files, five manifests, 24 CSVs, two input-recording ZIP inventories/bounded contents and four charts. This is enough for correspondence checks, not a runnable benchmark reconstruction.

The measurement script's literal `powermetrics` interval is `-i 1`, although its comment/README call this one-second sampling; that interpretation was not executed or verified. It converts missing CPU matches to zero and GPU/FPS misses to `NA`. The plotting source drops `NA`, expects Mono filenames with an extra `-Build`, reuses a CPU dataframe in one path, and does not establish that it generated every published table. These static observations bound the released pipeline without asserting that any reported run was missing.

Fourteen FantasyKingdom result files contain **420 complete finite 10-field rows**, 30 per configuration. Four 30×14 matrices reproduce **1,680 derived cells**: CPU/GPU mW-to-W conversion, FPS values and CPU+GPU totals, with maximum floating-point difference `3.56×10⁻¹⁵`. No equivalent raw result CSVs for the other four games occur in the pin. Descriptive FantasyKingdom means remain:

| Build | CPU+GPU W | Recorded FPS | Power change vs Dev-Mono | FPS change |
| --- | ---: | ---: | ---: | ---: |
| Dev-Mono | 11.728994 | 116.594667 | baseline | baseline |
| Mono | 11.296842 | 116.521000 | −3.6845% | −0.0632% |
| FB-R | 11.095211 | 116.641667 | −5.4036% | +0.0403% |
| FR-R | 11.124522 | 116.674000 | −5.1537% | +0.0680% |
| FR-M | 11.223126 | 116.663333 | −4.3130% | +0.0589% |

The favorable power differences coexist with tiny FPS differences in this game. NPSK grouping or a directional win does not itself establish a practically meaningful latency change. The extra `MonoBuild` folder's 80 rows have different means and unspecified lineage, so they remain excluded; the one-line `results_.csv` is an empty-field placeholder, and the unused 30-row/four-configuration time matrix is not a complete timing lineage. The input ZIPs contain 15,315 FPS records ending at 52.7713, 9,636 touch records ending at 179.9509, 3,644 Platformer records ending at 72.8, and 234 Roguelike records ending at 59.9313. These are recording extents, not validated benchmark windows. The missing source and four-game raw data prevent independent NPSK, GPEEQ or correlation reproduction.

## Design implications and limits

For B05/B06/B12, the useful result is conditional: production-oriented Unity settings often lower measured CPU+GPU power, but backend alone does not determine the outcome, and some build/game cells trade higher FPS for higher power or move in the opposite direction. A Nu comparison should predeclare engine/build mode, hardware, workload trajectory, observation window, service denominator and whether the estimand is average component power, whole-system joules, J/frame, latency, build energy or iteration time. Matched behavior and fixed time must be observed rather than inferred from an input trace.

FR-R is the strongest directional count in this sample, while Mono remains competitive in several power/J-frame groups. The paper's shorter-build-time rationale for Mono is plausible but unmeasured here; no compile durations or compile energy are reported. Results are bounded to five URP samples/microgames, one Unity version, one Apple platform and no DOTS/ECS workload. The authors themselves identify player representativeness, omitted settings, precompiled engine components, thermal behavior, URP-only scope and platform-specific measurement as threats (pp. 12–13).

The paper repeats S260's disputed 48%-lower headline and S261's older global estimates; those citations add no independent measurement here. Retain this runtime counterweight alongside S257/S259's development gains, S258's localization null/adverse outcomes and S260/S261's scene dependence. S265 does not measure Nu or any joint maintenance/runtime benefit.

The original 15-page article and all seven figures are now fully covered. Remaining gaps are the supplementary appendix, raw data for four projects, recorder/replayer/FPS-monitor and benchmark source, built executables, exact NPSK environment/settings and adjudication of the single Roguelike Dev-FB-D figure/count conflict. Those limits prevent full reproduction; they do not erase the favorable configuration effects or imply a Nu effect.
