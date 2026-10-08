# S42 Streams and loops with their dedicated debuggers

**Full publication reading completed 2026-10-08.** Jan Reichl, Stefan Hanenberg and Volker Gruhn, *Does the Stream API Benefit from Special Debugging Facilities? A Controlled Experiment on Loops and Streams with Specific Debuggers*, ICSE 2023, pp.576–588, DOI [10.1109/ICSE48619.2023.00058](https://doi.org/10.1109/ICSE48619.2023.00058). Existing Zotero parent `LQPAZLXG`, PDF `G6KGJBE3`, collection `PKLXQNEE`, and the two existing notes were verified before reading. The earlier acquisition-only status is superseded; the source identity and S42 ID are retained.

The study supplies a useful positive result and a reversal: its stream-plus-debugger package is faster overall, while loops with the stepwise debugger are faster when the failing object is identified in advance. This is evidence for studying task and information conditions alongside a programming-system package. It does not isolate a language effect or the additional benefit of a debugger independently of the code representation.

## Identity and coverage

All thirteen publisher-layout pages, all three figures, Tables I–III, twelve numbered footnotes and 56 printed references are read textually and visually. Crossref's 56 reference records agree with the printed roster at the inspected identity scope. The existing local and native PDFs are byte-identical: 355,888 bytes, SHA256 `1299f979077c309e7564c7dde13f6898a51ac24c3b7f1f6f647543a98cab62a6`, MD5 `6a2e1bb4f0a0fd18fbe97b924abf2c54`. PyMuPDF extraction supplies 78,292 characters. An earlier pypdf layout extraction inserted excessive spacing and warned about rotated text; Poppler rendered with a missing Symbol-font warning. All thirteen MuPDF page images were therefore inspected, including the original statistical symbols and dense page-7 tables. No publisher body, extraction or source package enters Git.

Footnote 9 links the [author's additional-material folder](https://drive.google.com/drive/folders/14Eg4krlQWZO8yrZlWMp325GGn42GtC2h). The web reader cannot open it, but a direct public HTTPS request succeeds. The folder lists an author preprint and `AdditionalMaterial.zip`; only the ZIP is newly acquired. It is 373,663 bytes, SHA256 `d8c1fa5009f7ed1214c484ed16206be773cca87af5282e923343a75a5254edfe`, with 36 nondirectory files. Two README files and seven Java files are read completely: `AllEventListener`, `ExperimentAction`, `Configuration`, `GeneratorController`, `LoopGenerator`, `StreamGenerator` and `TestGenerator`. Other source/build files and the binary SPSS data/output remain unread. The publication-era experiment used IntelliJ 2020.2/JDK14; the README also documents a later 2022.2/JDK18 development environment. Available source is not certified as the exact executed build. Nothing is compiled or run, and statistical reproduction is not claimed. The ZIP is preserved under the existing Zotero parent as attachment `SXT4RSCY`; stored bytes are hash-verified.

## What was assigned and measured

Twenty purposively recruited professional Java developers, aged 20–50, volunteered after reporting frequent industrial Stream API use; sixteen were men and four women. Each remotely used an author's machine. There was an informal individual introduction, not a standardized training examination. The comparison assigns **loops with a stepwise debugger versus streams with IntelliJ's stream debugger**; it is not a crossed API-by-debugger experiment.

Every participant receives all sixteen combinations of four binary within-person factors: programming/debugging package, known versus unknown failing object, failing-object position in the first versus last third, and failing-field position in the first versus last third. Task order and concrete positions within those regions are randomized. The planned design has 320 repeated task observations, not 320 independent developers. Generated tasks fix forty objects and thirty fields/filters. The paper says these values were chosen following pretests that exposed the interactions; population prevalence of that workload is not established.

Filters compare fields with simple literals; an interface's Javadoc supplies the intended criterion. Object IDs support identification. The known-object condition identifies a missing object; the unknown condition gives a result mismatch. Generated tasks vary names and values to reduce repeated-task learning, which does not eliminate carryover. The measured outcome is elapsed task solution time, including the prescribed debugging workflow, on these prepared local filter repairs. Repository-wide fault localization, creative diagnosis, onboarding and subsequent maintenance are outside the tested outcome.

## Positive, null and adverse results

| Condition | Loop/stepwise mean seconds | Stream/debugger mean seconds | Reported interpretation |
| --- | --- | --- | --- |
| Overall | 232 | 114 | Stream package faster; repeated-measures ANOVA reports p<.001 and partial eta squared .899. |
| Failing object unknown | 401 | 139 | Stream package faster; approximately 2.88 times the elapsed time with loops. |
| Failing object known | 63 | 88 | Ordering reverses; stream package takes approximately 1.40 times as long. |
| Unknown object in first third | 170 | 141 | Authors report no significant difference; this is not equivalence. |
| Unknown object in last third | 633 | 136 | Large favorable stream contrast in this constructed cell. |
| Known object, first/last third | 64 / 62 | 87 / 89 | Loop package faster in both reported position cells. |

These are rounded published means and condition-specific comparisons, not a pooled estimate for Nu. Figure 3 uses logarithmic time axes and shows the known-object crossover. Field position also changes the size of the package contrast. The study reports tool interaction and startup costs, including mouse versus keyboard use and several seconds to initialize some stream views. More complicated predicates, unordered or parallel collections and different task sizes can change the comparison; the authors' predicted effects outside the experiment remain hypotheses.

Two printed inconsistencies remain explicit. The abstract gives partial eta squared .928 for the package-by-known-object interaction, whereas Table I and the conclusion give .933. Table I prints F=61.250, p=.948 and partial eta squared <.001 for K×FP, an internally inconsistent combination. Several ratio labels and a Table II/III reference also have apparent copy errors. This reading preserves the published values and does not repair the statistics from guesses. The principal mean crossover appears consistently in the text and tables; the reporting errors do not justify discarding that scoped finding.

## What the selected artifact establishes

The configuration generates sixteen conditions, skips the middle positional thirds, fixes 30 fields/40 objects and targets twenty passing objects. The controller constructs a single changed comparison value in the selected implementation; the other implementation remains the generated reference. Both generators and the test generator are inspected. The test compares membership of the two results on the same generated object list. The known condition prints differing object IDs; the unknown condition prints differing-object counts. It does not establish a separate held-out semantic oracle or exhaustive correctness over arbitrary inputs.

The plugin starts timing when generation terminates and ordinarily advances after the test-suite callback reports all tests passed. This bounds “solution” more concretely than the main paper alone. The inspected callback is not explicitly restricted to the named test configuration, and the plugin also contains a manual early-finish route that calls the completion handler. Whether those paths affected recorded participants is unknown. The paper and acquired binaries have not been reconciled to per-attempt logs; neither contamination nor full exclusion accounting is asserted. The README's JUnit wording and the generator's TestNG imports further counsel against treating the distributed setup as an independently validated execution recipe.

## Consequence for the Nu agenda

1. Compare credible programming-system packages when the question concerns a practical workflow. Attribute any observed difference to that package unless a separately justified design isolates the representation or tool.
2. Prespecify whether a failure report already identifies the relevant entity, event or point in history. Treat this as assigned information or a baseline task characteristic, not a post-outcome subgroup chosen for a favorable result.
3. Keep complete correct repair, supplied-test agreement, diagnosis and elapsed time distinct. A Nu study needs independently specified old/new behavior obligations, including temporal/effect boundaries where relevant.
4. Retain realistic tool initialization, navigation and setup costs. An overall winner can hide a useful reversal by task; the purpose is actionable conditions of benefit, not a universal ranking.

S42 raises the value of a conditional debugging/recovery comparison in the [Nu research agenda](../../nu-research-agenda-2026-10-08.md). It supplies no Nu, F#, coding-agent or whole-game effect estimate. Its references to reactive comprehension, time-travel debugging, developer experience and crossover methods retain their existing reading states; citation-context inspection does not create 56 new full readings.
