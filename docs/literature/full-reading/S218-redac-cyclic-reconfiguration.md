# S218 — ReDAC: cyclic calls, quiescence and measured costs

**Identity:** Andreas Rasche and Andreas Polze, *ReDAC — Dynamic Reconfiguration of Distributed Component-Based Applications with Cyclic Dependencies*, *11th IEEE Symposium on Object Oriented Real-Time Distributed Computing (ISORC 2008)*, pp. 322–330, DOI [10.1109/ISORC.2008.44](https://doi.org/10.1109/ISORC.2008.44). Crossref, DBLP, the authors' HPI publication list, and the IEEE publisher PDF agree on the work and edition. S187 reference 115 and its roster row 61 provide the discovery route.

## Coverage and edition reconciliation

**2026-10-15: complete original publisher-PDF reading, including every visual.** Before reading, the native Zotero objects were revalidated read-only: conference-paper parent **`LPNN8V3S` v5162**, stored-file attachment **`YX86LULR` v5200** under that parent, and access note **`SZJVQTUY` v7061**, all in collection `PKLXQNEE`. The PDF is the nine-page IEEE proceedings article with printed pages 322–330. It is 594,772 bytes, SHA-256 `138de100af67a9b8ef50a976b43e711245ab56f93c6891322ad789e445e6b195`, and MD5 `cb2ad83af94f68891758ac5ff32410e5`. Its first page prints the exact title, authors, proceedings heading, page 322, and DOI.

The full text of PDF pages 1–9 was read from title through all 15 references. `pdftotext -layout` returned 70,804 characters and page boundaries for all nine pages. The extractor emitted a missing-Symbol-font warning and mangled some mathematical symbols and plot labels, so no formula, algorithm predicate, or chart reading relies on extraction alone. All nine pages were rendered at 180 DPI and inspected. Higher-resolution crops were used for the Petri net and its printed values (400/600 DPI) and the blackout histogram (400 DPI). The visual coverage includes Figures 1–7, Algorithms 1–4, equations (1)–(3), the implementation listing, timing table, publisher headers/footers, and bibliography. The private reading receipt is `.artifacts/s218-reading-20261015/verification.json`.

This closes the original-PDF and visual gap. It does not add a separate study: the 2026-10-02 work was a complete text reconstruction of this same article from ResearchGate's returned text. That earlier reading remains the provenance for the initial synthesis, while the current pass supplies publisher-copy correspondence and visual evidence. No source code, raw timing data, TimeNET model file, supplement, or executable artifact was supplied or run. No model checking or runtime reproduction is claimed.

### Preserved 2026-10-02 access history

The earlier reading registered parent `LPNN8V3S` and note `SZJVQTUY` before using the author-uploaded ResearchGate text. It covered numbered pages 1–9, sections 1–9, four algorithms, three displayed equations, the timing table, and extracted text/captions for seven figures, but it had no verified PDF bytes or visual coverage. The HPI-linked ResearchGate PDF routes returned HTTP 403; the old HPI/DCL route returned 404; CiteSeerX's indexed and redirected document routes returned 404; the ordinary IEEE PDF route returned 418; and Scite returned `contentDenied`. Those route results remain historical access evidence rather than evidence about the article's contents.

Three ignored extraction snapshots preserved the returned text windows:

| Returned line window | Bytes | SHA-256 |
| --- | ---: | --- |
| 77–940 | 28,545 | `6f0e5cb9e1bd54428dcc8c9c2d67e5385e6dc0312c903020a1b04bfde0f0e889` |
| 669–1450 | 25,004 | `6372e66874c02cd37396edcc9195961b54f8bdd681bb4e4b7043cc3ce6f23a52` |
| 1297–1877 | 26,717 | `9bba020cc44a470e9304cd1d21c25ed72e1a5461de8e0410c98a836ff3ba60e1` |

The paper ended at returned line 1798; later citation-card text was not treated as part of the body. The snapshots were overlapping text windows, not an independent edition.

### Comparison with the old text reconstruction

The original PDF confirms the old reconstruction's section order, capsule/root model, cyclic-call example, four algorithms, implementation race handling, shared-resource extension, evaluation setup, all five timing rows, blackout setup and range, two application reports, and 15-entry bibliography. The reported numerical results in the old note require no correction.

Two text-level corrections and several visual additions matter:

- On printed p. 328, the publisher text says progress and absence of deadlock were **evaluated** using the invariants and that progress was **analysed** from positive occupancy. The ResearchGate extraction said “proved/proven” in the corresponding sentences. The stronger extraction wording should not be used. The publisher text does separately say on p. 327 that mutual exclusion was “proven by the invariant.”
- On printed p. 329, the publisher text says “Most values are below 300 µs”; the old extraction said “Most measurements can be found below 300 µs.” The empirical scope is unchanged.
- The diagrams now establish the exact cycle, thread paths, counter examples, shared-lock sequence, Petri-net markings, and histogram shape described below. The earlier note did not claim these visual facts.
- The publisher prose immediately before Algorithm 4 says `blockEnd` is set to true, but Algorithm 4 line 4 sets each capsule's `BlockMode` to true; the later prose and release signal use `blockEnd` as an event. This appears to be an internal naming slip. The reconstruction follows the algorithm.

## Mechanism reconstructed from the original

Sections 3–5 make a deployment component into a runtime **capsule**: an object graph with designated root objects. Every thread must enter the capsule through a guarded root method; inter-capsule references and logical thread identities are part of the application model. A cross-capsule transaction here is a single synchronous method invocation, possibly with nested or re-entrant calls. It is not a model of every asynchronous task, external effect, or durable application transaction.

Updating a chosen block-set requires its active invocations to drain so that live state does not remain on stacks, in registers, or in transit. Blocking every connection immediately can deadlock a cyclic call that must re-enter an affected capsule before returning. ReDAC instead maintains each capsule's count of active calls per logical thread. A thread already active somewhere in the block-set may continue nested calls; a thread with no active call there waits. Normal entry increments its count and exit decrements it. Once every relevant count reaches zero, the reconfiguration thread may act and then release waiting threads.

The printed algorithms make the synchronization obligations explicit:

1. `ActiveThreadOnBlockSet` scans every capsule in the block-set and returns true if any logical-thread counter is positive.
2. Before a root-object call, a thread in block mode signals quiescence if no active thread remains, then waits on `blockEnd` only if its own logical ID has no positive counter anywhere in the block-set; otherwise it may continue. Entry then increments its per-capsule counter.
3. After a root-object call, exit decrements the counter and signals `quiescenceReached` if that decrement removed the final active call during block mode.
4. A reconfiguration request resets both events, sets `BlockMode` for every capsule, waits if any call is active, performs the unspecified reconfiguration actions, clears `BlockMode`, and signals `blockEnd`.

The C#-like implementation excerpt on printed p. 329 adds details absent from the pseudocode. It snapshots `initialBlockMode`, serializes the quiescence check under `globalLock`, snapshots and increments a reconfiguration generation counter (`reconfNr`), and retries if either the mode or generation changed. After incrementing the call counter it checks whether block mode changed between the initial test and increment; if so, it rolls back the increment and retries. These are material concurrency obligations. The paper does not verify distributed memory, process failure, or communication behavior.

A further example shows that shared locks can still deadlock the basic protocol. A thread outside the block-set can hold a resource needed by an active thread inside it and then itself be stopped at entry. The proposed extension includes every capsule on a path between members of the block-set. This is a concrete obligation on dependency analysis, not a demonstrated bound for arbitrary synchronization patterns.

The mechanism establishes a place to apply reconfiguration. Section 6 delegates update operations and object-graph state transfer to earlier work. Drained invocations do not prove that a new representation preserves application invariants, that identities and resources survive transfer, or that an urgent replacement has the desired behavior. The introduction's three requirements—structural integrity, mutually consistent capsule states, and application invariants—remain distinct obligations.

## Visual reconstruction from the original pages

- **Figure 1, printed p. 324 / PDF p. 3:** a rounded capsule boundary contains an object graph with multiple marked root objects. Dashed external references enter roots, application threads enter roots from below, and internal solid references connect ordinary objects and primitive fields. This visually supports the interception boundary; it does not show an enforcement mechanism for arbitrary references.
- **Figure 2, printed p. 325 / PDF p. 4:** `K1` and `K2` are in the block-set and `K3` is outside it. Directed calls form the `K1 → K2 → K3 → K1` cycle. Thread `ID1` already spans the cycle; blocking its return into `K1` prevents it from unwinding, while `ID2` enters at `K3` and has no active call in the block-set. The red cross marks the problematic blocked re-entry.
- **Figure 3, printed p. 326 / PDF p. 5:** the example counter tables are `K1={ID1:2, ID2:1}`, `K2={ID1:1}`, and `K3={ID1:1, ID2:1}`. The visual makes clear that counters are per logical thread and per capsule, and may exceed one under re-entry.
- **Figure 4, printed p. 327 / PDF p. 6:** `K2` and `K3` are the block-set; `K1` lies between them and owns shared resource `R`. The numbered sequence shows `ID1` enter `K1`, lock `R`, and start a call to `K2`; after a context switch, `ID2` enters through `K3`, calls `K1`, and waits for `R`; blocking `ID1` at `K2` completes the deadlock. Including intervening `K1` in the expanded block-set addresses this pictured case.
- **Figure 5, printed p. 328 / PDF p. 7:** the one-capsule Petri net visibly separates an upper application loop from lower reconfiguration logic. Initial markings are shown at `Thread1Start`, `NoBlock`, `ReconfThreadStart`, and three tokens in `RecursionPool`; `InMethod` and `Reconfiguration` are highlighted as the mutually exclusive places. The net includes counter-zero/positive tests, quiescence set/wait paths, active/no-active-thread branches, and block-end set/wait paths. Printed analysis values are `MutualExclusion = 0.0`, `ProgressReconfiguration = 0.1381689`, and `ProgressApplication = 0.0886657`. These values document this displayed model; they do not expose the full reachability graph or verify every drawn arc independently.
- **Figure 6, printed p. 329 / PDF p. 8:** the 26-line implementation listing confirms the mode snapshot, global lock, generation check, blocking decision, counter increment, race recheck/rollback, target invocation, and decrement summarized above.
- **Figure 7, printed p. 329 / PDF p. 8:** the histogram is strongly right-skewed. Its tallest bar is near 80 µs at roughly 0.27 of observations, with secondary bars around 140–160 µs at about 0.15 each and a sparse tail extending toward 400 µs. The plot gives no exact raw bin counts, so these visual heights are approximate; the textual claims of 80–400 µs and most values below 300 µs remain the exact reported statements.

## What the evaluation establishes

Section 7 reports a .NET Framework 2.0 implementation on Windows XP SP2, a 2.8 GHz Intel Xeon with one active core, and 2 GB RAM. Timings use the x86 CPU tick counter (`rdtsc`). Each row reports the mean and standard deviation for batches of 1,000 invocations over 1,000 separate measurements:

| Invocation | Reported duration for 1,000 calls |
| --- | ---: |
| Interface method call | 5.96 ± 0.14 µs |
| `Reflection.Invoke` | 5.05 ± 0.21 ms |
| .NET Remoting call | 346.92 ± 2.11 ms |
| ReDAC | 151.68 ± 2.09 µs |
| Reader–writer-lock synchronization | 324.19 ± 4.28 µs |

Arithmetic on the printed means gives **145.72 ns additional time per guarded call** relative to the interface baseline, about **25.45 times that tiny baseline duration**. ReDAC uses **46.79% of the reader–writer-lock batch time**, a reduction of about **53.21%**. These are derived comparisons, not new observations. Reflection and remoting are different invocation mechanisms, so the table is not a matched comparison of complete applications implementing the same distributed update obligations.

The authors argue that only a small share of calls cross capsule roots and useful method bodies take much longer. Those claims explain how the absolute overhead might be small in an application; this paper does not report a measured root-call fraction or whole-application slowdown for Nu. Its “order of magnitude faster” conclusion refers to the earlier 2003 approach, not the roughly twofold reader–writer-lock contrast in this table.

The blackout experiment covers 500 reconfigurations of randomly generated configurations with 20 capsules, 10 threads, and maximum call depth 20. Methods perform only a few arithmetic operations to expose protocol cost. The exact textual result is 80–400 µs, mostly below 300 µs. Waiting for long methods, blocking I/O, state conversion, rendering, and recovery can change application interruption time; this is neither a worst-case bound nor a complete urgent-update latency.

Section 8 reports successful dynamic updating of PaintDotNet, described as exceeding 133,000 lines of code, with no overhead noticed during use. It also describes replacing faulty controllers in a Distributed Control Lab. No human participants, task assignment, controlled responsiveness measurement, exact change roster, or recovery denominator is reported. **S187's compressed no-overhead entry therefore remains a scoped experience report, not literal zero measured cost.**

## Formal and transfer boundaries

The displayed TimeNET model contains one capsule and one recursively calling application thread; recursion depth is set by initial tokens in `RecursionPool`. Equation (1), `P{#InMethod + #Reconfiguration > 1} = 0`, states zero probability of simultaneous application-method and reconfiguration occupancy. Equations (2) and (3), `E{#InMethod} > 0` and `E{#Reconfiguration} > 0`, are used to argue application and reconfiguration progress through positive expected occupancy. More complex configurations are mentioned but not shown.

The original visual strengthens the record of what was modeled and exposes the three printed stationary-analysis values. It does not turn the reported analysis into a checked proof for every distributed topology, schedule, resource dependency, or fault. The model file and TimeNET version/configuration are absent, and no rerun was performed.

For B04/B08/B10, ReDAC supplies a constructive cyclic-call alternative to global stopping, with explicit root boundaries, logical-thread tracking, synchronization, and update-set obligations. For B06, its favorable lock comparison and small absolute guarded-call cost coexist with positive overhead and a narrow blackout workload. For B05, PaintDotNet is an interactive-application lead, not game-loop or rendering evidence. For B12, invocation timing, a scoped model analysis, and application experience remain separate evidence units. None establishes Nu-specific novelty, human benefit, or correctness of future F# changes.

Reference 10 is now covered by the completed [S219 reading](S219-gui-updates-access.md): **Rasche and Schult, *Dynamic Updates of Graphical Components in the .NET Framework*, SAKS 2007, pp. 219–230**. S219 reconstructs assembly-directed object-graph replacement, alias/cycle memoization, delegate repair, Windows Forms reconciliation, and the retained native-proxy boundary; it also records an exact `Delegate.Combine` versus official `CreateDelegate` API mismatch without inferring an executed failure. This resolves S218's selected state-transfer reading dependency while keeping the papers' evidence separate: S218 establishes quiescence and measured root-call cost, whereas S219 supplies an unmeasured migration design with correspondence, resource, deferred-installation, and recovery gaps. This S218 pass did not execute code, a runtime, or a model checker.
