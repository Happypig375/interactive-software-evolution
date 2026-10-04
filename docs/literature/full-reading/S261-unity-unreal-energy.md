# S261 — Unity/Unreal energy: scene dependence and edition lineage

**Primary author edition fully read 2026-10-04 HKT by the main Codex AI session.** Carlos Pérez, Javier Verón, Francisca Pérez, María Ángeles Moraga, Coral Calero and Carlos Cetina, *Towards Green Game Software Engineering: A Comparative Analysis of Energy Consumption Between the Widespread Unity and Unreal Video Game Engines*, Information and Software Technology 191 (March 2026), article 107991, [DOI 10.1016/j.infsof.2025.107991](https://doi.org/10.1016/j.infsof.2025.107991). The earlier arXiv edition belongs to the same empirical lineage. This is an engine/scene comparison, separate from S260's Blueprint/C++ comparison.

## Identity, acquisition and actual coverage

Crossref confirms the journal, six authors, volume and issue date. The [author page](https://svit.usj.es/research/paper/towards-green-game-software-engineering-a-comparative-analysis-of-energy-consumption-between-the-widespread-unity-and-unreal-video-game-engines) dates the work 3 December 2025. Its [current PDF](https://svit.usj.es/api/media/file/CPerez_IST_2026_PRE.pdf) has **15 pages**, a preprint footer and creation/modification date **18 February 2026**. These dates describe different objects; publisher-final byte correspondence is unverified. The publisher route failed, and its direct ScienceDirect page returned 403.

All 15 current pages, **11 figures, 10 tables and 37 references** were read. All pages were visually inspected in contact sheets, with enlarged pp.9–14 for tables, plots and the conclusion. This edition has no appendix. The [earlier arXiv v3 PDF](https://arxiv.org/pdf/2402.06346v3), *A Comparative Analysis of Energy Consumption Between the Widespread Unity and Unreal Video Game Engines*, has 14 pages; the repository dates v3 to 23 May 2024, while PDF metadata says 24 May. Its **pp.1,4–9,11–13 were read as text** and **pp.1,4–13 visually inspected**, including enlarged p.10. Pages 2–3 and 14 remain unread. The earlier edition is a partial lineage check, not another complete reading or independent study. The [SSRN record](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5372202), DOI 10.2139/ssrn.5372202, advertises the current title/authors, 15 pages and posting 30 July 2025; its body returned 403 and is not byte-verified against either acquired PDF.

Before selected reading, collection `PKLXQNEE` contained 286 parents; DOI/title/arXiv/SSRN library checks found no matching record. Native Zotero parent **`Q4D5CXH3`**, note **`FEDAPHFB`** and both PDF attachments preserve one work with explicit editions:

| Attachment | Bytes | SHA-256 | MD5 |
| --- | --- | --- | --- |
| Current author PDF `LTZWS75H` | 5,359,575 | `be48432ba451d55feddba0a5040c50e42590057e9b0a2dc91737732e67dd0b0a` | `dd88e56ce2ab31fbca1786e5df3d42e7` |
| arXiv v3 `C6GEWTQX` | 5,700,449 | `0b5e11d0826f993b60cbc657d3247ce39ae04824eb14cf652f0dab1a6058a7e3` | `187f96b796d73ee8ebd63c4de0ee5035` |

Native attachment bytes were read back and verified; final object versions are recorded in the search ledger. No GUI or JavaScript-window workaround was used.

**Artifact coverage is metadata only.** The current paper cites concept DOI `10.5281/zenodo.16313729`; the author's link resolves to [version record 16313730](https://zenodo.org/records/16313730), published 22 July 2025 and displayed as modified 28 September 2025. All 172 indexed lines were read. The page describes six Windows 10+ builds for Unity 2022.3.6f1 and Unreal 5.2.1:

| Declared ZIP | Displayed size | Declared MD5, not independently verified |
| --- | --- | --- |
| Unity_01_Physics.zip | 26.2 MB | `66350c7ebceb6077eb936116320e5c2d` |
| Unity_02_StaticMesh.zip | 30.8 MB | `858ec67793fcf64f48ddadea14f0bdb6` |
| Unity_03_DynamicMesh.zip | 30.8 MB | `d57c2906b51c856c712512f1d85e6b86` |
| Unreal-Engine_01_Physics.zip | 397.1 MB | `e14824e766d2c96472402ab07613e893` |
| Unreal-Engine_02_StaticMesh.zip | 785.0 MB | `f4ba9de55d185916c178e0c279847a8c` |
| Unreal-Engine_03_DynamicMesh.zip | 225.2 MB | `038a66b3986bf1dfbd7be5964d00fac5` |

No ZIP, internal directory, project, script or measurement series was acquired. The public API and a direct Unity Physics file HEAD request returned 403; the preview failed through the web tool. The older paper's [author artifact route](https://svit.usj.es/unreal-vs-unity-energy-comparative-analysis/) timed out in the web tool and returned 403 by an ordinary request. The blank displayed license field does not establish that no license exists. Nor does the six-build description establish that raw data or source are absent inside the archives. Restored lawful access would enable a passive inventory and checks of inclusion, baseline calculation, sampling and configuration; executing the builds remains outside this assignment.

## What the comparison actually holds constant

The paper compares **Unity 2022.3.6f1** with **Unreal 5.2.1**, implemented respectively through C# `MonoBehaviour` and a combination of Blueprint/C++ `APawn`. The second author, described as an experienced game developer, implements both; two external industry professionals validate their equivalence. That is useful domain review, not an independent replication or an executable equivalence proof.

Each scene uses 1,000 objects, a camera, a generator and a directional light, with largely default engine settings and adjustments for visually similar light intensity. Static scenes render meshes/textures. Dynamic scenes add a Mixamo stabbing animation. Physics scenes use one-metre, 50 kg cubes with collisions and random forces of 1–80 N applied **each frame** toward the origin. Equal object counts/assets do not by themselves verify equal rendered quality, simulated trajectories, physics steps or completed work. In particular, per-frame forcing can couple the workload to frame frequency; matching caps, fixed steps, seeds and trajectories are not reconstructed.

FEETINGS supplies the GSMP procedure, EET hardware measurement and ELLIOT processing. The reported DUT is an i7-10700, RTX3060 12 GB, Asus B460 board, four 32 GB DDR4 modules, Kingston A400 480 GB storage and Windows 11 Pro; a 27-inch 2K monitor is listed. Measurement samples power at **100 Hz for 60 seconds** per execution, with a pre-launch baseline subtracted. Those equal durations make mean power and integrated energy proportional **within the declared measurement boundary**; they do not establish equal useful service.

Order V1 executes Unreal dynamic→static→physics, then Unity dynamic→static→physics; V2 reverses that sequence. Both sequences are said to be repeated 30 times, but Table 2 provides only 30 total slots per engine/scene. The relationship between those slots, order groups and pooling is unresolved. Do not infer an exact 360-run dataset from the prose or treat Table 2 as a resolved order-specific census.

| Scene | Unity invalid / retained | Unreal invalid / retained |
| --- | --- | --- |
| Dynamic | 4 / 26 | 7 / 23 |
| Static | 5 / 25 | 9 / 21 |
| Physics | 4 / 26 | 9 / 21 |

Thus **38 of 180 tabulated slots are excluded and 142 retained**. Wrong executions/outliers are described through inconsistency or extreme consumption, without numerical thresholds or excluded identities. These counts are more informative than S260's unreported inclusion counts, but outcome-based removal remains part of the observed analysis. Samples and repeated runs on one DUT are not independent games or hardware cases.

The current edition reports Mann–Whitney order comparisons: Unity static p=.869, dynamic p=.091, physics p=.109; all Unreal cases p<.001, with order differences described as 1–3%. Engine comparisons are reported as p<.001 for each scene. Preserve those inferential claims at their stated scope; non-significant Unity order tests do not prove absence of an order effect. Raw observations, group allocation, U statistics and uncertainty intervals were not acquired, so this reading does not reproduce the tests or establish that exclusions/configurations are causally innocuous.

## Retain the scene-dependent result with the correct denominator

Tables 6–8 report the following mean DUT power after the stated baseline subtraction. The relative comparisons and 60-second conversion below are this reading's arithmetic on printed aggregates, not repaired measurements:

| Scene | Unity / Unreal (W) | Unreal relative to Unity | Unity relative to Unreal | Conditional Unity / Unreal energy over 60 s (J) |
| --- | --- | --- | --- | --- |
| Static | 269.78 / 315.11 | 16.80% higher | 14.39% lower | 16,186.8 / 18,906.6 |
| Dynamic | 296.59 / 218.74 | 26.25% lower | 35.59% higher | 17,795.4 / 13,124.4 |
| Physics | 67.92 / 306.17 | 350.78% higher | 77.82% lower | 4,075.2 / 18,370.2 |

The preferred engine changes with the selected scene. That result is useful counterevidence to a universal ranking. The physics ratio is approximately **4.51× Unreal/Unity**; Unity cannot consume “351% less” than Unreal. The current p.14 conclusion, also present in the inspected older conclusion, swaps the 17% and 26% scene labels. Tables 6–8 preserve the interpretable pairing. The same denominator reversal affects the smaller HDD physics comparison.

Three reporting limits prevent promoting the table ratios into independently verified equal-service energy savings:

1. **Baseline presentation:** Tables 3–5 label their means “without baseline.” Static and physics DUT means exceed the corresponding Tables 6/8 values by about **107.4 W** in both engines. Dynamic Table 4 means instead equal Table 7 exactly, while its DUT medians are 327.57/404.98 W rather than the means 218.74/296.59 W (Unreal/Unity). Component differences show a similar mixed pattern. This suggests inconsistent presentation, but does not identify which raw values or processing step should be corrected.
2. **Plot identity:** current Figure 6 is captioned Dynamic Mesh, yet its graph labels say Unreal/Unity **Physics**, with the same physics-like ranges as Figure 8. The two embedded images have different hashes/dimensions; no byte-identical-image claim is made. Earlier p.10 Figure 8 does display Dynamic Mesh labels and different ranges. Current Figure 6 therefore cannot verify the dynamic distribution. Older dynamic and current static plots also require care about their apparent pre-baseline observation boundary.
3. **Service and transfer:** no frame-rate, frame-tail, image-quality or physics-work equality was measured here. Professional validation supports scene plausibility; instrument validation does not prove that relative engine effects are invariant across hardware or real games. This neither negates the observed ordering nor supplies Nu's runtime result.

## One empirical lineage; a changed global illustration

Passive comparison of the printed editions finds **192 identical numerical cells**: 12 counts in Table 2, 120 descriptive values in Tables 3–5, 36 outcomes in Tables 6–8 and 24 model values in Tables 9–10. The newer edition adds statistical-test reporting and changes surrounding material; the older inspected methods/results do not report those Mann–Whitney tests. Identical outcomes and the common setup warrant treating this as **one empirical lineage**, not two replications. This is not proof that every underlying file or textual claim is identical.

The hypothetical optimum combines the lowest scene-specific values from different engines. Equal weighting of the three scenes gives Unity 211.4 W, Unreal 280.0 W and the constructed optimum 185.5 W. Table 10 uses developer market shares .38/.15/.47 for Unity/Unreal/others and imputes other engines as their mean, 245.7 W. The resulting weighted 237.8 W versus 185.5 W gives about **22.02%**. This is an arithmetic construction, not an implemented hybrid engine, measured integration or representative workload distribution.

The older discussion applies that fraction to a 230–347 TWh gaming illustration, yielding 51–76 TWh and at least 13 million household-equivalents. The current version instead uses a **historical 2012 gaming-PC estimate of 75 TWh**, attributed to Mills and Mills (2016), to illustrate **16.5 TWh / 4.23 million households**. The same scene measurements therefore support different external illustrations. The underlying Mills paper was not read here, and neither illustration is credited as a current worldwide saving estimate. Developer shares are not runtime-hour shares; scene weights, other-engine imputation, full-system versus incremental power, hardware and equal-service transfer all remain assumptions. Changing the external total or correcting a percentage does not validate them.

Current reference 21 repeats S260's “48% lower” headline. That is citation uptake, not an independent confirmation; reuse S260's own denominator/unit reconstruction. Conversely, the present study's explicit equal-duration design and excluded-run counts improve the available account relative to S260. Preserve that methodological information alongside the remaining limits.

## Consequence for Nu and the next gap

Together, S257/S259 show scoped development-task advantages for the studied visual workflows; S258 shows activity-dependent localization outcomes; S260/S261 show that runtime outcomes depend on workload and the denominator. They do not measure a joint lifecycle benefit or establish a general ordering of languages, paradigms or engines. For Nu, trace an architectural mechanism to a concrete completed change and runtime service obligation, retaining both benefits and costs. A small source or diagnostic count is not that outcome.

The immediate method question now shifts to **version-specific Blueprint compiler/debugger contracts**: what is transformed, what compile-time validation checks, how instances are reinstanced and what debugging exposes. That can distinguish a documented mechanism from S260's compiler intuition and S257/S259's participant reports without executing a compiler. The independent Unity-build study remains a consequential conditional runtime check; it does not require extending this branch before every tool/practice/temporal gap. Phylogenix, generative assets, contemporary practice, postmortem continuation and live state/type evolution remain open. No build, benchmark, author script, statistical fit or candidate experiment was executed or authorized.
