# S296–S297 — State exploration and live replay in game development

**S296:** Rokas Volkovas, Michael Fairbank, John R. Woodward and Simon Lucas, *Practical Game Design Tool: State Explorer*, IEEE Conference on Games 2020. [DOI 10.1109/COG47356.2020.9231863](https://doi.org/10.1109/COG47356.2020.9231863), [conference-hosted paper](https://ieee-cog.org/2020/papers/paper_156.pdf).

**S297:** Andrew R. Martin and Simon Colton, *Towards Liveness in Game Development*, IEEE Conference on Games 2019. [DOI 10.1109/CIG.2019.8848092](https://doi.org/10.1109/CIG.2019.8848092), [conference-hosted paper](https://ieee-cog.org/2019/papers/paper_229.pdf).

**Disposition:** both selected main papers are completely read, textually and visually: S296 has eight pages, nine figures, one pseudocode listing, one footnote and ten references; S297 has four pages, three figures and seventeen references. Neither supplies an appendix, numerical results table or linked implementation artifact for the described tool. No game, author code, benchmark or experiment is executed. These are two publications with different mechanisms and evidence scopes, not two controlled demonstrations of a Nu effect.

## S296: finding relevant states in existing game code

State Explorer is a Godot editor plugin implemented in GDScript. It instantiates a root object and repeatedly copies and modifies represented game state. The designer supplies possible actions, a predicate deciding which transitions are relevant, and a visualization as text or pixels. The interface displays the current state and reachable relevant states. Selecting one makes it current and starts another exploration (§III, Figures 2–4).

Listing 1 describes a modified breadth-first search: skip previously seen states, retain newly relevant states, and queue the remaining successors. It continues after finding one relevant state but **does not expand a relevant state in that search**. The result is therefore a frontier defined by the designer's predicate, not a claim that every subsequent state has been examined. The paper does not specify the implementation of its state-equality/copying machinery sufficiently to certify arbitrary host objects or side effects.

The designer can further restrict the returned actions or the state variables used to distinguish changes. These choices make a query practical and determine what it can answer. **Consequence inferred from the method:** a negative reachability result over a restricted action/state representation does not establish absence in the whole game without justifying that restriction. An observable state or useful diagram also does not provide the intended correctness criterion automatically.

The paper reports three small demonstrations (§IV). In Tic Tac Toe, the tool reveals an unintended move that places a circle over an existing cross, missed during the described manual play-test. In Sokoban, it finds relevant box-push states and supplies undo without requiring undo logic in the game. In Breakout, tracking the ball while ignoring different paddle positions makes a selected query run within roughly 2,000 states and under 2 seconds after saving code. Preserve these concrete positives. The last figure is a selected, guided query observation, not a general throughput bound, frame-latency distribution or measured developer-time effect.

## S296: useful iteration and substantial integration work

The authors then use the tool while developing *Eternower*, a small commercial tower-defense game (§§V–VI). The genre, mazing and upgrade-path concepts already exist when the selected evaluation starts. Reported uses include examining reachable enemy-health values, tower-placement effects on path length, and resolving levels without waiting through their animations. The stated minimum 60 steps at 0.3 seconds each accounts for 18 seconds of animation per ordinary level check. Skipping that wait is a concrete mechanism; the paper does not measure complete end-to-end savings after search, interpretation, tool construction and integration costs.

Late integration is explicitly difficult. Mechanics and visual state are spread across files and share sprite positions. The authors report that including animation data increases the tracked data by at least tenfold, and that separating mechanics takes considerable time. They move damage, path and player-state logic into separate objects with no dependencies on other game systems, then reconnect the visual interface and reuse it for State Explorer. Thus the reported usefulness depends on an intentional boundary around the game mechanics.

This is valuable experience rather than an assigned comparison: one developer's roughly three-month project and three small demonstrations do not provide independent replications, a representative industry sample or a causal maintenance estimate. The authors judge the tool particularly useful for verification-oriented questions, while warning that poor integration can cost more than obtaining the information manually. Retain both outcomes.

For Nu, the consequential comparison is whether its organization and tools make the relevant mechanics easier to isolate, observe and revisit at lower total cost. State navigation and undo can be supplied inside another engine through an explicit state/action interface. Their availability alone does not establish a distinctive Nu advantage; conversely, the reported isolation burden gives a concrete cost that a later authorized comparison could examine.

## S297: replay reconstructs state after an edit

S297 distinguishes exploratory REPL changes, edits to an already-running program, dependency-driven recomputation and reactive GUI components (§II). Its example of changing enemy-size code is useful: existing enemies may retain old sizes while new enemies use the new value. The desired relationship between a code edit and an existing run needs an explicit policy.

The implemented demonstration uses a small imperative language and a text-based prototype with two modules (§III-D). The controller initializes the game component and logs events, including periodic ticks that drive update and rendering. After a game-code change, it discards the component, initializes a new one and rapidly replays **all recorded events**. Figure 3 illustrates a changed Tetris-like piece shape affecting the replayed history.

This reconstructs behavior from the beginning under the changed program and retained event sequence. It is distinct from preserving the old current state through an arbitrary edit, migrating pending continuations, or proving that the resulting play is intended. The paper supplies no general treatment of unlogged clocks, randomness, external effects or resource handles. Those boundaries matter if the mechanism is transferred to a larger game.

The prototype also needlessly replays the entire event log when only rendering changes. The proposed node graph would separate dependencies so that such changes could trigger less work. Do not credit that planned optimization to the demonstrated controller.

## S297: proposed ownership discipline and unfinished interface

The proposed reactive model processes discrete event streams with push/pull evaluation. Nodes may own mutable state. To avoid dependencies hidden in shared mutation, mutable state is not shared between nodes; downstream nodes may borrow and re-export immutable references but may not store them. The authors intend language semantics and types to enforce this discipline (§III-A). This is an alternative design to making all represented data immutable, not a formalized or benchmark-validated guarantee in this paper.

The planned interface combines textual game logic with a visual graph for feedback, asset processing and custom GUI nodes. Figure 2's pixel-editor/timeline interface is explicitly **hypothetical**; Figure 1 reproduces Bret Victor's earlier demonstration. The implemented state is the language and text-based Tetris-like replay prototype. Node GUI construction, further demonstrations, formalization and comparison with other tools are future work (§IV).

The paper argues for productivity, creativity and enjoyment benefits, but reports no user study, comparative timing, allocation profile or numerical scalability result. Its claims about persistent-structure performance motivate the design; they are not measured costs of Nu or of the proposed ownership alternative. For today's comparison, retain the useful replay policy and concrete prototype while separating them from the proposed full environment.

## Combined consequence

| Question | S296 State Explorer | S297 liveness prototype |
| --- | --- | --- |
| What is retained or reconstructed? | Represented state copies and transitions from a selected root/current state. | An event log; game state is rebuilt from initialization after a code edit. |
| What determines observation? | Supplied actions, tracked variables, relevance predicate and visualization. | Logged inputs/ticks and the current initialization/update/render behavior. |
| What useful outcome is reported? | A found implementation flaw, undo, guided queries and selected commercial-game iteration uses. | A working hot-reload/replay demonstration that changes a piece across the recorded play. |
| What work remains part of the cost? | Mechanics isolation, adapters, query policy, visualization, copying/search and interpretation. | Complete input capture, replay/rebuild work and implementation of the proposed graph/interface. |

These methods make the Nu question more precise: what representation and workflow reduce the work needed to obtain trustworthy feedback for a consequential change? A useful observer, a retained value, a replayed run and a complete temporal oracle remain different capabilities. The literature supplies comparators and reported outcomes; Nu-specific advantage remains unmeasured. Publication dates alone do not establish priority relative to the original introduction of a Nu feature.

## Exact acquisition, coverage and native records

S296's conference file returns 200: **963,499 bytes**, SHA256 `d1b443dfbb395721af41c1658da17dfa759acf23b440a21adcd7ca4ee20aeaa8`, MD5 `159ed232cc7bc63a7954989441bbdc61`. Its pages are internally numbered 1–8; bibliographic discovery records use proceedings pages 439–446. The Essex institutional copy is located but its ordinary GET times out, so byte correspondence is unverified. Crossref returns 429 for S296; no retry is made. The conference title page verifies all four authors, whereas Scite displays three. Final publisher bytes are not compared.

S297's conference file returns 200: **1,419,305 bytes**, SHA256 `e1e70e52d0d303941baaf9ca7ffb134d4724f0e273dbccde60920bebee5968ad`, MD5 `4eba4abce17390f0c8a24bf77003c0b0`. Crossref returns 200 with the two authors, August 2019 and pages 1–4; the [Monash record](https://research.monash.edu/en/publications/towards-liveness-in-game-development/) gives proceedings pages 186–189. These are pagination descriptions of the same four-page work, not separate studies. The conference file carries the 2019 imprint; final publisher byte identity remains unverified.

All eight/four original pages are read textually and visually, including every figure, reference and S296's listing/footnote. Private text extraction contains 40,627/21,228 characters respectively; Poppler layout extraction and page images support the reading. Neither acquisition nor complete reading constitutes tool execution or independent reproduction.

Collection `PKLXQNEE` and global DOI/title checks initially find no exact records among 325 collection parents. Before deliberate full-paper reading, S296 is registered as parent **`C8K9CW2D`**, note **`GYEK5AJA`**, PDF **`V22K85RY`**; S297 as **`Z98DZFSU`**, **`E9649V6A`**, **`LMLBURNB`**. Discovery had already supplied incidental primary excerpts; those are not backdated as complete readings. Attachment bytes/hashes and memberships verify. Final canonical-note/object versions are recorded in the search ledger. PDFs, extracted bodies, renders and native snapshots remain ignored by Git.

**Considered-source audit:** 109 occurrences normalize to 81 units: two credited, 60 deferred and 19 unused. Of 12 historical matches across 181 prior files, two receive material updates and ten unchanged decisions are withheld. Answer `nu_background_s296_s297_20261008` records 71 decisions: two credited, 51 deferred and 18 unused, with two full-text and 69 title/abstract/reference-context stages. Receipt and `citation_report` match every membership/decision and all 426 compared fields. There are no skipped records, missing reasons, linkage warnings or truncated lists; answer-scoped retrieved count is null. Provenance is 30 other, 31 Scite and ten web records. Conditional leads are excluded from this segment's evidence, not adjudged absent or invalid. No incoming citation graph or new Consensus query is claimed.

The selected C01 state-exploration and live-replay gaps are resolved at these publication scopes. The remaining broader discovery ranges, inaccessible generation/corpus methods, exact-edition gaps and conditional positive user-study leads retain their own dispositions. No experiment, extra worker, new adapter or access purchase follows.
