# Prioritized agenda for investigating Nu value

**Assignment, 2026-10-08:** prepare the plausible research directions together, prioritize them by research value, and continue literature work when it can change a question, comparison or interpretation. This replaces the immediate requirement to choose only one direction before further preparation. It does not select a favorable answer or reopen experimental execution.

The central question is **when Nu's combination of representations, coordination, history and development tools changes the cost and correctness of real software evolution**. The highest-value result would identify useful conditions of benefit and their costs, including conditions where a credible alternative works better. Whole-package value, the MMCC/ImSim choice and a source convention such as D1 answer different questions. They belong in one agenda with separate comparisons.

This agenda covers **21 currently plausible directions**, including less mature extensions and the user-added R21 steering question. It is a revisable map, not a claim that every possible idea has been enumerated or a commitment to run 21 studies. [PLAN](../PLAN.md) owns authority. The [B01–B12 survey](literature/nu-background-survey-2026-09-30.md), [reading index](literature/full-reading/INDEX.md) and [search ledger](literature/nu-background-searches-2026-09-30.md) retain source coverage and gaps.

**Implemented continuation:** the [saved plan](nu-research-continuation-plan-2026-10-08.md) and [six detailed designs](nu-research-study-designs-2026-10-08.md) prioritize **mechanisms/costs plus bounded agent maintenance**. Human-steered development is the intended practical context; its anticipated 2027 importance is a planning assumption, not a measured forecast. Steering effectiveness is deferred pending measurement and participant-design work. Human-only and agent-only extremes remain optional reference cases; the near-term packet does not require three equal workflow arms. Source-grounded task diversity and counterexamples address the user's convergence concern without claiming that prompts or repeated AI outputs establish independent thinking.

## How the priorities are chosen

Priority is an ordinal research judgment, not an estimated effect size or a computed score. It considers:

- **Decision value:** who could make a consequential development, tooling or adoption decision from the answer?
- **Connection to Nu:** does an inspected capability motivate the question, or would the study first require an unverified new capability?
- **Unresolved knowledge:** what would be learned beyond the closest existing method or comparison? A Nu port or a low publication count alone is insufficient.
- **Discrimination:** can credible alternatives, meaningful outcomes and rival explanations be distinguished? Useful nulls, adverse findings and crossovers count as valuable answers.
- **Evidence cost and transfer:** what preparation, source access, participants, engineering and replication would be needed, and how narrowly would the answer apply?

Research value and order of execution are different. R01 has the greatest direct adoption value but depends on a defensible workload and measurement boundary. R02/R03 may offer a smaller first comparison after separately authorized feasibility. R05/R06 and R14 supply measurement and practice foundations early, even when their standalone contribution is less distinctive. Order within a band is provisional; a missing comparator, a close duplicate or a real stakeholder decision can change it.

## Ranked directions

| Rank / ID | Priority | Question | Decision or knowledge gained |
| --- | --- | --- | --- |
| 1 / R01 | A | Does the complete Nu development workflow provide net value against a credible alternative? | Whether and for which work a developer should adopt the package. |
| 2 / R02 | A | How do ownership and coordination choices affect local versus coordinated changes? | When to choose MMCC, ImSim or another justified organization within Nu. |
| 3 / R03 | A | When do retained history and state inspection improve debugging and recovery? | Which failure situations justify the tooling and retention cost. |
| 4 / R04 | A | Do explicit domain representations help complete evolving behavior? | When type/domain modeling or explicit-case conventions repay their cost. |
| 5 / R05 | A, enabling | What evidence warrants a claim of correct interactive-software change? | A defensible outcome/oracle for the other directions; possibly a reusable evaluation method. |
| 6 / R06 | A, enabling | What runtime and development costs accompany Nu's state/coordination choices? | The workload boundary at which an otherwise useful workflow becomes too expensive. |
| 7 / R07 | B | How do learning, comprehension and prior experience affect productive use? | Training and onboarding decisions, with performance separated from preference. |
| 8 / R08 | B | Which Nu representations and tools help coding agents, and under what information policy? | A concrete agent maintenance workflow, without inferring an effect from human results. |
| 9 / R09 | B | Do benefits survive sequences of changes and accumulated requirements? | Whether a short-task gain persists through maintenance and handoff. |
| 10 / R10 | B | Which live edits and schema changes can preserve useful state and continuation? | When live development saves restart/reconstruction work safely. |
| 11 / R11 | B | How does the workflow affect collaborative editing, merging and cross-role handoff? | Team-level value and where work moves between participants. |
| 12 / R12 | B | Does domain-specific reuse or content authoring reduce total change effort? | When reusable mechanics/assets/models help and when their extension cost dominates. |
| 13 / R13 | B | Can interaction contracts make extension and replacement more compositional? | What guarantees and verification effort accompany modular game behavior. |
| 14 / R14 | B, enabling | Which actual development problems and adoption constraints should the agenda target? | Relevant populations, change families and cost boundaries. |
| 15 / R15 | C | Can prospective analysis predict the better architectural choice? | Whether analysis improves adoption advice enough to justify its own effort. |
| 16 / R16 | C | Which effects transfer across F#, other languages and source/context representations? | The boundary between Nu/package effects, language effects and information cost. |
| 17 / R17 | C | How costly are interoperability, dependency upgrades and engine/application coevolution? | Whether local application gains survive ecosystem and integration work. |
| 18 / R18 | C | Can explicit state/history help distributed play, rollback or concurrent simulation? | A possible extension beyond local development, conditional on a real Nu capability and workload. |
| 19 / R19 | C | How do deployment targets, power and energy change the value assessment? | Resource costs at equivalent useful work on relevant platforms. |
| 20 / R20 | C | What expressive and collaborative work becomes possible for designers or less specialized users? | Whether tooling broadens useful authoring without shifting hidden work to programmers. |
| Future / R21 | B, deferred human study | Which representations and intervention policies help humans steer agents toward correct changes? | Whether specification, review, redirection and takeover costs justify a workflow under reliable measures. |

Band A deserves the most preparation now. Band B receives actionable designs and consequential reading alongside it; R21's future label separates human-study feasibility from eventual research value and does not renumber the existing IDs. Band C remains an active set of conditional questions. No band implies a positive effect or established feasibility. R01–R06 now have detailed specifications; the dispositions below govern their next preparation.

## Band A study preparation

### R01 Whole workflow value

**Question and comparison.** For stated developers and change families, compare an authentic Nu workflow with an independently credible alternative workflow. Match required behavior and available resources; allow each package its normal useful facilities when estimating package value. An ordinary workflow and a feature-ablation contrast estimate different things and need separate interpretations.

**Outcome.** New and retained behavior satisfied across all assigned changes, with total setup, learning, integration, change, review and recovery work. Runtime costs accompany the development outcome. Report failures and unfinished changes rather than comparing only successful attempts.

**Evidence and rival.** The [pinned Nu account](nu-grounded-maintenance-methodology-2026-09-14.md) and survey characterize capabilities; S255–S259 and S269–S271 offer prepared-tool/package comparisons. S42 shows why package rankings can reverse with the information supplied. Familiarity, task fit and tooling maturity may explain a difference; that remains part of a practical package contrast but prevents attribution to immutability or language alone.

**Next preparation and redirect condition.** The [2026-10-11 inventory](nu-comparator-and-convention-audit-2026-10-11.md#r01-version-and-package-boundary) now pins a provisional Godot/GDScript edition and its ordinary facilities, including live inspection, programmable undo and diagnostic snapshots. The [task/common-requirement audit](nu-task-diversity-and-common-requirements-2026-10-11.md) now grounds a platform interaction in #1020 and credits ordinary Godot character/platform APIs. Resolve the actual Nu route and intended input/movement/lifecycle/effect semantics; account for each package's required integration. Narrow or redirect if equivalent requirements cannot be supported credibly, the comparison is merely a deliberately weak baseline, or no consequential adoption decision remains. A scoped adverse Nu result is still informative.

### R02 Ownership and temporal coordination

**Question and comparison.** Compare credible Nu organizations for local interaction edits versus changes that coordinate entity lifecycle, parent/child state, events and effects. MMCC/ImSim is a candidate package comparison within one language/engine. The existing Breakout examples differ in physics and collision implementation; intended parity does not establish controlled equivalence.

**Outcome and rival.** Correct completed changes, retained temporal obligations and total work. Explicit transitions may reduce omissions while adding propagation/plumbing; nearby immediate-mode code may simplify local edits while increasing order or identity sensitivity. These are two-sided, prespecified predictions. Patch spread, messages added and architecture conformity are explanatory observations, not success definitions.

**Evidence and next action.** Reuse the source distinctions, S39/S40, S298 interaction typing, S299 modular preservation and the Ceptre/SGL alternatives. Use the [Blaze Vector mismatch register and requirement families](nu-task-diversity-and-common-requirements-2026-10-11.md): a second named pair has real input, gravity, hit-count and lifecycle differences, not established baseline equivalence. Fix intended common behavior and record any alignment work before assigning tasks. Redirect the causal claim to a package claim if differences cannot be isolated without rebuilding one style into the other. No adapter or baseline construction is authorized by this card.

### R03 History assisted debugging and recovery

**Question and comparison.** Compare an available Nu history/inspection workflow with a credible ordinary debugging/recovery workflow on reproducible failures. A within-Nu feature comparison may estimate an incremental workflow benefit; a comparison to another engine estimates a package difference. First identify exactly which state, inputs, pending work and effects each workflow retains.

**Outcome and rival.** Independently verified repair and successful continuation/recovery, elapsed and active work, retention/instrumentation costs and unresolved failures. A history view may help locate an unknown event but add overhead when the offending entity or event is already known. The [completed S42 study](literature/full-reading/S42-stream-debugger-comparison.md) gives a concrete predecessor for such a reversal; it does not estimate a Nu effect. S66 and [State Explorer/live replay](literature/full-reading/S296-S297-state-exploration-and-live-replay.md) provide closer debugging/history alternatives.

**Next action.** The [selected application contract](nu-history-application-contract-2026-10-11.md) specifies functional Gaia/MMCC Breakout, a halted checkpoint, B0 values and separate B1 continuation. Its launch, observation phase, controlled input and same-state fresh reconstruction remain feasibility dependencies. Prepare actual repair tasks only after the technical/access boundary is supported, preserving known versus unknown fault information. Redirect if instrumentation solves the fault or requires an unavailable facility; in-process getters do not verify agent access. A model restoration check alone does not establish debugging benefit.

### R04 Domain modeling and evolution

**Question and comparison.** Distinguish richer domain representation from the narrower [D1 explicit-case versus equivalent catch-all convention](fsharp-domain-evolution-research-proposal-2026-09-16.md). The first can change API and modeling effort; the second can potentially retain language, engine and initial behavior. Both D1 baselines can be exhaustive, and a correct catch-all remains valid.

**Outcome and rival.** Correct new and retained behavior, including compiler-silent semantic/temporal obligations, under a common allowance. Record diagnostic opportunities separately from obligations. Explicit cases may expose edit sites but also create noisy work or encourage mechanically compiling repairs. Static types, informative names, documentation, compiler feedback and source size are distinct interventions.

**Evidence and next action.** P08, S34–S37, S127/S129 and the completed type-evolution readings constrain the design. The [existing-site audit](nu-comparator-and-convention-audit-2026-10-11.md#r04-an-authentic-existing-source-site) now specifies the guarded MMCC update/fallback, checked-in warning policy and contrasting authored requirements. FS0025 is not explicitly promoted to an error; exact effective policy and diagnostics await authorized validation. The [Blaze Vector projectile site](nu-task-diversity-and-common-requirements-2026-10-11.md#r04-an-additional-authentic-convention-site) now adds lifetime/identity obligations and valid default behavior. These two demos broaden source coverage within one Nu lineage; they do not establish representative tasks. Keep D1 as one convention study; it cannot establish whole-Nu or F#/C# superiority. Redirect if the contrast is practically immaterial or already resolved by a close comparison.

### R05 Interactive correctness and evaluation

**Question and comparison.** Define what counts as successful change under state, time, identity, input and external-effect obligations. A separate methods study would compare observation strategies against independently justified fault/behavior cases; simply building a benchmark is not yet a research contribution.

**Outcome and rival.** False passes, false failures, inconclusive results, fault sensitivity and specification/observation cost. Compiler acceptance, screenshots, sampled traces, development-test agreement and final behavior are distinct. S42's supplied-test completion is useful evidence within its generated repair setting; it is not an independent general semantic oracle.

**Evidence and next action.** Reuse [industrial regression testing](literature/full-reading/S294-industrial-game-regression-testing.md), [temporal monitoring](literature/full-reading/S281-game-monitoring-thesis.md), S220/S222 and agent/game judge reconstructions. Draft an obligation-to-observation table covering triggers, clocks, horizons, resets, identity, pending events and inconclusive cases. Resolve an exact missing formula or release when the chosen contract depends on it. Development feedback must be separated from final scoring; no final-test-driven repair or stopping.

### R06 Runtime and state retention costs

**Question and comparison.** Determine how chosen representation, retention and coordination policies change frame-time tails, allocation, working set, throughput and edit/recovery latency under equivalent useful work. Compare identifiable policies or complete runtime packages, with the corresponding attribution boundary.

**Outcome and rival.** A workflow can reduce debugging effort while increasing retained memory or frame stalls. Charge snapshot creation, retention, disposal, host work and rebuilding to the correct boundary. Average FPS and source size cannot stand in for that trade-off.

**Evidence and next action.** S138–S151, S211–S214, S237–S248 and S260/S261 supply mechanisms and workload-specific positive/adverse results. Prepare workload dimensions—world size, mutation rate, retention horizon, event fan-out and external/native resources—and identify the exact Nu policy each comparison would vary. Use a workload grounded in R01/R03 before proposing unrelated allocator measurements. A cost result can refine useful scope without refuting every development benefit.

## Band B study preparation

### R07 Learning and comprehension

Compare newcomers and experienced users within separately defined populations, with an authentic onboarding/support policy. Measure learning effort, correct changes, delayed retention and transfer to a new task; keep preferences and comprehension questions secondary. S300/S301 show why understanding, structure-conformity scores and partial progress cannot be substituted for completed change. S39/S40 and S255–S259 preserve positive and contrary representation results.

Next, prepare prerequisite and training boundaries and identify whether the question concerns initial adoption or trained productivity. S38's acquired Cognitive Dimensions paper becomes consequential if its constructs are used as measures; it remains unread. The primary abstract of the [engine-API usability study](https://onlinelibrary.wiley.com/doi/10.1002/spe.2985) describes eight structural metrics across 95 C++ engine repositories. Its full method remains unread; this screen supplies no human usability result. Redirect if a supposed language effect is only unequal preparation or the claimed outcome is a preference score.

### R08 Coding agents and tool support

Compare concrete agent workflows using Nu representations, typed/source context or inspection tools while fixing the intended model/policy and documenting available information and cost. Human and agent results require separate estimates. Valid repairs may reorganize code; conformity to the assigned starting style is not an outcome filter.

Measure new/retained behavior across every assigned attempt, resource use, failure classes and recovery burden. P03–P13, S35/S36 and the game-agent readings already overlap strongly with generic context/planning claims. The next preparation is an information/feedback/accounting contract and a close-method comparison. Read [S227 v2](https://arxiv.org/abs/2605.28258v2) before adopting its updated GUI-playtesting method; the completed note covers v1. Redirect if the contribution is just another model leaderboard, F# port, or unpriced tool advantage. New model calls and workers remain unallocated.

The current packet proposes bounded agents as executors of independently specified changes, while treating task convergence as a coverage risk. Source/history/practice provenance, adverse families and valid alternative solutions matter more than repeated prompts on one puzzle. Agent-only observations do not estimate human-steered productivity; R21 retains that future transfer question.

### R09 Sequences of change and retained obligations

Compare the durability of a selected representation/workflow across ordered changes with an explicit dependency structure. Preserve the submitted predecessor state and record what happens after a failed change. A clean reference predecessor, a repaired predecessor and the actual inherited state define different questions.

Measure retained and new obligations, cumulative effort, recovery and missingness for the assigned sequence. P04–P06/P09 and the long-horizon agent readings are close prior art; sequence length alone adds little novelty. Prepare a requirement/lineage model and distinguish a persistent benefit from short-task gains displaced into later rework. Redirect if the design silently filters successful histories, supplies successor solutions as memory, or repeats an already established benchmark contrast without a new practical decision.

### R10 Live editing and state migration

Compare restart/reconstruction, replay and migration workflows for a specified class of edits. State the identities, defaults, pending events, observers and external effects that must survive; a type-correct migrated object does not establish valid continuation.

Measure correctly preserved behavior, recovery/reconstruction work and unsupported edits, with S71/S86 and [S295](literature/full-reading/S295-persistent-object-evolution.md) as distinct change contracts. Next, map proposed Nu edits onto those contracts and verify which facility is actually available. Original S218/S219 or other edition gaps become required only for a chosen close comparator. Redirect or narrow if the proposal assumes arbitrary code/state migration or reversal of irreversible effects. Demonstrating more edit kinds alone does not establish developer value.

### R11 Collaboration and handoff

Compare team workflows for concurrent edits, merge conflicts and designer/programmer handoff. Establish whether Nu changes shared representation, coordination or tooling; personal debugging history and a collaborative document history are different facilities.

Measure correct integrated outcomes, unresolved conflicts, total team effort and work shifted between roles. [S283](literature/full-reading/S283-nccollab-collaboration-history.md), [S284](literature/full-reading/S284-levelmerge-scene-merge.md), S287 and S288 supply selected collaboration/history methods and costs. Next, prepare role/ownership boundaries and plausible concurrent changes, then verify the actual merge and history contracts. Account for team-level assignment and repeated tasks. Redirect if the apparent gain is one role's time saved by undocumented assistance from another, or a nonexistent merge facility is required. Recruitment remains separate from this preparation.

### R12 Reuse and content authoring

Compare reusable mechanics, asset/configuration families or domain-specific authoring with a credible ordinary implementation. Separate creating a supported variant from extending the representation to express a new requirement.

Measure behavioral validity, authoring/change effort and amortized construction/integration/extension cost. S255–S259 show prepared-tool gains, nulls and overlap between datasets; [S263/S264](literature/full-reading/S263-S264-content-generation-access.md) remain access-limited generation methods. Next, define the intended reuse unit and whether the task stays within the existing vocabulary. Follow those original methods or another specific comparator when necessary. Redirect a claimed maintenance benefit if only visual appeal, generated volume or family similarity is observed. Distinct editions of one dataset are not replications.

### R13 Interaction composition and guarantees

Compare an explicit interaction/behavior contract with a credible less-formal development method for extension or replacement. The research can concern what is provable, what faults are detected, or what verification effort is saved; these are separate outcomes.

S298 provides data-compatible interaction substitution with configured runtime checks. [S299](literature/full-reading/S299-modular-reactive-verification.md) provides property preservation under model and exit assumptions; Ceptre distinguishes local existential composition from whole staged behavior. Next, write the intended Nu contract and identify its host/world assumptions and the work needed to establish them. Redirect if the claim merely restates an existing theorem, confuses disabled diagnostic opportunities with checks, or promises whole-system preservation outside the model. Formalization construction is a later authorization decision.

### R14 Practice and adoption relevance

Use existing primary studies and passive repository/source inspection to identify recurring changes, constraints, support needs and reasons to adopt or abandon a workflow. A later empirical study would need a justified sample and its own authorization; observations/interviews remain held. This direction supplies sampling and cost boundaries for R01–R13; another list of reported complaints is not automatically a standalone contribution.

S250–S252, S267–S271 and S288–S290 already supply situated practice evidence. [S266](literature/full-reading/S266-postmortem-extension-access.md) could update the corpus account if source overlap, selection and coding are reconstructed; its abstract cannot establish industry prevalence. Next, connect each proposed change family to evidence and document whose work is missing. Continue the retained practice search from offset 100 when a gap needs it. Redirect population-wide claims when the evidence only supports a situated sample. No participant contact or recruitment occurs under this agenda.

## Band C study preparation

### R15 Prospective architecture choice

This retains D2 as a future decision question: does analysis performed before seeing successor outcomes improve architecture/package choice against equally informed ordinary review, defaults or simpler predictors? Measure decision quality and the cost of producing advice. The earlier [D2 proposal](architecture-maintenance-research-proposal-2026-09-15.md) and completed selection literature already establish much of the method.

Prepare this only around a real choice with credible alternatives and change profiles. Advice and predictions must precede outcome observation. Promote it when R01/R02 identify meaningful, predictable trade-offs; demote it if one option dominates or the analysis costs more than the decision is worth. Preparing the question does not reopen D2/A0 selection or construction.

### R16 Language and information representation transfer

Ask whether a specified result survives a change of language, library or source/context representation. A natural F#/C# package comparison and an isolated source-information manipulation have different interpretations. Match intended behavior and accessible support; do not force an unnatural transliteration to manufacture equivalence.

Measure correct change and total work/information cost. Existing E/H negative compactness observations remain valid; authored source size, cumulative model traffic and retained/peak context are distinct. S34–S37 and the type/agent evidence defeat a generic “F# is understudied” rationale. First identify a result or practical choice worth testing for transfer. Redirect if training familiarity, APIs and tooling cannot support the intended attribution. A universal language ranking is outside this agenda's defensible scope.

### R17 Ecosystem integration and coevolution

Compare supported approaches to dependency/API upgrades, native-resource integration or engine/application boundary changes. Measure all affected behavior, integration/recovery effort and ongoing compatibility work. S267's operational migration and S204's industrial change propagation motivate costs beyond the local edit.

The [Nu/Jolt dependency audit](nu-jolt-dependency-audit-2026-10-11.md) now supplies an actual cross-layer case: history rebuilding, native maintenance/callback semantics, binding coverage and package provenance. It verifies package-to-vendored-binary identity and the upstream zero-time fix, while exact native source/build correspondence and actual Nu behavior remain open. Nu's positive-time guard and periodic optimization persist; upstream batch advice is not an established managed API at the inspected pin. Use this case to refine R03/R06 first. Promote R17 when integration demonstrably dominates the target workflow; a provenance mismatch alone is not a standalone research contribution. Existing backend, transport and security decisions remain fixed.

### R18 Distributed state and concurrency

Explore whether explicit state, identity and history could help deterministic replay, rollback, synchronization or concurrent simulation. No inspected Nu capability is being newly asserted to implement these distributed guarantees. Networking delay, nondeterminism, ownership and externally visible effects require their own contracts.

Possible outcomes include divergence, recovery correctness, responsiveness and computation/bandwidth cost at equivalent work. The new search locates *Hybrid Prediction for Games' Rollback Netcode* (DOI 10.1145/3532719.3543199) and CRDT-based game-state synchronization (conference DOI 10.1145/3721473.3722144; same-title arXiv 2503.17826). These are title/metadata leads; their methods and exact edition relationship remain unverified. Next, establish a real Nu use case/capability before promoting a primary reading. Keep this exploratory if it requires creating a networking subsystem; immutability alone does not establish determinism or network consistency.

### R19 Deployment power and energy

Compare relevant deployment/runtime configurations at matched useful work, quality and behavior. Measure power, total energy, frame-time distribution and any developer/runtime trade-off separately. [S260](literature/full-reading/S260-unreal-energy.md) and [S261](literature/full-reading/S261-unity-unreal-energy.md) show workload-dependent engine ordering; S265's selected source/data and missing visuals retain their limits.

Next, connect a target platform and workload to R06, then identify necessary build and measurement correspondence. Promote when energy or constrained hardware is a real adoption boundary. Redirect an independent engine-ranking study if it repeats hardware-specific FPS/power comparisons without an unresolved Nu decision. Equal wall-clock duration alone does not establish equal completed work.

### R20 Expressive reach and designer collaboration

Ask whether Nu's actual authoring workflow lets designers or less specialized developers express and revise useful interactive behavior with less dependence on specialist intervention. Compare authentic workflows and separately account for preparation by tool builders or programmers.

Measure successfully expressed behavior, revision work, learning and assistance; creative quality requires a justified independent assessment rather than screenshot preference as a substitute for behavior. S67, S253, S288 and S291–S293 motivate expressive and cross-role questions. Next, identify a role, authoring capability and representative unsupported change, then follow the exact usability/expressiveness method needed. Promote when that role and facility exist in the intended setting. Redirect if the proposed benefit depends on inventing a new editor or on excluding all requests outside a prepared vocabulary.

## R21 Human steering and intervention — future direction

Ask whether Nu's representations, state visibility and contracts help people specify work, delegate, inspect evidence, redirect an agent and accept correct changes. This is distinct from R08's fixed agent/tool policy and R11's multi-person editing. It remains valuable for the user's intended 2027 setting, while direct steering effectiveness is deferred because construct reliability, task/person variation and participant feasibility are unresolved.

Preserve two future policies: **steering-only**, where people specify/inspect/diagnose/redirect and agents implement, and **unrestricted intervention**, which also permits direct editing and takeover. Human-authored replacement code or patches supplied through prompts count as human coding. Count specification, context gathering, review, redirection, rescue and rework alongside agent cost and verified outcomes. A successful artifact does not reveal how much expert work produced it.

[S229](literature/full-reading/S229-picoscenes-expert-ai.md) supplies favorable expert–AI practice with explicit allocation/accounting limits. Next, develop a literature-grounded observation vocabulary and reliability questions before proposing participant numbers; a larger sample cannot by itself define the construct. Small descriptive/pilot work could later inform feasibility, but no recruitment or study is authorized now. Retain human-only/agent-only cases only when they clarify a specific question, rather than requiring three equally funded arms or a universal autonomy ranking. Do not retrofit this direction into D1 or add a steering-policy factorial to R02.

## Readiness and next actions for all directions

These are preparation dispositions, not execution decisions. **Review-ready** means ready for bounded feasibility review with stated unvalidated conditions. **Conditional** identifies a consequential dependency; **deferred** preserves a future question or existing hold. The [study packet](nu-research-study-designs-2026-10-08.md) owns detailed R01–R06 contracts and shared dependencies.

| ID | Disposition | Consequential dependency | Next desk action / promotion condition |
| --- | --- | --- | --- |
| R01 | Conditional; common platform requirements prepared, human net-value study deferred | Actual Nu platform/character route, matched behavior and full work boundary | Use #1020's practice motivation and ordinary Godot support. Freeze movement/input/lifecycle/effect semantics and integration costs before construction. |
| R02 | Review-ready at package scope; second pair conditional | Common semantics, visible alignment work and initial behavior | Use Breakout plus Blaze Vector's mismatch register. Keep request-derived and authored families distinct; two styles are not independent applications. Require later common-behavior observations. |
| R03 | First application/B0–B1 contract specified; feasibility and agent extension conditional | Supported functional launch, observation phase, controlled continuation and actual agent access | Apply the selected MMCC/Gaia state/effect contract and matched fresh reconstruction. Validate only under later authority; do not substitute restart, input/RNG assumptions or source-only access. |
| R04 | Review-ready under D1 conditions; two authentic sites inspected | Actual equivalence/diagnostics, useful task value and temporal/identity obligations | Use Breakout update and Blaze Vector projectile-command sites. Preserve valid cancellation defaults and no-case-extension changes; demo lineage is not representative task coverage. |
| R05 | Source-bound trace specification prepared | Independent reference behavior and exercise evidence | Bind the audit's traces to chosen requirements, phases, horizons and tolerances before later construction; no executable oracle exists. |
| R06 | Cost boundary source-grounded; measurements conditional | Same-mode retention and equivalent useful work | Use the retained/shared/native inventory; separate checkpoint creation, retention, rebuilding and resumed frames. History eviction/instrumentation is not a finished feature. |
| R07 | Deferred human comparison; conditional desk work | Prerequisites, training and valid constructs | Define onboarding versus trained-productivity claims; read S38 before adopting its constructs as measures. |
| R08 | Conditional support for bounded tasks | Real tool access, feedback and accounting | Apply the packet's information contract; read S227 v2 only if the updated GUI method is selected. |
| R09 | Conditional | Requirement lineage and failed-predecessor policy | Prepare a sequence specification distinguishing actual inherited, repaired and clean predecessor states; promote when a single-change result needs durability evidence. |
| R10 | Conditional mechanism question | Supported edit and continuation contract | Map one proposed edit to restart/replay/migration boundaries, with identities and pending effects; promote only an actual supported capability. |
| R11 | Deferred team comparison | Actual merge/history facilities and role boundary | Identify a source-supported concurrent-change/handoff case and total-team accounting before participant design. |
| R12 | Conditional | Reuse unit, expressible variants and generation methods | Separate use from extension of a vocabulary; resolve S263/S264 if their method changes the selected comparator. |
| R13 | Conditional | Valid host/world models and relevant boundary predicates | Write one intended extension/replacement contract using S298/S299; promote only if the additional guarantee or effort question exceeds a restated theorem. |
| R14 | Active enabling desk work | Task provenance, eligibility and population scope | Extend the verified public lineage with credible task diversity; distinguish native historical, authored and adapted requirements. Resolve S266 before expanded prevalence claims. |
| R15 | Deferred D2 | Meaningful prospective choice and pre-outcome information | Retain the selector history; promote only after R01/R02 expose a practical predictable trade-off and D2 is explicitly reopened. |
| R16 | Conditional later transfer | A bounded result worth transferring | State the changed language/context/package dimension and credible equivalent behavior; preserve E/H adverse compactness evidence. |
| R17 | Conditional; cross-layer case inspected | Exact native build provenance, actual loaded artifacts and affected obligations | Use the package/blob/fix audit to refine R03/R06; preserve Nu's positive-time/optimization policy and unverified batch-binding route. No current defect or cost advantage is established. |
| R18 | Deferred exploratory extension | Verified distributed Nu capability and real workload | Establish a concrete use case before reading netcode/CRDT methods as treatment evidence or proposing new infrastructure. |
| R19 | Conditional extension of R06 | Target platform and matched useful work | Identify an energy-relevant adoption boundary, then bind build/sampling/measurement correspondence; promote only if it changes the value decision. |
| R20 | Deferred human-role comparison | Existing authoring facility and intended non-specialist role | Identify a representative supported/unsupported revision and assistance boundary before expressive-reach claims. |
| R21 | Deferred steering effectiveness | Reliable constructs, task/person variation and feasible participant design | Prepare measurement candidates from S229 and consequential primary studies; preserve both intervention policies without selecting sample size or running a pilot. |

## Shared study requirements

Each later protocol needs a claim-to-source-to-comparison record: the actual Nu revision/capability, intended users and changes, closest methods and adverse evidence, assigned treatment, initial information, permitted development feedback, final observation, total cost, and the inference it supports. The current source basis remains revision `064f7ae92a8506689cd91aff5e6804a375d6ef3d`; this preparation does not certify current-head source correspondence. A later source refresh must record what changed.

Separate package effects from mechanism effects. Use credible alternatives and give a reason for their information/tool policy. Initial behavior equivalence is an obligation to validate, not a consequence of naming the same game. Do not implement the requested change in an adapter, hide extra work in setup or require the preferred internal organization as the behavioral answer.

Choose outcomes appropriate to the question. For maintenance, retain all assigned attempts, new/old behavior, incomplete outcomes and missingness. Do not average time only over successful repairs and call it the overall treatment effect. Model repeated developers, applications, tasks and sequences at their actual units; repeated frames and publications are not independent participants. Specify practically meaningful effects, uncertainty analysis and resource allowances only after the population, outcome and feasible design are known. No sample size or allocation is invented here.

Record intermediate observations—diagnostic exposure, comprehension, navigation, patch spread, tool use and source size—without turning them into proof of correct change or adjusting away post-treatment consequences to claim a pure mechanism. Information probes can themselves change behavior and cost. S42 makes initial failing-entity knowledge a concrete candidate moderator; it does not justify a huge factorial crossing every possible factor.

Preserve favorable, null, adverse and interaction results. Existing E/H results are not rescored or discarded. Stop or redirect a proposed study when its decision is immaterial, its closest predecessor already answers it, its comparison is not credible, its outcome cannot test the claim or its required resources are unavailable. An adequately measured negative result is not a reason to replace cases until Nu wins.

## Preparation order and literature continuation

1. **Use the completed R01–R06 design packet.** The current emphasis is mechanisms/costs plus bounded agent maintenance, with R14 supplying practice/task provenance. R01 retains eventual adoption value; human steering is a future R21 question. No mandatory human/agent/team factorial follows.
2. **Use the resolved source boundaries before any build.** The [2026-10-11 audit](nu-source-contracts-and-scenarios-2026-10-11.md) supplies R02 ownership/order/identity/effects, a verified historical issue/patch, R03's real history/reference/access boundary and R05/R06 trace/cost specifications. The [history application contract](nu-history-application-contract-2026-10-11.md) now selects R03's functional MMCC/Gaia subset and B0/B1 observations. The task-diversity audit adds common platform requirements and a second application/site. Next resolve the actual Nu platform/character route and intended common semantics; actual R03 launch/phase/access and R04 equivalence/diagnostic checks remain held. Source-grounded sketches and historical fixes are not validated equivalent baselines or new allocation.
3. **Maintain all other dispositions above.** Use their cards to identify beneficiaries, outcomes and conditions for promotion. Resolve consequential accessible gaps without waiting for every human/access-limited direction. A newly found close or adverse source can reorder the agenda.
4. **Read where the answer can change the design.** S42's previously queued publication and selected artifact are now reconstructed. S38 is the next accessible conceptual dependency if usability measures are adopted. S227 v2 becomes a method/version dependency for R08; S263/S264 for R12; S266 for an expanded contemporary practice claim. Exact temporal, live-state and comparator gaps remain attached to the directions that need them. Resolve accessible consequential gaps without waiting for a fixed batch to finish or for denied sources to become available.
5. **Promote C directions by evidence.** A verified capability, an actual stakeholder/workload need, or a close method that exposes an important unanswered question can raise their priority. Generic novelty claims, attractive feature names and raw citation counts cannot.

Searches are targeted to missing mechanisms, comparators, methods, contrary results and edition changes. Use aliases across relevant communities and follow primary sources. Scite requests remain `limit:20`; native Consensus requests remain `page_size:100` when used. Continue useful pages by actual returns and reformulate noisy queries; log unopened continuations and denied routes. Abstract/title screens locate reading candidates and do not establish effect, absence or full understanding. Create/reuse Zotero records before selected reading, preserve preprint types and edition lineage, and report considered decisions once after historical deduplication.

The preceding discovery pass inspected engine-usability/adoption and distributed-state leads and extended the retained practice query through positions 81–100. Broad prefixes were noisy and were reformulated; later pages remain open. The current design pass reuses that evidence and completed reconstructions; it adds no new retrieval/full-reading credit or citation-screen decisions. Neither pass certifies novelty across the agenda. Reopen the closest-source/edition check before a stronger novelty or publication claim.

All current construction, recruitment, added-worker, model/probe/candidate and H-execution holds remain; new experimental allocation is zero. Authorized work now is continued literature, source inspection, synthesis and preparation of the full prioritized agenda. When a concrete study is ready for a separate execution decision, its comparison, costs and unresolved risks must be reviewable first.

## Coverage against the broad survey

| Survey theme | Agenda directions |
| --- | --- |
| B01 Foundations and comprehension | R01, R02, R07, R20, R21 |
| B02 Domain types and evolution | R04, R10, R13, R16 |
| B03 Reactive coordination and lifecycle | R02, R05, R13, R18 |
| B04 Persistent state, effects and history | R03, R06, R09–R11, R18 |
| B05 Game architecture alternatives | R01, R02, R12, R15, R17 |
| B06 Runtime and resource costs | R06, R18, R19 |
| B07 Specification, testing and oracles | R05 and the outcome contract of every empirical direction |
| B08 Debugging and live development | R03, R08, R10, R20, R21 |
| B09 Coding agents and language effects | R04, R08, R09, R16, R21 |
| B10 Maintenance and adoption in practice | R01, R07, R11, R12, R14, R17, R20, R21 |
| B11 Architecture choice and assessment | R01, R02, R06, R15 |
| B12 Empirical and synthesis methods | R05, R14, R21 and the shared study requirements |

Player enjoyment, accessibility, security and resilience may be important requirements or costs within a chosen game/workflow, but no inspected Nu-specific causal mechanism currently justifies standalone superiority studies for them. Promote such a direction when an actual capability, beneficiary and comparison are established. Generic AI game generation, universal language rankings and unrelated hardware leaderboards likewise need a concrete connection to this agenda before they displace its leading questions.
