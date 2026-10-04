# S255 — Product lines versus Clone and Own in game-content tasks

Jorge Chueca, Jose Ignacio Trasobares, África Domingo, Lorena Arcega, Carlos Cetina and Jaime Font, *Comparing software product lines and Clone and Own for game software engineering under two paradigms: Model-driven development and code-driven development*, Journal of Systems and Software205 (November2023),111824, [DOI10.1016/j.jss.2023.111824](https://doi.org/10.1016/j.jss.2023.111824). Main-agent reconstruction,2026-10-04. All1,542 indexed lines of the [19-page author preprint](https://svit.usj.es/Chueca_JSS_2023_PRE), dated3November2023, are read, including eight tables, seven figure captions/available labels and54 references. Main PDF bytes, main-page visuals and final-edition correspondence remain unavailable. **No full-publication credit.**

The comparison supplies positive evidence for prepared product-line configurations on constrained game-content tasks. It also supplies an efficiency null under model-driven development and participant concerns about lost detail/control. Its released materials establish that the tasks use handwritten code, diagrams or feature selections, with rubric-based scores. The observed benefit is therefore task performance with supplied representations; total setup, executable integration, retained behavior and lifecycle maintenance are separate questions.

## Identity, lineage and native holdings

Collection`PKLXQNEE` contained280 parents before selection. Collection DOI/title checks and library DOI/Chueca queries found no matching parent. Native parent **`L4LBKPLM`5571** and note **`7CCASKMN`5572** were created before selected reading. Parent identity, membership, existing note and attachment versions were checked during attachment, and stored bytes match:

| Attachment | Identity |
| --- | --- |
| Indexed text **`R5EAQG7D`5574**, `text/plain` |112,086bytes; SHA-256 `c6f4610fe137bb517a5723de3baab3290e91ed0b189e5128b5d0e6f482841a2a`. Indexed lines0–1541 have no gaps or conflicting duplicates. This identifies assembled indexed text, not a PDF. |
| [Replication package14674600](https://zenodo.org/records/14674600), RAR **`MVSE6JXB`5576** |191,138,796bytes; SHA-256 `66e7eb978244ea616a51250138e04688e104e629fe1a0fb578d5f53db47af938`; MD5 `293c9ce6bc770c4cd107d0aff4cb3ba6`, matching Zenodo. Metadata publication date11November2023, record created16January2025; concept14674599, version14674600; `isSupplementTo` binds the journal DOI. |

The institutional repository bitstream, old WordPress PDF and current author-site media link each return403 through ordinary requests. Web access supplies the old preprint index; its screenshot and current media fetch fail. Scite SC173 (`limit:20`, offset0,1/1) supplies metadata, `contentDenied:true` and an institutional locator, without abstract, excerpts or outgoing citation contexts. Its eight citing publications and zero classified statements are not a verdict or an inspected citation graph. No institutional entitlement is assumed and no purchase/contact occurs.

The paper explicitly extends [Trasobares etal2022, DOI10.1145/3546932.3546998](https://doi.org/10.1145/3546932.3546998): its28-person MDD experiment is reused here, while the journal adds a51-slot CDD experiment and combined analysis. The predecessor body/edition has not yet been read. Do not count its28 people again as a replication. Moreover, ten of51 CDD form responses acknowledge an earlier Kromaia boss-modeling experiment; this does not identify which experiment or establish how many people overlap with MDD. The paper's “new subjects” wording does not resolve that linkage.

## Treatments, assignment and actual task boundary

Both experiments use Kromaia, a commercial game built on a proprietary C++ engine with Ogre/Bullet dependencies. SDML models specify bosses and are interpreted into runtime objects; a C++ API also creates bosses. That architecture is context for the experiment, not a runtime whose correctness or performance was reproduced here.

| Context | Clone and Own comparator | Supplied product-line treatment |
| --- | --- | --- |
| MDD | Reuse/edit existing SDML boss models; submit the complete graphical model. | Choose model fragments for named variation points using a compositional product line. The task sheet explicitly accepts assignments such as a feature for each hole and says a complete drawing is unnecessary. |
| CDD | Reuse an example boss function and documented C++ API calls; submit handwritten code. | Select features from a prepared constrained tree and its documentation/examples. The paper describes an annotative C++ generator behind the feature model; submitted selections do not demonstrate that participants extended or tested that generator. |

The CDD materials expose a consequential difference in granularity. API calls request exact counts, while product-line choices include low/medium/high quantities and small/medium/big size categories. Feature constraints and an overview of available options also provide information that participants say was harder to recover from the API documentation. This is a useful prepared-system comparison, with bundled representation, granularity, documentation and derivation support. It does not isolate one syntactic convention or establish equal expressive scope for arbitrary successor changes.

Each participant performs two tasks: reconstruct Argos, then Teuthus, from gameplay videos. Random assignment counterbalances reuse-approach order between two groups; task order remains fixed. Each paradigm has one professional online session and one student in-person session. MDD comprises13 professionals/15 students; CDD13/38. Paradigm is a between-cohort comparison, with different composition and different product-line implementations; professional status also accompanies session setting. Two separate two-person pilots are reported, outside the main experiments.

The paper schedules roughly30minutes per task inside a105-minute session. Training, form access, consent, demographics and focus groups sit outside task-time scores. Instructions request start/end clock times and scanned/photographed handwritten solutions. The CDD training slide24 and task sheets confirm this directly; MDD sheets distinguish complete drawings from variation-point selections. The released time values include tasks exceeding30minutes, so the schedule is not evidence of a uniformly enforced stopping cap.

Correctness is a0–100 correction-template score. Efficiency divides that score by elapsed minutes; it is not simply reciprocal completion time. Satisfaction comprises perceived ease of use, perceived usefulness and intention to use, derived from16 agreement items. The source reports templates designed by a researcher and game engineer, but the inspected inventory supplies no standalone item-level correction rubric or adjudication record. Released total scores and photographed submissions do not by themselves establish executable or temporal correctness.

## Results retained at their actual denominators

Own passive parsing of the original XLSX files checks102 CDD task rows and56 MDD rows, with both methods represented for every recorded within-cohort ID. No missing value is imputed and no participant is removed based on performance. CDD correctness/efficiency are absent for subject23/task1/CaO and subject47/task2/SPL; thus each method has50 values for these outcomes, while time and satisfaction each have51. MDD has28 per method for all outcomes. These are recorded-data denominators, not a reconstruction of recruitment attrition or missingness causes.

| Outcome, CaO → SPL | CDD | MDD | Published selected-model result |
| --- | --- | --- | --- |
| Correctness, points/100 |53.867 →69.777; +15.910points, +29.54% relative |51.875 →64.132; +12.257points, +23.63% relative |CDD p<.001; MDD p=.028, favorable to SPL in both. |
| Efficiency, points/minute |2.582 →3.903; +51.15% relative |3.415 →3.293; −3.56% relative |CDD p<.001; MDD p=.678. Preserve the latter as inconclusive, not equivalence. |
| Mean task minutes |21.647 →19.686; −9.06% |18.429 →20.679; +12.21% |Descriptive time comparison; the51% efficiency headline is not51% less time. |
| Ease of use,1–5 |3.565 →4.069 |3.542 →3.786 |CDD p<.001; MDD p=.192. |
| Usefulness,1–5 |3.561 →3.993 |3.799 →3.701 |CDD p=.001; MDD p=.684. |
| Intention to use,1–5 |3.216 →3.647 |3.304 →3.268 |CDD p=.030; MDD p=.993. |

These raw-workbook means recover the published substantive patterns, allowing small reporting-rounding/truncation differences. Every available efficiency cell equals its stored correctness/time ratio. The package's13.21% CDD satisfaction headline is an arithmetic average of the three relative mean changes; it is not a13-percentage-point improvement or an extra independent outcome. MDD SPL correctness ranges from0 to100; these adverse/low observations remain included.

The authors fit repeated-measures linear mixed models, inspect residual normality and compare alternative fixed-factor models with AIC/BIC. CDD efficiency uses a square-root transform and ease of use a square transform. Multiple outcomes, model selection and cohort/setting differences constrain inferential transfer. An independent analyst or95% confidence level does not itself establish adequate power or eliminate selection/multiplicity issues. No model fit is rerun here.

Two important qualifications survive comparison with the released `Summary-DESCRIPTIVES-TEST-COHEN.xlsx`:

- **Correctness interaction:** indexed Table6 and workbook `Hip-Test-results-ALL!C9` both give approach×paradigm F=.577, p=.45. Sections4.2.1/4.2.4 instead describe a significant correctness interaction. Preserve the within-paradigm positive effects, but do not adopt that claimed interaction. Efficiency's interaction p=.001 and usefulness's p=.023 remain the reported results.
- **Prior-experiment field:** original CDD responses contain41 “no” and10 “yes” answers. The derived `DATA4SPSS` prior-experiment column is uniformly2; its first formula references the method cell rather than the original yes/no answer. This makes that derived field unsuitable for establishing exposure history. It does not show that the published professional-experience factor, which has a separate column, is uniformly wrong.

The full SPSS `.sav`/`.spv` files are inventoried but not decoded or executed. Therefore this is a descriptive-data and reported-table check, not reproduction of the selected fits or a reconstruction of their full analysis history.

## Materials and qualitative evidence

The package has246 files:31PDFs,2PPTX,6XLSX,150 standalone images,34SPV and23SAV. Full inventories and hashes remain in ignored local artifacts; bodies, response dumps and private transcripts are not committed. The158 named participant task files are inventoried, not individually rescored or visually read.

Actual selected material coverage is recorded precisely: all59 extracted training-slide pages (CDD24/MDD35); six one-page CDD API/feature/example PDFs; all17 pages of the released focus-group notes; page2 of each focus-group question deck; CDD CaO-first form pp7–16/36–38 and SPL-first p9; MDD SDML-first pp5–7/12–13 and SPL-first pp5–6/12. Twenty-seven selected page visuals are inspected in seven contact sheets, including all six one-page mechanism PDFs, CDD training6/10/15/17/23/24, task pages and MDD syntax/composition diagrams. The one-page participant-information sheet is visually read. Form page24 is visually blank except its header/footer; other uninspected pages are not claimed read. Main-paper visuals, all task-video content, the complete response corpus and full material visuals remain outside this coverage.

Workbook coverage includes both per-task analysis inputs, the CDD original-form prior-exposure column, four selected summary sheets (`%DE MEJORA` and all three hypothesis-result sheets), and metadata/header screening of the other sheets. Cached numeric cells and formulas are read from OOXML; author formulas/code are not executed. The six ethics PDFs, duplicate PPTX files and remaining output files are inventory-only.

The focus notes preserve real favorable mechanisms: a feature overview can reveal available parts and constraints, help avoid omitted functions/components and reduce the number of decisions when reconstructing a known boss. Participants also describe useful composition for repeated content and difficulty variants. The adverse counterpart is loss of exact detail, expressive freedom and source-level control. Some prefer SDML/code to invent new content and product lines for variants, or describe using both together as the library evolves. These are participant accounts and proposals, not measured player-quality, generation, balancing or long-term cost outcomes. Difficulty identifying the boss from noisy videos is reported across both methods.

The MDD notes contain a local wording inconsistency: one final tally says only one student prefers SDML, while the surrounding account and summary say most do. The CDD notes also mix approximate ranges and percentages. Preserve the qualitative disagreement and avoid turning those summaries into an exact new preference dataset. Prior statements about “ten versus fifty–one hundred decisions” are one participant's explanation, not an independently measured mechanism effect.

## Consequence for Nu and next action

For B03/B10/B12, this supplies a concrete positive comparator: prepared domain choices and constraints can help people describe desired game content, while greater control and unfamiliar requirements remain consequential. Nu's claims should distinguish discovering requirements, representing them, creating supported variants, extending the representation and preserving integrated behavior. A successful configuration or compiler diagnostic does not establish all of these outcomes. For D1, explicit option visibility is a plausible alternative explanation worth retaining; this is not an explicit-case versus equivalent-catch-all experiment.

Setup of the API, DSL, feature library, rules and generator is supplied to participants. Extending the annotative source is explicitly outside the experiment. The paper therefore leaves net setup/amortization, unsupported-feature evolution, debugging and deployment costs unmeasured. That limitation does not erase the favorable prepared-task scores. Nor do the MDD nulls prove that product lines lack value.

Next bind the original2022 predecessor and any distinct scoring details to this shared MDD cohort. Then prioritize the retained2025 Unreal model/code experiment for contemporary tool-integrated comparison; its title alone does not establish its task or execution setting. Phylogenix, newer practice, generative-asset integration and temporal/state alternatives remain open by consequence. Main-PDF/final-edition access and unknown Nu benefit remain separate. No author runtime, compiler, statistical model, candidate experiment or extra worker is executed.
