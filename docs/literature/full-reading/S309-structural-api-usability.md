# S309 — Structural measures of API usability

G. M. Rama and Avinash Kak, *Some structural measures of API usability*, DOI [10.1002/spe.2215](https://doi.org/10.1002/spe.2215). The selected source is the authors' Wiley-formatted early-view PDF: it says “Copyright © 2013”, records online publication on 3 September 2013, and has no issue pagination. The later bibliographic issue is *Software: Practice and Experience* 45(1), 75–110 (January 2015). Findings below belong to the inspected early-view bytes and are not silently relabelled as inspection of the paginated issue.

**Complete primary reading, 2026-10-15.** All 36 PDF pages were extracted and read, including formulas, algorithms, threats, conclusion and all 51 references. All 36 pages were rendered and visually inspected in nine four-page contact sheets. PDF pages 9–11, 14–19, 21–35 were additionally inspected as individual full-page renders; these cover every displayed formula, Table I, Algorithm 1, both tool screenshots, Figures 3–11, Tables II–VI, result examples, threats and conclusion. Pages 1 and 36 were also checked at full-page resolution for edition identity and the end of the references. No supplement, dataset, implementation or participant material accompanies the PDF. No metric implementation or empirical analysis was reproduced.

## Decision answer

The paper does **not** empirically validate the eight metrics against developer outcomes such as task success, time, errors, comprehension, learning, maintenance effort or productivity. It has no recruited users, expert-rating panel, allocation, tasks or measured development outcomes. Its “experimental support” consists of calculating structural scores for seven Java systems, comparing the scores with counts of the same structural features, manually inspecting selected low/high cases, and sometimes checking whether the direction agrees with community commentary or a Java 2/Java 5 comparison (PDF pp. 23–34). This provides worked operationalization, face checks and limited internal/known-groups evidence. It does not establish criterion, predictive or causal validity for API usability.

The authors acknowledge the decisive gap: strictly answering whether programmers find low-scoring APIs difficult would require a human-centric study, which they reject here as too expensive and confounded (p. 34). Their alternative is to identify declarations that contribute to low scores and explain why those declarations might be difficult. The paper also makes no cross-language validation: every evaluated system is Java, while language independence is argued from the metrics' use of signatures and documentation rather than tested (p. 34).

## Construct and nine motivating issues

“API” is narrowed to published method declarations. The authors explicitly exclude implementation and do not evaluate whether an API is functionally complete; structural usability is one quality alongside correctness, performance and other concerns (pp. 2–3). The nine issues are presented as common design concerns, not nine prospectively tested causal hypotheses, and the list is explicitly non-exhaustive (pp. 3–8):

| Issue | Proposed problem | Metric |
| --- | --- | --- |
| S1 | Overloads with the same name return different types. | AMNOI |
| S2 | Adjacent runs of parameters have the same type. | APXI |
| S3 | Methods have long parameter lists. | APXI |
| S4 | Similar parameter names/types are ordered inconsistently across methods. | APLCI |
| S5 | Method names are nearly identical. | AMNCI |
| S6 | Conceptually related methods are dispersed rather than grouped. | AMGI |
| S7 | Documentation does not state thread-safety status. | ATSI |
| S8 | Declared exception classes are too general. | AESI |
| S9 | Method documentation is absent or too short. | ADI |

Thus nine issues yield eight metrics because APXI combines S2 and S3 (Table I, p. 19). There is a small terminology mismatch: S4 and the APLCI construction use parameter **names** and their order (pp. 6, 11), whereas Table I describes “parameter types” (p. 19).

## Metric reconstruction

All eight scores are intended to range from 0 to 1, with larger values interpreted as structurally better. System results are described as means of class-API scores (p. 23). That aggregation does not by itself supply a usability criterion.

1. **API Method Name Overload Index (AMNOI), p. 9.** For an overload group \(G_j\),
   `AMNOI(G_j) = 1 - (|{Returns(m): m in G_j}| - 1) / (|G_j| - 1)`.
   The API score is the mean over its \(N\) overloaded-name groups. One means that all overloads in every group share a return type; zero means every overload in every group has a different return type. The validation excludes constructors. The authors note that overloading used to simulate generics can make the metric pessimistic.

2. **API Parameter Usability Index (APXI), pp. 9–11.** Let \(A(m)\) be a method's ordered parameter sequence. The length component is `C_l = (1/|M|) Σ_m g(N_d, |A(m)|)`, where `g(x,y) = exp(x-y)` when `y > x`, otherwise 1. Let \(S_pt(m)\) contain adjacent equal-type parameter pairs. The type-run component is `C_s = (1/|M|) Σ_m h(m)`, with `h(m) = 1 - |S_pt(m)|/(|A(m)|-1)` for methods with more than one parameter and 1 otherwise. `APXI = (C_l + C_s)/2`. Validation fixes the desirable maximum \(N_d=4\); the threshold is a choice, not an estimated human limit. Type identity, conversions and call syntax can change the construct across languages.

3. **API Parameter List Consistency Index (APLCI), p. 11.** For each parameter-name pair \(p_i,p_j\), the method set \(M_{p_i,p_j}\) is eligible when at least three methods contain both names. It is consistent only if every eligible declaration uses the same relative order. APLCI is the number of eligible consistent sets divided by all eligible sets. Unrelated methods that happen to reuse common names can depress the score.

4. **API Method Name Confusion Index (AMNCI), pp. 12–14.** Canonicalization removes underscores, numeric suffixes and case distinctions. Duplicate names from overloading are first removed. Let \(C\) be the method names whose canonical form is shared with another name and \(M\) the distinct method names: `AMNCI = 1 - |C|/|M|`. It detects only the three encoded name variations; the authors reject edit distance because semantically different names can be close, and acknowledge that other mnemonic suffixes are missed.

5. **API Method Grouping Index (AMGI), pp. 14–15.** Common prefixes/suffixes are removed, names are split at connectors and case changes, and fragments whose occurrence exceeds a threshold \(theta\) become keywords. For keyword \(s_j\), let \(O(s_j)\) be the number of matching declarations and \(R_j\) the number of contiguous runs: `AMGI(s_j) = 1 - (R_j - 1)/(O(s_j) - 1)`. The API score averages the keyword scores. Multiple keywords and semantically weak fragments can make the result pessimistic. The validation assumes declarations are alphabetically sorted, as in Javadoc, even when they were extracted from source (pp. 29–30).

6. **API Thread Safety Index (ATSI), p. 16.** Let \(T\) be methods whose associated documentation contains both substrings `thread` and `safe`: `ATSI = |T|/|M|`. A class- or package-level statement applies to all included methods. The score counts documentation of both safe and unsafe status as success. Unrelated uses of those words can produce false positives.

7. **API Exception Specificity Index (AESI), pp. 16–17.** In the exception hierarchy, exception \(e\) has depth \(D\) and height \(H\): `AESI(e) = D/(D+H)`. A method averages its declared exceptions; methods declaring none receive a sentinel −1 and are omitted from the API mean. Leaves score 1 and the root scores 0. Unchecked exceptions are excluded. Global hierarchy depth may not reflect contextual specificity, especially for custom exception subtrees.

8. **API Documentation Index (ADI), pp. 17–18.** For documentation word count \(L_d(m)\) and user-set threshold \(Psi\), `ADI(m) = 1` when `L_d(m) >= Psi`, otherwise `L_d(m)/Psi`; ADI is the mean over methods. Validation uses \(Psi=10\). The measure is explicitly quantity, not semantic quality.

The proposed use is relative: compare versions, modules or teams; treat a decrease as an early warning; then inspect the declarations reported by tool hooks (pp. 20–23, 35). The authors say an uncalibrated absolute label such as “low” is moot outside comparison. Their HTML report offers system and module views and lists contributing methods, but inclusion in a release dashboard is a plan, not an evaluated deployment.

## Seven systems and actual extraction

The evaluated corpus comprises Java 2 (JDK 1.4.2), Java 5, Eclipse JDT, Petstore 1.3.2, Hibernate, Compiere R2.6.0c and one large proprietary legacy financial system (pp. 21–23). Public method headers were scanned from source; for each class they became that class's API. Only packages in Oracle's online documentation were included for Java 2/5, deprecated methods were excluded, and Eclipse packages containing `internal` were excluded.

Two source-version footnotes are internally awkward and should not be repaired by inference: Eclipse is called “Version R3.3” but its download URL names `R-3.2.2-200702121330`, and the Hibernate URL names `3.2.5.ga` (p. 22). The financial system is not independently identifiable. These are the paper's corpus descriptions, not reconstructed builds.

The paper repeatedly calls the metrics derivable from API documents, yet the evaluation actually scanned sources because that was easier; it asserts the declarations would match Javadoc when Javadoc exists (p. 22). No extraction accuracy audit, frozen source archive, tool source or per-class dataset is supplied in the PDF.

## What the reported checks establish

The checks are useful as executable examples of the definitions:

- **AMNOI:** Table II reports overloaded methods, overload groups and groups with differing return types. Java 5 has 3,763 overloaded methods in 1,495 groups, of which 137 are marked problematic. A Java 5 `Attribute` class example scores .333 after two of three overload groups differ in return type (p. 24).
- **APXI:** Petstore is lowest. A 13-parameter `Item` constructor has 11 of 12 adjacent pairs with equal types; with \(N_d=4\), its length component is approximately .0001, type component .0833 and APXI .041728 (pp. 25–26).
- **APLCI:** Table III reports eligible parameter-name groups and inconsistent groups, such as 749 and 8 for Compiere. A three-method `MPrivateAccess` example reverses `AD_User_ID` and `AD_Table_ID` and scores 0 (pp. 26–27).
- **AMNCI:** Table IV reports API methods and methods flagged as confusing, including 25,540 and 90 for Java 5 and 6,622 and 632 for Financial. Its headings do not identify the first column as a globally deduplicated name count. Two class examples apply `1-|C|/|M|`: 2 of 5 confusing names produce .6; 2 of 7 produce approximately .7143, printed as .7141 (pp. 28–29).
- **AMGI:** Financial scores .5452 and is interpreted through its ten-year evolution. A Java 5 `DecimalFormatSymbols` example derives .1599 by averaging five keyword contributions after examining declaration runs (pp. 29–30).
- **ATSI:** Only Java 2 and Java 5 are compared. Swing rises from .030 to .094, directionally matching the authors' expectation that Java 5 better documents thread safety, but the authors still judge .094 low and cite an `XMLEncoder` omission (pp. 30–31).
- **AESI:** Table V reports methods declaring any exception and methods declaring root `Exception`, including 1,101 and 162 for Hibernate. Application-specific exceptions are ignored in this evaluation. An `InvocationHandler` declaration of root `Throwable` scores 0 (pp. 31–32).
- **ADI:** Table VI reports class counts and classes with zero or insufficient documentation. Financial scores .18 and Eclipse .9. A seven-method `StreamHandler` example averages five full contributions and two fractional word-count contributions to .88 (pp. 32–33).

These examples show that the formulas can distinguish selected structural cases and reproduce hand-counted inputs. They do not show that score differences predict actual ease, effort or outcome. Many “quantitative assessments” are counts of the same elements already used by the metric, and manual inspection of selected extremes often restates the encoded rule. Community beliefs and version comparisons add face plausibility but are neither blinded nor independent outcome measures.

## Falsifier-relevant inconsistencies and limitations

AMNCI has an unresolved internal reporting inconsistency. Section 4.4 defines the score as `1-|C|/|M|`, and both worked class examples use that direction. Algorithm 1 line 9 instead prints `|C|/|M|`, omitting `1-` and reversing the score (pp. 14, 21, 28–29). More strongly, Figure 1 reports Java 5 AMNCI as `.746`, while Table IV reports only 90 confusing names among 25,540 and Table VI reports 2,848 API classes (pp. 22, 28, 32). Under the stated per-class formula and system-level class mean, even assigning score 0 to 90 different affected classes leaves a lower bound of `(2848-90)/2848 = .9684`; concentrating confusing names in fewer classes raises that bound. Petstore similarly reports 12 confusing names and 262 classes, giving a lower bound of `.9542`, while Figure 7 is visually about .77. The PDF provides no data or implementation that can reconcile the formula, pseudocode, gross counts and reported system values. This does not prove which component is wrong, but it prevents treating the reported AMNCI system results as a successful validation of the stated metric.

The broader threats are substantial and partly author-acknowledged (pp. 33–34):

- system scores are averages over classes, but class size weighting and empty/undefined cases can change interpretation;
- selected manual low/high examples are not a statistical analysis, and the authors explicitly decline deeper analysis for focus and space;
- thresholds \(N_d=4\), \(Psi=10\) and the AMGI keyword threshold encode judgments without outcome calibration;
- alphabetical ordering, Java exception hierarchies, declared exceptions, source/Javadoc presentation, and exact parameter types are part of the operational construct rather than language-neutral details;
- documentation substring and word-count proxies can reward irrelevant text and miss useful concise text;
- seven heterogeneous systems are treated as validation units without uncertainty estimates, preregistered predictions or controls for domain, age, API size and documentation practice;
- the Java 2/Java 5 contrasts are version comparisons with many simultaneous changes, not metric interventions.

The claim that hundreds or thousands of classes lend “statistical validity” (p. 23) is unsupported by a sampling model, uncertainty analysis or independent criterion. A large number of class scores cannot substitute for observing the target developer construct.

## Transfer to C++, F# and GDScript

S309 itself evaluates only Java. It supplies no evidence for C++, F# or GDScript and cannot establish the method of unread S308 merely because S308 reportedly applies API metrics to game engines.

Some syntactic quantities could be reimplemented for a specified C++ or F# public API, but their meaning depends on the target's overload rules, generic/type system, currying or tuple/record conventions, optional/named arguments, documentation generator and declaration ordering. AMGI especially changes when display order changes; AESI requires an analogous declared exception hierarchy; ATSI and ADI depend on documentation conventions. For a language/toolchain without Java-like overloads, exact static parameter types or declared exception classes, the corresponding scores can become degenerate or require a new construct. That applies directly to any proposed GDScript adaptation unless its API representation and call/documentation semantics are specified first.

On this paper's evidence, use these metrics in Nu study preparation as predeclared **structural descriptors or lint candidates** after a language-specific mapping and extraction audit. This evidence does not justify labelling them API-usability outcomes or substituting them for task success, errors, comprehension, time, assistance or total maintenance work. A credible validation would preregister score predictions, sample APIs beyond the derivation corpus, measure relevant developer outcomes on realistic tasks, report uncertainty and confounders, and test whether the metric adds predictive value beyond simpler size/documentation counts.

## Native and private evidence

Registered before substantive reading in collection `PKLXQNEE`: parent `QK6399JY` version 7252, citation key `Rama2015StructuralAPIUsability`; attached PDF `DLCXECD4` version 7267. Native identity and parentage were rechecked without mutation.

PDF attachment `DLCXECD4`: 1,726,026 bytes; 36 pages; SHA256 `0fc175548dfef995d4ede24ca0f25bd200000269ac773f97fc732502f63ef49b`. The acquisition receipt is under `.artifacts/s309-structural-api-20261015/acquisition/`; native snapshots, extraction, renders, contact sheets and the coverage receipt are under `.artifacts/s309-structural-api-20261015/reading/`. Local attachment paths, copyrighted text and page renders remain outside Git.
