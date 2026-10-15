# S206 — ECOOP short report on scanner/parser typing

## Identity and complete publisher reading

Stefan Hanenberg, *Doubts about the Positive Impact of Static Type Systems on Programming Tasks in Single Developer Projects — An Empirical Study*, ECOOP 2010, LNCS 6183, pp. 300–303, [DOI10.1007/978-3-642-14107-2_14](https://doi.org/10.1007/978-3-642-14107-2_14). The native parent **`TCF847EU` v4983**, note **`VEA6FUPJ` v4988**, and publisher PDF **`VCD95IIU` v7119** were reverified before reading. The four-page PDF is 122,120 bytes with SHA-256 `37728b772a2306074172761cb994e8d30c3ff68996052a801c955858fd72fe74`.

**All four publication pages were read as extracted text and visually inspected**, including Figure 1's two boxplots and all nine references. The registered article PDF is an exact extraction of publisher-volume PDF leaves 311–314, which carry printed article pages 300–303. The 610-page source volume is 9,348,114 bytes with SHA-256 `3f9c290a84dee40c4bc337070c11d53577e9e4a04897574147dee88b581c65dd`. This preserves the volume/extraction lineage; it is not a four-page preview reconstructed from another edition. No participant logs, programs, hidden tests, or analysis code were acquired or executed.

The earlier 2026-10-02 reading covered only printed pp. 300–301 from publisher preview attachment **`TDV38UY3` v4985** (117,540 bytes; SHA-256 `a6c126a0448faefd455ec4bf28fa6ec10e56116b27d05cee77aa383ea53994d8`). Its access history remains valid, but its missing-results gap is now closed by the acquired publisher volume. The old preview must not be counted as a second edition or an independent study.

## Design, treatment, and outcome units

The study convenience-samples **49 undergraduate students**. Each implements a simplified scanner followed by a MiniJava-like recognizer specified by a context-free grammar. This is a between-subject design: each participant learns and uses only the static or only the dynamic version of the custom object-oriented language, avoiding a language crossover. The short report says participants were “divided” between groups; it does not report group sizes, random assignment, or the balancing interviews later described in [S132](S132-scanner-parser-types.md).

The two language versions share single inheritance, late binding, blocks, a small API, and a small IDE that can modify and run code. The static version uses a nominal, non-generic type system with declared types on variables and parameters and an additional cast operator; the dynamic version omits type annotations. The paper describes their semantics as identical apart from the cast, but the manipulation is still a bundle of annotations, checking/feedback, casts, and tool behavior. Every class or method write or modification is logged so the authors can reconstruct development steps.

Training is not equal in observed hours despite the design motivation of equal learning opportunity: the dynamic group receives **16 hours**, while the static group receives **18 hours**, with the additional two hours spent on the static type system. The report does not add these hours to either outcome. It also omits the fuller report's 27-hour/four-day task schedule. The comparison therefore does not estimate total onboarding-plus-development cost.

The two endpoints use different units:

- **Scanner:** elapsed development time until a reconstructed program state passes all hidden minimal-functionality tests. The ECOOP report says **25 test cases**.
- **Parser:** number, plotted as a percentage, of **400 hidden word cases** passed by the final recognizer: 200 valid and 200 invalid words.

Both language groups are compared with Mann–Whitney U tests. Figure 1 is descriptive only: its scanner boxplot places the dynamic distribution below the static distribution, while its parser boxes overlap substantially. It displays minima, maxima, medians, and quartiles, but no group sizes, exclusions, raw observations, uncertainty intervals, or effect estimates.

## Results and bounded interpretation

The dynamically typed group is reported significantly faster on the scanner endpoint (**p=.04**). The parser endpoint shows no statistically significant difference in successful tests (**p=.40**). The latter is failure to detect a distributional difference, not evidence of equivalence or equal practical performance. The short report does not disclose that the scanner timing result is conditional on participants who completed the hidden scanner tests; that denominator and its missingness must come from S132, not be inferred from Figure 1.

The paper presents the findings as a counterexample to a universal claim that static typing has an obvious benefit under all circumstances. It explicitly declines a general final verdict and calls for other tasks, maintainability/readability outcomes, and team settings. It names threats from the language, design, subjects, and tests but delegates their full treatment to the longer report.

## One experiment lineage with S132

The full publisher reading strongly supports treating S206 and [S132](S132-scanner-parser-types.md) as reports from **one experiment lineage**, not independent replication: author, 49-person sample, scanner/parser project, custom paired languages, 16/18-hour training, hidden outcome structure, and headline p-values all coincide. Exact participant, log, and test-suite correspondence is not independently verified. S206 is the earlier four-page ECOOP summary. Its reference 4 points to an unlocated technical report “to appear in June 2010,” not directly to the final 14-page OOPSLA publication recorded as S132. S132 supplies group sizes, assignment procedure, execution rules, schedules, raw result tables, exclusions, debugging proxies, and fuller threats. Study-level synthesis should count the lineage once while retaining each publication identity and the unresolved intermediate-report route.

There is one material source discrepancy. Printed p. 302 of S206 says the scanner used **25** hidden tests. A targeted return to the original S132 PDF, PDF page 7 / printed p. 28, verifies that section 4.4 says **23** hidden scanner tests. The underlying test suite was not acquired, so neither number can be repaired by assumption. The count is edition-specific and should be reported as 25 in S206 versus 23 in S132. This does not change the matching p=.04 result, but it prevents treating the endpoint definitions as textually identical.

S132 also supplies limits absent from S206: 25 dynamic and 24 static participants were assigned; 21 in each group completed the scanner endpoint, so four dynamic and three static participants were excluded from that timing comparison. Its parser analysis retains all 49. These facts explain why the short report's scanner statement is a completer-conditional result. They are linked-study context, not details independently recovered from S206.

## Consequences for R04 and D1

S206 is adverse evidence against assuming a static checker automatically reduces development time on every construction task. It does not isolate compiler diagnostics from other treatment components: static participants write declarations, learn additional typing rules, have a cast, receive two extra training hours, and—according to the fuller S132 account—face whole-program checking that can prevent execution. Earlier dynamic execution can expose behavior sooner, but neither paper experimentally separates that mechanism from annotation effort, learning, language design, or group composition.

For R04, compiler exposure and observable behavioral change must remain separate measurements. A diagnostic or blocked run is not evidence that a requested behavior has been preserved, and a behavioral test result does not price the work of satisfying the checker. The study suggests recording both feedback events and task behavior, while counting training and adaptation cost for each arm.

For D1, the study does not compare explicit case enumeration with an equivalent catch-all, future-case extension, retained behavior, F#, Nu, maintenance, or agent work. Both D1 sources may be statically checked and initially exhaustive. S206 therefore motivates treatment separation and adverse-result preservation; it does not predict which D1 representation will perform better.

The selected S206 publication reading is complete. Remaining limits are the unresolved 25-versus-23 test-suite provenance, unavailable primary logs/tests/code, and the unlocated June 2010 technical report cited by S206, not missing article pages.
