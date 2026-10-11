# S38 Cognitive Dimensions and the boundary of a usability claim

**Full publication reading completed 2026-10-11.** T. R. G. Green and Marian Petre, *Usability Analysis of Visual Programming Environments: A ‘Cognitive Dimensions’ Framework*, Journal of Visual Languages and Computing 7(2), 1996, pp.131–174, [DOI 10.1006/jvlc.1996.0009](https://doi.org/10.1006/jvlc.1996.0009). Existing Zotero parent `X52S9RPV`, canonical evidence note `VNBHNCAQ`, both PDF children and membership in `PKLXQNEE` were verified through the native local API **before selected reading**. Its journal-article type is appropriate; the paper is not a preprint. Reader: the main Codex session, without independent review or experimental reproduction.

The useful contribution is a vocabulary for explaining task-dependent trade-offs in programming environments. A small editing exercise also supplies a concrete favorable result for text editing. Neither establishes a validated learning score, a universal ordering of programming systems or an effect on Nu users or coding agents.

## Edition, coverage and provenance

The selected existing attachment is `YT8S985E`: **44 PDF pages, 659,095 bytes**, SHA256 `88465adb3261286d6ba400de51cf9440adc441eed90ef5ae8d74bd4494cbb3bc`. Attachment `MFW7CG4D` is the previously identified byte-identical duplicate, with its correction history preserved. No new PDF was downloaded. The publisher-layout title page identifies the 1996 article, pp.131–174, and its acceptance date. Scite's exact DOI lookup agrees on title, authors, volume, issue and pages; its access-denied metadata response is not the body used for reading.

All PDF pages 1–44 were read from the extracted text, including sections 1–6, acknowledgments, 91 printed references and the complete viscosity appendix. Rendered PDF pages **1, 10–13, 16, 21–24, 26, 28–29, 31–33 and 42–44** were inspected: the title, all fifteen main figures, all three appendix figures, code and numerical/graphical examples, and the printed editing-time comparison. Rendering alone was not counted as inspection. PyMuPDF text extraction and the rendered pages complement one another; source formulas and figure labels were checked visually where extraction was ambiguous. The references are a read bibliography, not 91 independently verified or reconstructed papers.

The paper discusses **Microsoft Basic 2.0, LabVIEW 2.0.6 and Prograph 2.5**. These versions bound its concrete tool observations. Original executable programs, interaction logs, raw timings and a reproducible experimental package were not acquired or executed. The private PDF, extraction, images, API snapshots and retrieval/decision receipts stay outside Git.

## What the framework does

Sections 1–3 propose an inexpensive, broad assessment of the relationship between a notation, its environment, a user's activity and the problems being solved. They do not offer a detailed cognitive model or claim that one collection of design rules optimizes every activity. The chosen scope emphasizes exploratory and incremental programming. Safety-critical criteria, performance engineering, requirements negotiation and organizational work are explicitly outside the paper's main treatment.

The argument combines earlier research, authors' experience, expert comments, illustrative analyses and selected observations. Predictions, anecdotes, imported empirical findings and the paper's own small exercise have different evidential status. The claim that a useful first assessment can take an afternoon is author judgment, not a measured onboarding or evaluation-time distribution.

Section 5 has thirteen dimension headings: abstraction gradient, closeness of mapping, consistency, diffuseness/terseness, error-proneness, hard mental operations, hidden dependencies, premature commitment, progressive evaluation, role-expressiveness, secondary notation, viscosity, and visibility/juxtaposability. Their intended independence is an analytical aspiration; section 6 acknowledges overlaps and unfinished formalization. This edition supplies no validated aggregate score, factor analysis, learning scale or calibration from a dimension rating to completed-change performance.

| Mechanism and location | Positive contribution and boundary |
| --- | --- |
| Abstraction and domain mapping, §§5.1–5.3 | Reusable abstractions can reduce repeated changes and errors; domain-shaped operations can reduce translation work. They can also raise the knowledge needed to start, force early choices or hide calling context. Prograph's relatively gentle abstraction gradient and LabVIEW's electronics mapping are credited within the inspected versions and activities. |
| Diffuseness, §5.4 | The rocket examples contain 22 Basic lines/140 words, 45 LabVIEW icons plus 59 wires, and 52 Prograph icons plus 79 connectors across eleven windows. Register pairs and system bars have special counting rules. The authors acknowledge imperfect units; screen area, terse code and comprehension do not follow monotonically from these counts. These are not comparable Nu token or LLM-context measurements. |
| Error-proneness and mental operations, §§5.5–5.6 | Avoiding certain textual slips is a plausible editor advantage. The LabVIEW Boolean example connects to earlier observations. The Prograph list-search difficulty is explicitly speculative and unsupported by empirical data in this paper; the Show-and-Tell example is an explanatory analysis. None is a new controlled Nu error-rate result. |
| Dependencies, commitment and evaluation, §§5.7–5.9 | Visible local dataflow helps, while long-range calls and uses can remain hard to find. Browsers and search can help at a navigation cost. Creation order/layout can demand advance decisions. Prograph's partial execution and code/data revision facilities receive positive discussion; this is not a complete live-state, effect-reversal or schema-migration contract. |
| Meaning and informal communication, §§5.10–5.11 | Names, grouping, comments and other informal cues can communicate roles beyond executable semantics. Expert rewiring effort is an anecdote, and the possible benefit of restricting novices' choices is a conjecture. Role-specific knowledge and preparation cannot be inferred from notation alone. |
| Change and access, §§5.12–5.13 | Editing tools materially change the work needed for a local revision. Visibility concerns access to material; hidden dependencies concern access to its relationships. Opening components one at a time and viewing them together are different affordances. Abstraction can reduce local editing while worsening navigation across levels. |

The paper's favorable view of visual programming is retained: domain operations, fewer incidental programming goals and some freedoms of construction can help. Its adverse control-flow, editing and search findings are also retained. The authors report diffuseness as less troublesome than expected. This is a set of conditional trade-offs, not an instruction to favor either visual or textual programming in every task.

## The editing-time result

The straw viscosity test is introduced as **N=1** and described in §5.12, printed p.162, with its appendix on pp.172–174. It adds air resistance proportional to squared velocity to the same rocket example. First, author TG prepares a modified program and a screen dump. An experienced user then receives the original program and the required final printout and is timed editing it into that shape. The method deliberately separates the act of editing from solving the programming problem.

| Version | Reported editing time |
| --- | --- |
| LabVIEW | 508.3 seconds |
| Prograph | 193.6 seconds |
| Basic | 63.3 seconds |

The roughly eightfold extreme ratio is a real reported contrast for this exercise. The explanation concerns moving boxes/rebuilding wires, placing Prograph additions in separate windows, and typing a few Basic lines. The appendix identifies TG's LabVIEW target construction as inexpert; copying a supplied layout is therefore part of the assigned work. The acknowledgments identify Randy Flanagan as the timed experienced LabVIEW user. The complete operator-by-language/expertise matrix is not reported, so a single identical operator across all three versions is not assumed.

The paper does not report repeated trials, randomized order, uncertainty estimates or general task sampling for this exercise. It predicts larger differences on larger programs without testing that extrapolation here. The result is neither an onboarding comparison nor total time to diagnose, design, implement and independently verify a new change. These limitations bound its useful finding; they do not erase it.

One visible correspondence discrepancy remains: Figure 1's specification and the Basic listings use angle **0.3941**, while the illustrated Prograph constant and LabVIEW appendix show **0.3491**. Figure 3 also displays 0.3491. These are differences in the published examples; the original executed programs and their behavior were not verified. Do not silently normalize them, assert an observed runtime defect or discard the editing-time result on that basis.

## Consequences for R07, R20 and the leading studies

Use Cognitive Dimensions as **qualitative, task- and tool-specific mechanism vocabulary**. For a claimed hidden dependency, identify the dependency and available lookup tools; for editing burden, identify the required change and operations; for progressive evaluation, state exactly which incomplete states can be observed. A maintainer's prediction is not observed human cognition or a validated rating.

The [learning and role contract](../../nu-learning-and-role-contract-2026-10-11.md) separates initial adoption from trained productivity, accounts for prerequisites, training failures and specialist assistance, and preserves correct new/retained behavior as an outcome. Giving a final program is legitimate for an editing-only question but would change an independent maintenance-solving question. Common documentation and ordinary tool access belong in the comparison.

The completed S39/S40/S42 and S300/S301 reconstructions retain their own positive, null and adverse evidence, populations, training and denominator limits. S38 does not supersede them or turn comprehension, preference, structural compactness or partial progress into successful maintenance. Historical E/H compactness findings remain intact. Human effects do not become model effects through a shared dimension name, and this reading does not promote R21 steering into the immediate programme.

Section 6 recommends complementing this overview with methods that examine required programming knowledge and detailed editing actions. Two consequential leads are [Bell, Rieman and Lewis's 1991 programming-walkthrough comparison](https://doi.org/10.1145/108844.108846) and [Lewis, Rieman and Bell's 1991 problem-centered design account](https://doi.org/10.1207/s15327051hci0603%264_5). Their methods remain unread here. The exact-title Scite route missed the first work; a shorter title query recovered it. A same-title [2020 chapter](https://doi.org/10.1201/9781003064053-6) is an edition lead with unverified correspondence, not an independent replication. Follow the primary methods before adopting a programming-walkthrough instrument; they are not necessary to label the present prerequisite sheet as an unvalidated design specification.

**Disposition:** the acquired-paper gap is closed. The framework supports task-specific explanations and the editing-only contrast; learning effectiveness, validated measurement and Nu benefit remain separate questions. The next step is a consequential method or role/task dependency, not another generic Cognitive Dimensions summary. No curriculum, participant study, agent run or executable baseline was constructed.
