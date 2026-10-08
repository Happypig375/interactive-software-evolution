# S299 — Local replacement has a behavioral contract

Oliver Biggar, Mohammad Zamani and Iman Shames, *On Modularity in Reactive Control Architectures, with an Application to Formal Verification*, ACM Transactions on Cyber-Physical Systems, 2022. [DOI 10.1145/3511606](https://doi.org/10.1145/3511606); [selected accepted manuscript, arXiv 2008.12515v3](https://arxiv.org/pdf/2008.12515v3).

**Coverage:** all 26 manuscript pages are read textually and visually, including nine figures, two tables, Algorithm 1, both appendices, all displayed proofs and 33 references. The paper supplies formal decomposition and sufficient replacement conditions, illustrated by reported model-checking results. Neither the checker nor an implementation is executed here. The final publisher edition and exact example encoding remain unbound.

## What the structure represents

An action has a behavior function from the current world state to a control signal, and a return-value function on that state (§4). A reactive action-selection mechanism chooses among finitely many actions from the **current input**, without remembering earlier inputs. The world may evolve nondeterministically. Assumption 4.6 nevertheless treats selection computation as negligible: the world remains unchanged while the decision is computed. A sufficiently rapid tick loop can approximate that assumption; arbitrary concurrent changes do not satisfy it automatically.

A decision structure is a single-source directed acyclic graph. Nodes carry actions, and outgoing arcs carry distinct return labels. Selection restarts at the source, follows the arc matching the current node's return, and selects the node's action when no matching arc exists (§5). This is different from an FSM whose current control node persists between decisions. The comparison includes teleo-reactive programs, decision trees, behavior trees and generalized k-BTs. Its BT account includes Sequence/Fallback and action/condition leaves; parallel and decorator nodes are excluded because their concurrency or memory semantics need separate treatment (§3).

Structural equivalence concerns the selection mechanism under arbitrary action assignments and preserves the number of action nodes (§4.2). It is stronger than equality of the concrete behavior of one labeled program. Duplicating a particular action or adding arcs for impossible returns can preserve actual behavior without preserving this structural comparison.

## Modules and the preservation argument

A module is a subgraph with one entry and a constrained exit interface (§6.1): for each return label that leaves the module, every member has an arc with that label either inside the module or to the same outside successor. This permits contracting the module to its derived action, or expanding a node into a module. Theorem 7.1 proves that contraction with the derived action preserves the selected control behavior. Its proof follows the three possibilities: selection bypasses the module, traverses and exits it, or ends inside it (Appendix B.3).

The canonical recursive decomposition, its algorithm and proofs connect this interface to BT/TR/DT structure (§6; Appendices A–B). Module identification has the stated **O(n²k)** bound for n nodes and k labels; recognition of the fixed-label architecture classes has an O(n²) bound. The essential-complexity measure takes the maximum cyclomatic complexity of the decomposition's quotients. k-BTs have value one. This is a structural characterization, not an empirically calibrated maintenance-effort measure.

Theorem 7.3 transfers sufficient conditions for replacing one action to sufficient conditions for replacing a module, using contraction. It does **not** say that every replacement is safe or supply an inexpensive local check for every verification method. The particular LTL scheme then provides such a sufficient condition (Lemma 7.7, p. 16):

- The new action's behavioral model entails the old model.
- For every return label on an outgoing arc, old and new actions return that label under exactly the same world-state conditions.

The resulting controller retains the properties established using those models. Matching every possible return value is unnecessary when a value cannot affect the surrounding graph. A sink module has no outgoing selection context; the example therefore checks behavioral implication without matching its return conditions (§8.3). These are **sufficient, not necessary** conditions: failure of this local check need not mean the changed system violates its specification.

The LTL action model overapproximates possible subsequent world traces (§7.1). Controller selection conditions select the applicable action formula, and the guarantee depends on those formulas and the world assumptions being valid. The proof does not derive accurate action models, intended requirements, environmental fairness or external-effect behavior from the source type system.

## The example preserves both failures and successful changes

The solar-drone example is an illustrative formal controller, not a physical flight experiment (§8). Table 1 represents battery, weather, altitude, light, position, goal availability and successful photography. The specification requires no empty battery while airborne, safe altitude during storms, and eventual photography. World assumptions constrain degradation and initial conditions, and eventually require **permanently** calm weather, bright light and a known goal. The liveness conclusion retains these strong environmental premises.

Using Spot, the authors report that the first structure fails: windy weather can select avoidance while a low battery empties in the air. Checking the battery first still fails eventual mission completion because the drone can remain landed. Adding ascent yields a controller that passes the modeled specification (Figures 1, 7–8). Thus the paper retains adverse designs instead of treating plausible control flow as a correctness verdict.

Two subsequent replacements are checked through their module models. The first matches the relevant success-exit condition and checks implication under the world rules; the second replaces a sink module. The resulting structure has essential complexity one and a corresponding 3-BT representation (Figure 9). This is a concrete account of how a local contract can preserve previously established behavior while the organization changes.

The saving has limits. The smallest module containing a change can be the whole structure, requiring essentially full verification again (Remark 8). The demonstrated replacement modules are not much smaller than the example controller; reduced verification time at larger scale is discussed but no timing or scaling comparison is reported (Remark 9). No developer modification-time, defect-rate or total modeling/integration-cost study is supplied.

Remark 11 also shows why the complexity value cannot stand in for an outcome: arcs for return values that an action never produces can reduce essential complexity without changing the concrete action-selection mechanism. Representation choices therefore affect the metric independently of delivered behavior.

One example-encoding detail remains unresolved. Table 2 prints return predicates that can overlap, such as Photograph's success when `photo` and failure when `not bright or not at`, while the formal action return is a function. The selected manuscript does not state a priority or extra invariant that disambiguates every overlap. No exact machine-readable example was identified in its five PDF links, the selected author publication entry or the bounded artifact search. This limits independent reconstruction of the reported Spot run; it is not a reproduced counterexample to the abstract replacement theorem. Publisher search excerpts expose selected sections, but the attempted `Photograph` lookup returns no match, so they do not resolve the table or establish final-edition equivalence.

## Consequence for the Nu assessment

Preserve the positive formal result: useful reusable local changes are possible when a structural boundary and explicit behavior/exit contracts compose. The relevant comparison is the obligation supplied by that contract, not merely the presence of modules, immutable values or a low complexity score.

For B03/B05/B07/B11/B12, this complements [Ceptre's resource and stage account](S291-S293-ceptre-resources-and-editor.md): local rewrites and stage handoffs differ from an all-traces property-preserving replacement under fixed models. It also complements [S298's interaction typing](S298-interaction-typing.md): data-compatible substitution and configured diagnostics do not themselves establish the behavioral entailment required here. None of these results establishes a Nu-specific maintenance benefit or a general invention priority for Nu.

A credible Nu preservation claim needs its actual state, timing, exit/observer and external-effect assumptions. A credible value claim additionally needs completed-change outcomes and the cost of supplying and checking those assumptions. [S300's reconstructed comprehension/modification study](S300-cognitive-fit-and-modification.md) supplies the separate measurement comparison. Stateful, interruptible BT languages and HFSM decomposition remain conditional follow-ups if the retained Nu claim requires their distinct semantics; an adjacent language proposal alone cannot establish benefit.

## Edition and native evidence

The selected PDF is **552,879 bytes**, SHA256 `2d901fb8aee8bc2ae66f31228dabf882a82894cdef0eb531001554cb9ed1475c`, MD5 `d083ec1dfc4664a0b3cd2bf338a99ecf`. The arXiv history identifies v1 in August 2020 and accepted v3 on 31 January 2022. The file has 26 pages and publisher placeholders; the indexed final journal pagination is 19:1–19:36. They are editions of one work, not separate empirical cases. Extraction contains 133,527 characters; rendered-page inspection resolves the diagrams and formal displays.

Before deliberate reading, the native Zotero 10.0.5 API confirms collection `PKLXQNEE`, parent **`2EZ9ZN3W`** version 6030, note **`EKXHC76L`** version 6031 and sole PDF **`W4QE7G8E`** version 6039. The stored attachment's bytes and hashes match. Final note/parent versions and the considered-source audit belong in the [search ledger](../nu-background-searches-2026-09-30.md). Native records and attachments are preserved; PDFs, extraction, renders and API snapshots remain outside public Git.
