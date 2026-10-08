# S298 — Interaction substitution and the actual checking boundary

Arnaud Blouin, *A Type System for Flexible User Interactions Handling*, PACM HCI 8 (EICS), 2024, pp. 1–27. [DOI 10.1145/3660248](https://doi.org/10.1145/3660248); [selected HAL v2 author manuscript](https://inria.hal.science/hal-04485762v2/document).

**Coverage:** all 28 PDF pages are read textually and visually: one HAL cover and 27 manuscript pages, all three figures, two tables, seventeen numbered listings, unnumbered code/formal displays, nine footnotes and 37 references. Ten selected companion/source files are read completely without executing them. This establishes a concrete substitution/composition mechanism and a bounded diagnostic implementation, not a measured maintenance advantage or an independently reproduced system.

## What changes while handling code is reused

An interaction consists of behavior and the data it exposes (§3). Families group interactions with related data. Replacing mouse drag-and-drop with reciprocal drag-and-drop permits the handling code to remain unchanged when both expose the same data type and clients operate on that data. This is **total substitution**. Replacing a mouse interaction with touch is partial: shared coordinates remain available, but device-specific uses, such as a left-mouse-button predicate, need adaptation (§§3.1–3.2; Listings 8–9, 14).

The union operator selects between interactions and exposes a union of their data. Sequential composition combines their data; cancellation retains the main interaction's data type while another interaction can cancel its execution (§§3.3–3.4). These operations supply useful reusable structure. They do not automatically determine the intended new behavior or compensate arbitrary external effects.

In the TypeScript Interacto implementation, a binder selects an interaction and configures the command produced from it. Start, update and end/cancel callbacks support a drawing example. During an interaction, the **same data object is updated and then cleared when the interaction ends** (§4.1.1). This is a mutable interaction-data contract, not immutable world history, live schema migration or arbitrary state restoration. The Angular SVG example is an implemented demonstration; it is not a comparative developer study.

## Data typing and conflict detection are different feedback

The host compiler infers the exposed data types. The proposed additional rules detect equal interaction types, equal data families, or full/partial behavioral inclusion on related widgets (§3.5). The paper considers event bubbling, shared/ancestor widgets, timing parameters and configurable ignore/warn/error severity. Legitimate combinations can trigger warnings: Table 2's same-data rule rejects opposite swipes or horizontal/vertical pans even where their behaviors are intended to coexist.

The implementation discussion explicitly places these checks **at system startup as dynamic analyses** (§4.1.1, manuscript p. 18), despite compile-time language earlier in the paper and Listing 17's static-analysis caption. Bindings with a `when` predicate are excluded; a lack of warning on them is not evidence that their predicates or commands were proved compatible. Partial behavioral inclusion uses hand-coded knowledge of the supported interactions. Timing-dependent overlap requires access to runtime parameter values (§4.2.2).

Table 2 contains eighteen illustrative rows, including the click/double-click pair twice. It is a representative decision discussion, not measured precision/recall over an independently labeled corpus. The soundness discussion depends on the host language and recognizers matching their declared interaction types. It acknowledges TypeScript casts, assumes `any` disabled, and offers wrappers/lint rules to restrict unsafe uses (§4.2). It does not supply a general soundness proof, verify arbitrary recognizer implementations, or derive behavioral disjointness solely from data shape.

## The companion release narrows the implementation claim

The printed companion URL does not yield a page through the web tool. The repository's actual EICS2024 directory is accessible through its public tree/API. Its [README at `ac8cd439a9dab73803213044d614296cb94d5f2d`](https://github.com/interacto/research/blob/ac8cd439a9dab73803213044d614296cb94d5f2d/EICS2024/README.md) points to **Interacto v8.0.0** and Angular-example v8.16.0. The paper says it extends Interacto 7.4.0; that is the library version, not a TypeScript compiler version. These are not interchangeable snapshots.

The bounded inspection reads the README and both Scala files, v7.4.0's package and binding observer, and v8.0.0's package, checker interface/implementation, binding observer and checker test file. The release commits are `972b70a14864c2b944d280ca2fdbe10739bff456` and `b85631e0355900d235159715ef3e71ed90c08759`. Private manifests preserve exact paths, bytes and SHA256 hashes. The public recursive trees return 372 research, 322 v7.4.0 and 385 v8.0.0 entries without truncation; this inventory is not a whole-repository reading.

The [v8.0.0 checker](https://github.com/interacto/interacto-ts/blob/b85631e0355900d235159715ef3e71ed90c08759/src/impl/checker/CheckerImpl.ts) establishes several narrower facts:

- All three global rule severities initially equal `ignore`. The binding observer invokes checking when a new binding is registered; this is runtime registration feedback and requires appropriate enabling/configuration.
- Same-interaction checks compare names; same-data checks compare data-object constructors. Both bindings are excluded when either has a `when` predicate. The seven authored tests inspect same-interaction/configuration/predicate cases; they are read, not run.
- Widget overlap uses direct set intersection. This selected implementation does not perform the paper's broader ancestor/bubbling analysis in that predicate.
- Inclusion is a symmetric lookup in a fixed name map. This selected path does not inspect timer values or recursively analyze composed interaction behavior. Its comments mention OR support, but the inspected predicates do not split OR names.

Listing 17's printed candidate-filter predicate lacks the negation on `isWhenDefined` that both the surrounding prose and released implementation use. The source therefore helps resolve the intended exclusion policy. It does not establish that the v8.0.0 tag is the exact build behind every later manuscript example. The Scala companion is illustrative type scaffolding: its binding methods return `this`, and its base interaction never starts. It is not a second implemented event-processing engine.

These are static, version-specific findings. No current-release defect, executed test failure, complete recognizer audit or failure rate is inferred. The Angular example, generated API pages and complete framework are not inspected or run. A stronger claim about the exact demonstrated runtime would need that version binding; the narrower substitution/feedback comparison can already be stated.

## Evidence disposition and consequence for Nu

Preserve the positive result: a mainstream typed API can separate interaction recognition from data handling, reuse handling code across selected substitutions, compose interactions and provide targeted conflict warnings. The paper also identifies real integration obligations: interaction objects, behavior/data separation, family design, commands, API changes and suitable host types (§4.3). Dynamically inferred gestures/input uncertainty are outside its implemented scope; VR is future work.

No controlled user comparison, completed-change timing, delivered-defect rate, diagnostic accuracy or total integration/runtime-cost estimate is reported. This limits an effect claim without erasing the demonstrated capability. General novelty relative to the original introduction of a Nu feature is not established by this later publication.

For B02/B03/B07/B08/B12, distinguish **data compatibility, the opportunity to receive a diagnostic, actual conflict coverage, and intended behavior after the change**. Compare Nu with the configured workflow and recognizer/host obligations actually supplied. A type-correct substitution can be useful without proving the new interaction is semantically appropriate; a successful startup with disabled or excluded checks is not a behavioral oracle. No experiment or new adapter is authorized by this reading.

## Edition and native evidence

The selected HAL file is **952,887 bytes**, SHA256 `59ab09777c9e889a7b1ed431db1c92c65cec39f5376131d9c3a3c4c9b131883c`, MD5 `89e8a7a385d68103cfa48609a992fdbb`. Its cover records deposition on 29 March 2024; the manuscript has March/volume-1 placeholders and an unfinished DOI. Crossref gives the final June 2024 identity. Publisher PDF access returns 403, so final-edition textual equivalence is unverified. Later PDF creation metadata is not a new study date.

Collection/global DOI and title checks precede native registration and deliberate reading. Parent **`8CBXX42A`**, note **`5QQSLPWT`**, PDF **`MTEZ2FQ3`** belong to collection `PKLXQNEE`. The PDF's version6037 and exact bytes/hashes verify. Extraction contains 91,267 characters; extraction alone did not determine completion. Final parent/note versions and the considered-source audit are recorded in the [search ledger](../nu-background-searches-2026-09-30.md). Copyrighted bodies, extracted text, renders and raw API/source snapshots remain outside public Git.
