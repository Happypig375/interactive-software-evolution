# S265 — Unity build configuration: power, frames and artifact correspondence

José Miguel Aragón-Jurado, Ruck Thawonmas, Patricia Ruiz and Bernabé Dorronsoro, *Native code, greener games? Investigating energy efficiency in unity builds*, Entertainment Computing57,101132, May2026; online30April2026. [DOI10.1016/j.entcom.2026.101132](https://doi.org/10.1016/j.entcom.2026.101132). Main-agent reconstruction,2026-10-04. **Partial publication coverage:** all2,861 indexed primary lines73–2933, with15-page pagination, four tables and79 references, are read. Original PDF, seven main figures and supplementary appendices remain unavailable. Four separate repository chart PNGs are visually read. No engine, compiler, benchmark or author analysis code is executed.

## Identity and preserved material

Native parent **`DMZN5HBS`5698** and note **`E3BAC292`5699** were created after DOI/title duplicate checks and before selected body reading. Collection`PKLXQNEE` membership is preserved. The author-uploaded ResearchGate text carries the final DOI/pagination and CC BY4.0 notice; Crossref agrees on authors/publication. Submission/revision/acceptance dates are16November2025/12March2026/22April2026. Bytewise final-PDF correspondence is unverified.

| Native attachment | Exact identity |
| --- | --- |
| Indexed text **`XLR9VRH5`5705** |117,303bytes, UTF-8 text/plain; SHA-256`ff14cfb16ba72ab7f997a1f75ff1d6c451e18af03629afc297d0edad688a51f5`; MD5`c08e11b4da15a0b60309dd36b48ea930`. Labeled indexed primary text, not original PDF/HTML. All primary line numbers merge without gaps/conflicts. |
| Selected artifact **`ZJQTP8T4`5707** |724,897bytes; SHA-256`9e9917d3617c766e55f72a7e1ef64bfe8d82a719747223edf9a4db504b40cc38`; MD5`356ec55dd3e3609a71d3c4b885de4b14`. Locally assembled46-file selection plus provenance, not an author release or complete repository. |

Publisher and Crossref-linked Elsevier XML requests return403. The ResearchGate PDF link resolves with a duplicated path and fails404; a transparently normalized public-path candidate fails through the web interface and returns403 by ordinary HTTP. A GPEEQ figure click fails. The UCA record links the DOI, not a deposited PDF. Scite returns no full text, and its incoming graph has zero edges/low coverage; neither result establishes absence. Supplementary frequency/correlation appendices are still unacquired.

## Reported design and outcomes

The paper compares14 configurations across five Unity samples, with30 runs per cell: Mono/development and IL2CPP's Faster Build/Faster Runtime × Debug/Release/Master × development setting. It uses Unity6000.0.45f1, macOS15.5 and an M3 Pro, fixed-duration input replay, powermetrics and an FPS-monitor object. Warmup, restarts and thermal preconditioning are described. A30-run monitor-overhead check reports under1.75% power difference without significance; that is not an equivalence bound.

GPEEQ compares power and frame-rate ratios against development Mono. NPSK95% groups drive classifications; same-group membership is called equivalent, although failure to distinguish is not an equivalence test. Production settings generally fare better, with workload-dependent exceptions. Table4's best energy/frame groups differ: FR-M for BossRoom, FB-M for FPSGame/Platformer, and several alternatives including Mono for FantasyKingdom/Roguelike. Spearman relationships vary in sign and are explicitly exploratory. Build-time savings are discussed, not measured lifecycle outcomes. The paper repeats S260's disputed48%-lower headline and S261's older global estimates; these repetitions add no independent evidence.

## Public artifact and selected source contract

The [public repository](https://github.com/josemiguel-aragon/unity-energy-benchmark/tree/7498de8ea2a1cb3f633eff1da8b39e470af72fe1) is pinned at **`7498de8ea2a1cb3f633eff1da8b39e470af72fe1`**,11August2025, message *Final scripts*. Repository pushed-at metadata is30April2026; it is not the commit date or proof of correspondence to the revised paper. The recursive tree contains426 entries and is not truncated. Selected original files have verified Git-blob hashes, sizes and SHA256. Coverage comprises README/ignore, four complete measurement/analysis scripts, five editor-version and five package manifests,24 CSVs, two recording ZIP inventories/bounded contents and four original charts. Large Project Auditor JSONs, other project settings and package utility bodies remain unselected.

All five editor-version files agree on6000.0.45f1 (`d91bd3d4e081`), and all manifests declare URP17.0.4. BossRoom also declares ParrelSync and VContainer; a blanket official-packages-only description is too broad for this pin. This does not establish custom native plugins, altered shipped runtime code or execution of those dependencies.

The `.gitignore` excludes Assets and those project directories are absent from the tree. The recording ZIPs contain inputs, not the recorder/replayer or FPS-monitor implementation. Consequently, exact replay scheduling, elapsed-time versus per-frame averaging, state/trajectory equivalence and the shipped executable are not reconstructed. A timestamped input list alone cannot validate those properties.

| Inspected file | Static contract and limit |
| --- | --- |
| `scripts/measureECMacos.sh` | Runs powermetrics around the executable, averages matching CPU/GPU power samples, records elapsed time/memory and reads an externally written FPS file. No sample-time integration, wall-plug measurement, per-process isolation or compilation-energy measurement appears. The literal option is`-i 1`; the comment/README describe one-second sampling, whose actual interpretation is not verified here. Missing CPU samples become zero; GPU/FPS become NA. No observed missing run is inferred from these paths. |
| `scripts/plot_compare_boxplots.py` | Divides milliwatts by1000 and drops NA rows. Its expected Mono filenames add`-Build`, unlike the selected raw files; CPU dataframe reuse and exported names differ from the supplied14-column matrix. This source is not certified as the exact generator of the published tables. |
| `FantasyKingdom-bench/IL2CPP-Build/NPSKClustering.r` | Reads the four supplied matrices and calls`sk_esd(model_performance)` for each, without explicit mode/version/direction arguments. No inferential package is installed or run; the described statistical configuration and groups are not independently reproduced. |
| `scripts/plot_frameup-powerup.py` | Four literal5×13 sign tables drive the count plots. These are classifications supplied by the authors, not regenerated statistical tests. Passive parsing and the four PNGs agree on all52 configuration/count bars. |

## What the released numbers corroborate

Fourteen FantasyKingdom result files contain **420 complete finite10-field rows**, with30 per configuration and no duplicate row within a file. The four30×14 analysis matrices match **1,680 derived cells**: CPU/GPU milliwatts converted to watts, recorded FPS unchanged and total power equal to CPU+GPU. Maximum floating-point difference is3.56×10⁻¹⁵; this verifies data correspondence, not instrumentation or significance. No corresponding raw result CSVs for the other four games occur in the pinned tree.

The following are our descriptive means from those released rows, without new hypothesis tests:

| FantasyKingdom build | CPU+GPU W | Recorded FPS | Power change from development Mono | FPS change |
| --- | ---: | ---: | ---: | ---: |
| Development Mono |11.728994|116.594667|baseline|baseline|
| Mono |11.296842|116.521000|−3.6845%|−0.0632%|
| Faster Build, Release |11.095211|116.641667|−5.4036%|+0.0403%|
| Faster Runtime, Release |11.124522|116.674000|−5.1537%|+0.0680%|
| Faster Runtime, Master |11.223126|116.663333|−4.3130%|+0.0589%|

The favorable power differences coexist with very small FPS differences in this game. A significant group or a win count does not itself establish a meaningful latency improvement. These are run-level recorded FPS means; without the monitor source, dividing power by them does not certify total joules divided by delivered frames. Fixed gameplay duration, equal useful service and equal frame count are different comparisons.

The literal sign tables reproduce34 lower-power alternatives among65:27also increase FPS, six decrease it and one has no detected FPS difference. **Forty-five** alternatives increase FPS:27with lower power, seven with no detected power difference and11with higher power. The paper's indexed lines1933–1935 instead report46 and15.22% without a power difference; the pinned artifact gives7/45=15.56%. Our earlier claim that the artifact corroborated46 was incorrect and is corrected on2026-10-05. The13 FPS bars sum to45, independently agreeing with the65-cell classification count. Paper/release correspondence remains unresolved; this check does not identify which paper cell, if any, differs. One alternative sits at the unchanged center. FR-R alone has favorable power and FPS signs for all five games; FB-R has five power improvements but four FPS improvements. These counts preserve the positive configuration result while bounding the broader prose about reliable combined gains. They are not65 independent games or a pooled effect size.

The separately stored `MonoBuild` folder contains another80 rows (30/30/10/10) with materially different power/FPS means. They are not pooled into the420-row analysis or treated as additional independent replications; experimental lineage is unspecified. The one-line `results_.csv` is an empty-field placeholder, not a valid run. The unused time matrix has30 rows/four configuration columns plus an index; it does not establish a complete timing-analysis lineage.

The root recording ZIP contains FPS/touch logs; the scripts ZIP adds platformer/roguelike logs. The two shared files are byte-identical across ZIPs. Bounded endpoint/schema inspection finds15,315 FPS records ending52.7713,9,636 touch records ending179.9509,3,644 platformer records ending72.8 and234 roguelike records ending59.9313. These timestamps are input-log extents, not verified benchmark durations or proof of truncated execution. The data/source selection is explicitly narrower than reproduction.

## Consequence for Nu and continuation

For B05/B06/B12, configuration and workload can materially change measured cost even within one engine/language. A valid Nu comparison must state production/development settings, work boundary and service target. CPU+GPU power, whole-device energy, energy/frame, latency and developer iteration time require distinct observations. Retain this useful runtime counterweight alongside S257/S259's development gains, S258's localization null/adverse outcomes and S260/S261's scene dependence. None of these readings measures Nu's joint maintenance/runtime benefit.

Primary figures/supplement, four-game raw data, benchmark source and exact statistical/edition provenance remain concrete coverage gaps. They do not establish a failed study or absence of a Nu effect. Resume obtainable original figures/supplement or a fuller author release when consequential, reusing this pin and native holdings. The broader practical-change frontier,2026 postmortem extension, temporal obligations and type evolution remain open. No full-paper increment or experiment follows.
