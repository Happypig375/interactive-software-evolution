# S295 — Persistent-object evolution, mappings and repair obligations

Tetsuo Kamina, Tomoyuki Aotani and Hidehiko Masuhara, *Evolution Language Framework for Persistent Objects*, The Art, Science, and Engineering of Programming 10(1), article12, published15February2025. [Printed DOI10.22152/programming-journal.org/2025/10/12](https://doi.org/10.22152/programming-journal.org/2025/10/12); [arXiv2502.20530v1](https://arxiv.org/abs/2502.20530v1).

**Disposition:** all39 main/appendix/bibliography pages read;27 selected pages inspected visually, covering all20 figures, Table1 and formal appendices A–F. The associated accepted artifact is inspected at README, archive-inventory and classification-workbook scope. No author program, database, formal checker or experiment is executed. The paper supplies a constructive evolution method and favorable coverage of selected historical edits; it does not measure maintenance savings or establish arbitrary live-state preservation.

## What evolves, and what the programmer supplies

Here a persistent object is an object stored in a database, not a functionally persistent data structure. The core language abstracts Java-like classes, fields and methods, with supplied identifiers and class-tagged runtime identities. Constructors retrieve or insert represented objects; `set` updates their fields. The small calculus omits important full-language features, including method overriding and transient fields. [Primary paper, §§3–5](https://arxiv.org/pdf/2502.20530v1.pdf).

The evolution language separates changes to class declarations and expressions from the concrete database mapping. Its eight user-facing operations create/rename classes, rename/add/delete fields, change field types, extract a superclass and merge classes. An internal class-deletion operation helps define compound changes. Renaming transforms relevant references. Adding a field requires a supplied, well-typed default object and adds corresponding arguments to constructors and field updates. These are explicit migration policies, not automatically recovered successor intent.

Superclass extraction partitions represented fields. Class merging has structural and method-name restrictions, including a direct inheritance relation and no remaining subclasses of the removed class. Constructor uses of that class must already have been removed or replaced outside this evolution language. The paper assumes an editing environment selects suitable operations; unsupported changes and some preparatory edits remain developer work. Tool construction is future work in §8.

The paper expressly separates this scope from changing running objects online. Multiple program versions may access the database, but multiple class versions within one Java process and dynamic software updating are outside the presented method (§3 premises and §7). A comparison with Nu must therefore name whether it concerns stored data, a historical value, a running computation or a host effect.

## Two mappings and their boundaries

The JPA-like mapping uses a table per represented class and an instance per row, with an identifier as primary key. The concrete inheritance treatment corresponds to `TABLE_PER_CLASS`/`@MappedSuperclass`, rather than covering every JPA strategy. Database evolution reuses BiDEL operations.

The signal-class mapping instead gives an object a time-series table. Updates append timestamped values; access selects a current value. Splitting and merging tables must preserve appropriate identity and timestamp relationships. The JPA merge uses an inner join under a foreign-key premise; the signal mapping uses an outer join, which can create empty cells at some timestamps. These are different data contracts even when the abstract class edit has the same name.

The signal presentation has an unresolved detail: §5.2 describes selecting the latest value of a column, and Figure14 shows a later row with an empty cell; Figure20's `Select` rule selects the latest tuple and then projects the field. The inspected definitions do not reconcile that case explicitly. This is a publication-definition gap, not an observed implementation failure. Snapshot/time-cursor details are expressly abstracted in footnote9. The method is not a proof of complete history restoration or continued control flow.

BiDEL supplies the multi-schema propagation dependency. Reuse the already reconstructed [S103](S103-bidirectional-schema-versions.md) and [S236](S236-multischema-placement-advisor.md) conditions: hidden information, mappings and cross-view policies matter. Describing multiple database versions as consistent does not establish preservation of unrepresented invariants, pending work or irreversible effects.

## Conditional preservation is useful, but not universal repair

AppendixB's preservation and progress arguments depend on the core language, well-formed store and query lemmas. AppendixC's evolution typing theorem excludes class deletion, field deletion and field-type change. The text explicitly leaves resulting type errors for compiler diagnosis and developer repair. The behavior theorem is a conditional one-step correspondence between original and evolved expressions, under the relevant typing/store assumptions. It does not infer intended new requirements.

Two proof-presentation discrepancies remain material to any stronger guarantee: the proof of C.1 includes a field-type-change case despite the theorem's exclusion; the constructor and `set` cases in C.2 treat non-renaming transformations as unchanged, whereas Figure10 and AppendixF.3 explicitly add default arguments for `AddField`. We retain the stated restricted results and constructive transformations without certifying a mechanically checked proof. No independent proof repair or counterexample execution is performed.

For Nu's type-evolution question, the useful distinction is between an operation vocabulary, the conditions under which it preserves a represented contract, and the remaining behavioral obligations. Field deletion and type change can belong to a supported editing vocabulary while still requiring manual repair. Neither a compiler diagnostic nor successful type repair establishes all intended behavior.

## Historical coverage and the accepted artifact

The empirical component manually classifies per-class deltas from three JPA projects through the last commit before27March2024:100 Broadleaf Commerce classes,60 Keycloak classes and34 Apollo Config classes. Broadleaf uses the top100 annotation-search matches, adds two superclasses and removes two irrelevant matches. This is a selected corpus, not a random sample of software evolution. One author performs the classification; a delta may receive several labels. Simultaneous field-name/type changes count as deletion plus addition, and a field move can count as both merge and new inheritance.

Table1 gives **650/340/45** labels across its seven supported structural categories, versus **5/5/1** across three unsupported categories, for Broadleaf/Keycloak/Apollo respectively. These are our sums of the printed rows, not counts of independent commits or verified successful migrations. **250/108/12** of those supported-category labels are field deletions or type changes—the very cases excluded from the typing-preservation theorem. The positive finding is that the vocabulary describes many selected structural changes.

The authors also identify unsupported mapping-strategy changes, component extraction needing foreign-key work, and converting field names into collection keys. Their concrete mapping covers only one of the three observed inheritance strategies: Broadleaf uses `JOINED`, Keycloak `SINGLE_TABLE`, and Apollo `TABLE_PER_CLASS`. The empirical classification is syntactic and abstracts unsupported Java features. Signal-class transfer is argued, not evaluated on a signal-class history corpus. No comparative effort, defect, migration-runtime or net-benefit measurement is reported.

The [accepted artifact](https://doi.org/10.5281/zenodo.14716986) contains a workbook, extracted class versions and repository clones. Its README confirms manual classification and contains no automation tools. We acquire both README versions and the workbook; source histories and clones remain uninspected beyond their archive paths. This is arithmetic/definition inspection, not independent reclassification or study reproduction.

All four workbook sheets, their summary definitions and **2,561 formula cells** are inspected computationally. Independently evaluating the stored `COUNTIF`/`SUM` expressions, including shared-formula offsets, agrees with every cached formula value. The original workbook is unchanged; this is not a native Excel recalculation. Its published totals nevertheless differ from Table1:

| Project / category | Paper Table1 | Workbook summary | Cell |
| --- | --- | --- | --- |
| Apollo, non-code plus computational | 131+178=309 | 312 under code0, irrelevant to persistence | `ApolloConfig!AJ45` |
| Apollo, non-structural schema | 79 | 77 | `ApolloConfig!AJ46` |
| Keycloak, field addition | 189 | 190 | `keycloak!BJ170` |
| Keycloak, field deletion | 92 | 93 | `keycloak!BJ172` |
| Keycloak, fields made a collection | 2 | 1 | `keycloak!BJ180` |

The workbook's code0 combines changes irrelevant to persistence; it does not reproduce the paper's separate non-code/computational split. The Broadleaf and Keycloak combined totals agree with the paper; Apollo's does not. Keycloak's shared formulas from columnC onward start at row4. Cell`M3` contains code16 and lies outside that summary range; including it would supply the paper's second collection label. Other row3 cells include inheritance labels as well as new-class labels, so indiscriminately extending the ranges is not a justified correction. The intended initial-version inclusion policy and remaining discrepancies are unresolved. They do not erase the broad vocabulary-coverage result, and neither version warrants a precise safe-migration percentage.

## Identity, coverage and library record

The publisher's2025 landing page links arXiv2502.20530v1. Its PDF and the author-hosted copy are byte-identical: **2,009,561bytes**, SHA256`bc33632dec5cd9b19cd6e237d1338bee45c11659c4da7786535f74770a25ae14`, MD5`ff215b2240d5ae7024aca1a01c92bc01`. Crossref also serves the same title/authors/date/volume under DOI`10.22152/programming-journal.org/2026/10/12`; arXiv and the artifact cite that alternate year string. The inspected title page prints the2025DOI. These are retained aliases/metadata discrepancies of one work, not two publications or independent studies.

All39 text pages, nine footnotes and34 references are covered. Visual pages are **1,3,4,6,7,9,11–18,20,24–35**; other pages are text-read. All20 figures, the table and all formal appendix displays fall within that visual coverage. Publication reconstruction does not certify the proofs or repository execution.

Zenodo declares a989,940,412-byte ZIP. Bounded ordinary HTTP range requests read its25,407-entry central-directory inventory and extract two members, with decompressed size/CRC and SHA256 checks. The whole archive is not acquired and its declared MD5 is not verified. The143,287-byte workbook has SHA256`638c15671b17e96a5d6505e53db144aff8955cb6f4a8ca3ff436ed72b7c8f020`; its inner README has4,176bytes, while the separately served README has3,878bytes and omits older Google Drive instructions. Both README versions are read; the alternate Drive routes are not followed.

Collection`PKLXQNEE` and global DOI/title/edition checks found no exact parent before deliberate primary reading. Native parent **`XPA4J995`**, note **`U3W7TYXU`**, PDF **`L3HMIGER`** and workbook **`9IDPYM5L`** retain this work and selected supplement. Existing membership, object versions and PDF attachment are preserved when the workbook is added; both attachment hashes match. Final note/version verification is recorded in the search ledger. Private bodies, extraction text, workbook and raw evidence remain ignored by Git.

## Consequence for the Nu survey

S295 resolves the retained persistent-object method at its actual abstract/concrete boundary. It adds class/field evolution and stored-data mappings to the existing document, relational and live-state comparisons. It does not create a requirement to read every database predecessor before making a bounded Nu claim. Signal Classes and ESCHER remain conditional dependencies if a future claim needs their original reactive-history or automatic-conversion method.

The source audit records61 occurrences and41 normalized units:2credited,37deferred and2unused. The credited units are one paper and its associated artifact. Comparison with180 prior decision files finds five historical identities: the main work receives a material reading update and four unchanged screens are withheld. Scite answer`nu_background_s295_20261008` accepts37decisions:2credited,33deferred and2unused. Receipt and `citation_report` preserve all37 memberships/decisions and221 of222 compared fields; the service returns512 of521characters in the main paper's reason, truncating its final sentence. The complete local reason and this note retain the no-execution boundary. Zero skips, missing reasons or linkage warnings; report lists are not truncated and answer-scoped retrieval is null. No unchanged decision is resubmitted to fix the field cap.

The remaining task is to account for consequential discovery paths and missing primary contracts across the existing survey, then synthesize a defensible claim and comparison. Access-limited generation/corpus papers remain explicit; missing Nu-specific empirical benefit remains a separate question. No experiment, adapter, extra worker or acquisition purchase follows from this reading.
