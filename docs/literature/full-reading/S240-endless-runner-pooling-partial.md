# S240 — Object pooling in a small Unity endless runner: full journal reading

Aditya Cipta Rahadian, Iwan Setiawan and George Pri Hartawan, “Analisis Penerapan Metode Object Pooling pada Game 2D Endless Runner,” *Pixel: Jurnal Ilmiah Komputer Grafis* 15(2), 254–266 (2022), DOI [10.51903/pixel.v15i2.770](https://doi.org/10.51903/pixel.v15i2.770).

**Full-reading status, 2026-10-15 HKT.** This note supersedes its earlier indexed-text-only reconstruction. Native Zotero parent **`Y5VD4GHT` v5445** and attachment **`WX4AFBYI` v5512** were verified before reading; the parent remains in collection **`PKLXQNEE`**. The imported final journal PDF is 918,452 bytes, 13 pages, and SHA-256 **`1adcd87739f8a1ac2a7d016810d708a3dcb78d2a34d63d626af3a86c2d655627`**. Page 1 visibly identifies the title, three authors, journal volume/issue and printed pages 254–266. The PDF spells the third author’s given name “Geroge” on the title page; the native bibliographic record uses “George.”

All 13 PDF pages (printed 254–266) were read as text and visually inspected. Visual coverage includes Figures 1–21: the research and pooling flows; gameplay, templates and boundary diagrams; Unity hierarchy captures; both Unity Profiler captures; and both Task Manager captures. There are no numbered tables. The private coverage receipt and rendered-page inventory are under `.artifacts/s240-reading-20261015/`. This is a paper reading, not a reproduction, source-code inspection or verification of the reported runs.

## Study and implementation

The authors built two simple C#/Unity 2D endless-runner variants for PC/desktop and say they used the same game data (*data yang sama*) with different object-reinitialization methods (PDF pp. 3, 5; printed pp. 256, 258). The player runs automatically and can jump; play ends when the player falls. Three ground templates are selected randomly. Two boundary objects control the ground lifecycle: `AreaStartOff` marks the initial creation area and later destruction boundary, while `AreaEndOff` marks the end of the initially created ground and the boundary for creating another ground (PDF pp. 6–8; printed pp. 259–261, Figures 6–14).

The comparator repeatedly instantiates and destroys ground objects. The pooling variant adds an unavailable ground object to a collection, activates it, and deactivates it when unused so it can be reused (PDF pp. 4, 8–9; printed pp. 257, 261–262). Figure 3 is a conceptual flow attributed to an earlier online-game-server paper: request an object, take one from the list if available or create and add one otherwise, activate it, and return inactive objects for reuse. The journal supplies no C# code, pool class, prewarming rule, capacity bound, reset protocol or per-object state-clearing procedure.

Figures 16–17 are current Unity hierarchy snapshots, not creation counters. The instantiate/destroy hierarchy shows four clone entries; the text says that container ordinarily holds four to five grounds. The pool hierarchy shows seven named ground entries (templates 1, 2, 1, 1, 3, 3 and 2) at the captured moment. The figures therefore distinguish current hierarchy membership and the retention strategy, but establish neither how many entries were active nor how many objects had ever been created. They do not show that pooling reduced cumulative creation by a measured amount. They also illustrate the relevant tradeoff: a pool can retain more current objects even when its reported “used total” is lower.

The claim that the variants used the same data is not a demonstrated behavioral-equivalence control. The paper does not report matched random seeds or ground sequences, equivalent scores/durations, a common start-state reset, order counterbalancing, or trace comparison. Both displayed Task Manager captures show score 1084 and are the same embedded PDF image object (`373` on PDF pages 10 and 11), so they cannot establish matched executions.

## Measurement procedure and denominators

The authors report two months spent making and analysing the game (PDF p. 4 / printed p. 257). This is project duration, not separately measured construction time for each method. They inspect the in-editor variants with Unity Profiler and exported desktop executables with Windows Task Manager. Three laptop labels are named: Lenovo G41-35, Asus X441U in the narrative and conclusion (once written X411U in the result list), and Acer Z-14 (PDF pp. 10–12 / printed pp. 263–265).

No Unity version, scripting backend, operating-system version, processor/RAM specification, build configuration, profiler attachment configuration, sampling interval, warm-up, run duration, workload length, trial count, execution order, random seed or uncertainty is reported. There is no participant denominator. The subjective statement that pooling felt smoother and instantiate/destroy sometimes lagged is not assigned to named observers or a number of play sessions. The screenshots and listed device values are point observations without repeated-run distributions or inferential analysis.

The paper does not measure FPS, frame time, latency, garbage-collection pause duration, total execution time or throughput. “Performance” is operationalized mainly through memory snapshots, listed CPU percentages for two devices, and the informal play experience. The Unity Profiler screenshots contain allocation traces, including visible `GC Allocated` spikes in both variants, but have no readable time axis or aggregation and are not analysed as frequency, magnitude or pause measurements.

## Reported and visually supported results

The favorable direction reported by the paper is retained, but the visual audit exposes several important discrepancies.

| Observation | Instantiate/destroy | Object pooling | What the PDF supports |
| --- | ---: | ---: | --- |
| Unity Profiler `Used Total` | 314.9 MB | 307.5 MB | Figures 18 and 20 show these values: a 7.4 MB (about 2.35%) difference. Section 4.6 rounds/describes it as 10 MB lower. |
| Unity Profiler `Reserved Total` | 0.50 GB | 0.50 GB | Both screenshots show 0.50 GB and Unity 485.7 MB. The prose’s “485 MB” for pooling is the Unity component, not a distinct lower reserved-total reading. |
| Unity Profiler `Total System Memory Usage` | 0.94 GB | 0.93 GB | Both screenshots show the separately labelled rounded values. They must not be added to `Used Total` or `Reserved Total`. |
| Unity Profiler loaded-resource details | 219 textures / 6.9 MB; 17 meshes / 448.0 KB; 19 materials / 27.0 KB | 223 textures / 7.4 MB; 22 meshes / 0.8 MB; 28 materials / 46.0 KB | Figures 18 and 20 show higher counts/amounts for these displayed pooled categories despite lower `Used Total`; the paper does not discuss this adverse detail. |
| Lenovo Task Manager memory, prose | 109.3 MB | 104.5 MB | The narrative reports a favorable 4.8 MB difference. However, Figures 19 and 21 both visibly show the `2D Endless Runner` row at 109.3 MB and 2.5% CPU, with the same score 1084. They reuse the same embedded PDF image object (`373`), so the pooled screenshot does not visually substantiate 104.5 MB. |
| Asus, listed values | CPU 4.9%; memory 106.6 MB | CPU 3.9%; memory 105.5 MB | Text only: favorable differences of 1.0 percentage point CPU and 1.1 MB memory. No screenshot, repetition or uncertainty. The model is inconsistently written X411U/X441U. |
| Acer Z-14, listed values | CPU 7.4%; memory 64.6 MB | CPU 6.5%; memory 63.4 MB | Text only: favorable differences of 0.9 percentage point CPU and 1.2 MB memory. No screenshot, repetition or uncertainty. |

The two Profiler captures also differ in subcomponents: Unity 297.7→290.2 MB, Mono 9.7→9.4 MB, GfxDriver 4.1→4.5 MB and Profiler 1.8→1.9 MB. These are single displayed states, not independently sampled component effects. The paper’s wording *apabila ditotalkan* (“when totalled”) should not be read as a valid sum of overlapping Profiler categories: the screenshots themselves separately label used, reserved and total-system values.

The authors conclude that pooling reduces memory burden and makes play smoother, while repeated destruction sometimes causes a little lag when new ground is created (PDF p. 12 / printed p. 265). Those are the study’s favorable conclusions. The much larger device-specific percentage improvements quoted on pp. 2–3 belong to Pekonen’s separate HTML5 thesis cited as background, not to this Unity experiment.

## Evidence disposition and design implications

S240 supplies a concrete, direct pooling-versus-instantiation example for a narrowly scoped ground-recycling loop. It supports the mechanism claim that the implemented pool retained hierarchy objects for deactivate/reactivate reuse, and it reports modest favorable memory/CPU observations. The hierarchy and Profiler visuals add an adverse but useful qualification: pooling retained more current ground entries and displayed higher counts for several loaded-resource categories. “Total objects ever created,” “objects currently live/in the hierarchy,” “objects active,” and “memory used” are distinct outcomes and must be measured separately in any future comparison.

For a defensible comparator, record a matched generated-ground trace, total instantiations and destructions, active and pooled counts over time, peak and steady-state memory, allocations and GC pauses, frame-time/FPS distributions, warm-up and sampling windows, repetitions and device/build configuration. Pool setup, reset logic, integration and retained-capacity costs also belong in total work. A source or instrumentation check is needed to establish whether recycled objects are fully reset.

The paper does not establish a causal memory or performance effect beyond these uncontrolled snapshots; it does not measure programmer productivity, implementation effort by arm, correctness, maintenance, agent assistance, or Nu. It cannot support a general Nu cost/benefit claim, GC-tail claim, mobile result, or conclusion about pooling arbitrary entity types. Its practical application is limited to one small Unity desktop endless runner’s generated-ground lifecycle, with unknown run denominators and a visually contradicted Lenovo pooled-memory value.
