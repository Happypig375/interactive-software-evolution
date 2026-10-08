# Study designs for Nu mechanisms, costs and bounded agent maintenance

**Design packet, 2026-10-08.** Implements the [continuation plan](nu-research-continuation-plan-2026-10-08.md) and the leading R01–R06 directions in the [agenda](nu-research-agenda-2026-10-08.md). These are proposed comparisons and observation specifications, not constructed baselines, validated protocols or experimental results. [PLAN](../PLAN.md) retains all execution holds and zero new allocation.

Human-steered development is the intended eventual use context. Near-term claims concern inspected mechanisms, their behavior/costs, and specified agent tasks. Steering effectiveness is deferred as R21; human-only and agent-only extremes are optional reference cases when they answer a concrete question. This packet does not introduce equal human/agent/team arms or assume a 2027 market distribution.

## Evidence and source basis

The reused Nu source basis is **064f7ae92a8506689cd91aff5e6804a375d6ef3d**, as inspected in the [source ledger](nu-grounded-maintenance-sources-2026-09-14.md) and [methodology](nu-grounded-maintenance-methodology-2026-09-14.md). This design pass rereads those records and selected completed literature reconstructions; it does not refresh current Nu HEAD, independently rerun code or acquire new primary papers. Historical source inspection and proposed behavior below retain separate status.

| Source-supported starting point | Consequence for the proposed comparison | Still to establish before execution |
| --- | --- | --- |
| MMCC and ImSim empty templates and Breakout examples exist at the pin. | Use legitimate within-Nu organizations as R02 candidates. | Initial observations, supported requirements and a credible comparison boundary; the empty templates are not matched games. |
| ImSim Breakout uses physics-body/collision results; MMCC updates coordinates and tests intersections explicitly. | Primary R02 attribution is to the selected packages. | Whether a narrower responsibility contrast can be isolated without destroying either idiom; intended gameplay parity is not a test result. |
| WorldTypes has a mutable wrapper; WorldModule has imperative/copying paths. | R03/R06 must describe the selected state boundary and actual policy. | Which referenced objects and native resources are shared, copied, retained or restored for the chosen facility. |
| Gaia uses snapshots for undo/redo. | A concrete history candidate exists for R03. | Whether the selected operation concerns editor documents, running game state or another boundary; pending work and external effects cannot be presumed restored. |
| EventGraph organizes event state. | R02/R05 need ownership, delivery and lifecycle observations. | Ordering, subscription cancellation and effects for each selected contract; event organization alone does not establish event sourcing. |
| A stub-world test initializes a world and a one-frame run. | There is a source lead for later observation feasibility. | A working environment and a sufficient observation interface; no headless candidate sandbox has been validated here. |

The linked ledger supplies exact pinned source locations. Reinspect those locations for a specific unresolved contract rather than treating a generated account or old description as current implementation truth. Record a new pin and its relevant differences before transferring this design to another revision.

## Shared design and accounting contract

### Units, comparison and initial information

An **obligation** is a required observable behavior; a **task** is one assigned change; a **family** groups tasks with the same substantive demand; an **application** supplies a starting program. An **attempt** is one independently initialized agent execution on a task/arm. Cosmetic variants and repeated calls do not create new families or applications.

For R02/R04 and any promoted R03 agent comparison, propose paired tasks on the two eligible arms, independently fresh workspaces/contexts and randomized or interleaved execution order. Keep source revision, model identity/configuration, environment, intended requirements, feedback and resource rules explicit. Do not supply the other arm, comparative predictions, reference solutions or final scores. This is a future policy specification; it does not modify or execute historical no-tools/no-repair protocols.

The default proposed agent policy permits ordinary source navigation, existing documentation and declared build/development-test feedback within a common fixed resource allowance. R03 additionally needs the exact history/inspection interface that defines its treatment. A source-only agent condition cannot silently inherit GUI access or a task-solving helper. Current runner/backend decisions are retained; compatibility and observation access are later feasibility dependencies, not reasons to create a new adapter now.

Requirements must precede candidate outcomes. Keep the desired behavior independent of a preferred patch and permit valid reorganization, helper extraction and catch-alls. Record initial information, including whether a failing entity/event is identified. Subsequent diagnostics, edits and tool usage can explain an outcome; do not adjust them away to label the remaining difference a pure source effect.

### Task provenance and convergence risk

The following are **requirement sketches**, not mined issues, authored successors, approved benchmark tasks or a claim of current Nu support for every operation.

| Family | Proposed requirement and old behavior to retain | Contrast or counterexample it can expose | Provenance and limit |
| --- | --- | --- | --- |
| F-local | Change a local control's condition/response while keeping unrelated controls and screen transitions correct. | Locality may help; implicit evaluation order or identity may hurt. | Pinned template/control discussion and S67's immediate-access/clutter trade-off; no verified Nu issue instance yet. |
| F-lifecycle | Change pause/resume or parent/child creation/removal while preserving ownership, pending actions and repeated transition behavior. | Explicit coordination may help; extra propagation may omit a required transition. | Nu source/practitioner ownership concerns and S291–S299 contracts; concrete trigger/deadline still needs source binding. |
| F-burst | Apply multiple eligible events under a stated rule for ordering, multiplicity and side effects. | Coherent processing versus fan-out/duplicate work; the requirement must decide what is permitted. | Event-graph and fan-out accounts; do not invent a universal exactly-once contract. |
| F-domain-distinct | Add a domain case that needs distinct behavior, retaining old-case semantics. | Useful diagnostic opportunity versus compiler-silent wrong behavior. | D1 and the type-evolution readings; not a favorable-agent-outcome filter. |
| F-domain-default | Add a case legitimately covered by the existing fallback, plus a change that does not extend the case set. | Enumeration can add work without behavioral benefit; correct defaults remain successes. | D1's adverse/control cases and S72's convention evidence. |
| F-history | Revisit a reproducible failure and repair it, with the failing entity either identified or initially unknown. | History can expose causes or add setup/navigation cost. | S42's information-dependent reversal and S66/S296/S297; no Nu effect inferred. |
| F-effect | Recover represented state around a permitted reversible operation and around an operation whose effect cannot be undone. | Stored values may be insufficient for correct continuation. | S235's restricted compensation and S107/S296/S297 contracts; unsupported operations define a boundary, not automatically a Nu bug. |

These families guide coverage and do not impose an all-factor experiment. Before execution, each selected task needs an exact requirement source, application/pin, initial contract, exercise conditions, observation map, strongest rival and reason for inclusion. Mark an illustrative task as illustrative until a real source/history/practice basis is verified. The existing source ledger explicitly lacks a verified Nu-specific issue/PR task; do not turn these sketches into claimed issue mining.

The maintainer should challenge redundant families and include cases favorable to either alternative before observing candidate results. Record actual user/practitioner input separately from AI synthesis. Another agent response or a request for diverse ideas is not independent review or evidence of coverage. Characterize repeated solution patterns only from observable edits/trajectories under a declared coding scheme; do not infer hidden reasoning. Broad transfer requires additional applications/families or later executor replication, not simply more calls on one puzzle.

### Outcome, missingness and costs

The main agent endpoint is **all required old and new obligations satisfied within the declared allowance**, relative to a validated observation contract. Report new/retained obligations separately as secondary outcomes. Successful compilation, a supplied test pass or a matching screenshot is insufficient by itself. Finite observations warrant only their declared scope.

Record eligible assigned attempts, valid completions, demonstrated failures, budget exhaustion, infrastructure-blocked/inconclusive observations, policy deviations and unexecuted planned slots separately. All assigned attempts stay in the disposition table. For the decision endpoint, an assigned attempt without established success receives no completion credit; distinguish its reason and bound conclusions when infrastructure missingness could change the contrast. Do not label an unevaluated attempt semantically incorrect. Never select the main timing sample using only successes.

Human operational intervention and rescue must be logged if later execution encounters them. Keep the original assigned outcome; a rescued patch cannot replace it. A separate assisted follow-up requires its own declared scope. Test authors and any actual reviewers must be identified honestly; a specification written by this maintainer is not human sign-off.

| Quantity | Accounting rule |
| --- | --- |
| Agent resources | All attempted model/tool work under the pinned accounting rule, including failed repairs; keep tokens, tool time and priced expenditure distinct. |
| Elapsed time | Assigned start through stop, including execution and permitted feedback; distinguish infrastructure waiting. |
| Preparation/integration | Record one-time source, instrument, oracle and tool setup separately from per-task work; do not hide it in an adapter. |
| Runtime cost | Matched workload, environment and useful work; include retention, disposal/rebuild and relevant host/native work. |
| Human effort | Only actual observed preparation/review/rescue time if collected under an approved method; no productivity estimate from patch size or agent elapsed time. |

For paired agent outcomes, prespecify the task-level success contrast, within-family aggregation, family weighting and planned family interaction before execution. The default descriptive target is the declared task portfolio with equal weight per substantive family and equal weight per selected task within family; repetitions estimate each task/arm's stochastic performance. This is not an industry frequency estimate. A single Breakout pair remains a local case. An inferential extension must justify independent clusters, an uncertainty procedure and precision; repeated frames or calls cannot supply missing applications. No interval, sample size, worthwhile effect or allocation is invented here.

Readiness requires the intended maintainer's practical decision threshold, an acceptable resource boundary, and a model-free sensitivity/precision justification at the actual unit. If the feasible units cannot support that claim, publish descriptive feasibility or narrow the claim. Preserve all E/H results; no historical result is rescored by these endpoints.

## R01 — Whole workflow value

**Question and beneficiary.** For a maintainer considering Nu for interactive software, which verified development capabilities and costs could justify adoption, and what evidence would establish net value? Human-steered work is the future practical target; this phase prepares the package comparison and its missing evidence.

**Candidate comparison.** Nu's documented workflow versus an ordinary Godot workflow is the leading candidate for the packet because [S67](literature/full-reading/S67-pronto-game-prototyping.md) and [S296/S297](literature/full-reading/S296-S297-state-exploration-and-live-replay.md) already reconstruct concrete nearby interaction/history methods. This is a justified candidate, not a selected current Godot release or a claim that a research plugin ships with the engine. Treat ordinary engine facilities and an optional research-plugin extension as different packages. A future version/language/support inventory must establish both sides before construction; a mature Unity workflow remains a conditional alternative only if it fits the chosen task better, with a recorded reason for changing the candidate before outcomes.

**Tasks and information.** Start from F-local/F-lifecycle and, if both packages support it, F-history, using independently stated requirements and native idiomatic facilities. Match intended behavior and accessible documentation/resources, not source layout or forced transliteration. Account for setup, learning, integration, support and recovery. Do not assemble a whole-workflow score by combining unrelated papers or agent-only tasks.

**Outcomes and rivals.** Verified completed changes, total work and relevant runtime cost; favorable Nu mechanisms can be outweighed by unfamiliarity, missing integration or expensive retention. Package differences include language, tools and ecosystem support, so a package result does not isolate immutability. Human-active effort and steering quality remain unmeasured until an appropriate participant/observation design exists.

**Evidence consequence.** S67 supports useful interface trade-offs with limited human evidence; S296 supplies state-navigation benefits and significant isolation costs; S42 supplies an initial-information crossover. [S229](literature/full-reading/S229-picoscenes-expert-ai.md) supplies a favorable expert–AI workflow with allocation/accounting limits. Preserve these positives without importing their effect sizes into Nu or treating their task/sample definitions as interchangeable.

**Disposition and next action.** Conditional package proposal; human net-value estimation deferred. Build a read-only capability inventory for the pinned Nu facility and the candidate Godot edition, linking each requirement to actual support and integration work. R02–R06 can narrow those requirements meanwhile. Redirect if matching requires an artificial weak baseline, a missing new engine facility or a claim that the component evidence already establishes human productivity. The stronger novelty/comparator check is required before a publication-priority claim.

## R02 — Ownership and temporal coordination

**Question and contrast.** Under a fixed agent policy and allowance, do the pinned Nu MMCC and ImSim packages differ in verified completion of local and coordinated changes? Compare the existing credible styles; sharing F# and Nu does not isolate responsibility organization because physics/collision and API use also differ.

**Source and task contract.** Use F-local and F-lifecycle as the initial planned strata; F-burst is promoted only when its event rule and common observations are source-bound. For each task specify the state owner, identity creation/destruction, order of reads/updates, event delivery, pending work, cancellation and external effects. Name initial observations required in both arms. Numeric motion/collision equality cannot be assumed; if the desired common contract depends on it, validate that contract later or narrow the selected behavior without hiding the package difference.

**Two-sided predictions.** Explicit transitions may help coordinated obligations and create extra propagation failures. Nearby interaction processing may help local edits and increase ordering/identity sensitivity. Prespecify this local/coordinated contrast before outcomes. Patch spread, messages added and architectural drift are explanatory observations; a safe implementation in either style passes.

**Evidence and outcomes.** [S39](literature/full-reading/S39-reactive-comprehension.md), [S40](literature/full-reading/S40-reactive-api-usability.md), [Ceptre](literature/full-reading/S291-S293-ceptre-resources-and-editor.md), [S298](literature/full-reading/S298-interaction-typing.md) and [S299](literature/full-reading/S299-modular-reactive-verification.md) motivate explicit interaction boundaries without proving a Nu benefit. Use the shared all-obligation endpoint and resource accounting, with the predeclared family contrast. Unknown initial equivalence and physics/API differences bound causal interpretation.

**Feasibility requirements.** An exact two-arm initial-contract sheet; source-grounded task provenance; exercised independent old/new observations; reachable environments; fixed warnings/tools; and a precision/resource rationale. Later validation must accept multiple correct implementations, detect ownership/order faults and expose missing/blocked observations. No such tests or baselines are built by this packet.

**Disposition and next action.** Ready for bounded feasibility review at package scope, with execution conditions outstanding. First passively bind one local and one coordinated requirement sketch to the pinned source owners and event paths; these are illustrations for a reviewable contract, not a two-task allocation. If a narrower mechanism cannot be isolated credibly, retain package attribution. If common requirements require rebuilding one style into the other, defer that pair rather than manufacture the contrast.

## R03 — History-assisted debugging and recovery

**Question and contrast.** What can an actual Nu history/inspection facility preserve and expose, at what cost, and can a fixed agent use it to complete a reproducible repair? The primary technical comparison is a selected supported retention/restoration workflow versus fresh initialization and reconstruction of the same declared state boundary. An agent repair extension compares access to that facility against ordinary declared debugging access within Nu.

**Facility boundary.** Start from the pinned Gaia undo/redo and World-copying leads. Determine whether the selected operation restores editor state, game state or both. Inventory represented values, entity identity, subscriptions, timers/pending actions, randomness/clocks, native handles and external effects. Label each as retained, reconstructed, invalidated, excluded or unknown with a source location. Do not rename editor undo as arbitrary game time travel or presume snapshot restoration migrates running code.

**Scenarios and information.** Prepare F-history with known versus unknown failing entity/event as a prespecified initial-information distinction, using separate task instances to avoid solution carryover. Separate fault localization, actual repair and resumed behavior. Add F-effect boundary cases only when the facility claims the relevant continuation. For an excluded irreversible effect, the useful result may be an explicit unsupported boundary rather than a failed promised rollback.

**Outcomes.** Technical restoration/continuation obligations, repair correctness, all-attempt elapsed/model cost, recording/instrumentation work, retained memory and replay/rebuild latency. The agent extension uses the shared endpoint. One known failure may be faster to fix without history; long retention or recording may dominate any diagnostic benefit.

**Evidence consequence.** [S42](literature/full-reading/S42-stream-debugger-comparison.md) supplies the information-dependent package reversal; [S66](literature/full-reading/S66-omniscient-debugging-behavior.md) distinguishes reruns from diagnosis success; S296/S297 distinguish represented-state exploration from replay under changed code. [S235](literature/full-reading/S235-mio-reversible-io.md) and [S107](literature/full-reading/S107-remote-concolic-debugging.md) supply restricted compensation/replay alternatives. None establishes the chosen Nu effect contract.

**Disposition and next action.** Conditional on the exact state/effect contract and real agent access. First passively trace one supported undo/restore operation and its mutable/native references, then inventory the already available observation interface. Keep the agent extension deferred if access would require an unapproved adapter or an observer that solves the task. A mechanism/cost comparison can remain useful without a human or agent productivity claim.

## R04 — Domain modeling and evolution

**Question and contrast.** The immediate bounded study retains [D1](fsharp-domain-evolution-research-proposal-2026-09-16.md): explicit enumeration of current cases versus an initially behaviorally equivalent catch-all in the same pinned implementation, for one fixed coding-agent policy. Both arms can be compiler-exhaustive. Richer domain modeling remains a separate broader question because it can change APIs, names and modeling work.

**Tasks.** Use F-domain-distinct, F-domain-default and changes without a case-set extension. Include temporal/lifecycle requirements that exhaustiveness cannot entail. Bind each targeted source site to its actual cases, payloads, guards, branch behavior and frozen compiler/warning policy. Keep the diagnostic-opportunity record separate from the requirement-to-observation record; neither site count nor warning count measures satisfied obligations.

**Controls and outcomes.** Keep engine, APIs, dependencies, names/comments and helper organization shared as far as the convention allows, recording unavoidable branch/token differences. Never insert a present-day bug into the fallback arm or force token equality. Use the common all-obligation endpoint and all-attempt resource accounting. A correct catch-all or safe reorganization is valid; a compiling explicit branch with incorrect behavior fails.

**Evidence and rival.** P08, S34–S37, S72 and the completed type-evolution readings in the [index](literature/full-reading/INDEX.md) constrain novelty and diagnostic claims. Additional source/diagnostic information might help, add redundant work or still miss temporal obligations. The total source-convention effect includes those consequences; do not adjust on successful compilation/diagnostic exposure to claim a pure type mechanism.

**Disposition and next action.** Ready for bounded feasibility review under the existing D1 conditions. Identify an authentic equivalent fallback site and prose requirements covering a useful extension, a valid-default extension and a compiler-silent obligation. Later authorized checks must establish initial equivalence, actual diagnostic opportunities and oracle sensitivity. If no legitimate source convention or consequential decision exists, redirect. Preserve the original D1 protocol/provenance; this packet neither substitutes MMCC/ImSim as its arms nor rewrites it as a steering experiment.

## R05 — Correctness of interactive change

**Question and contrast.** Which declared observations warrant an all-obligation pass, and where do weaker observations miss relevant behavior? This is the shared evaluation specification. A separate methods contribution would compare observation policies on independently justified behavior/fault cases, including the cost of specifying and observing them.

**Proposed policy comparison.** Treat compilation plus ordinary development-test agreement as a restricted observation policy, and the explicit obligation contract as a stronger candidate. Keep their exact included predicates visible; do not assume that a richer monitor is automatically correct or complete. Reference behavior is justified independently through requirements, source reasoning and diverse valid/invalid traces, not solely by the same monitor or candidate logic being assessed.

| Obligation class | Required observation specification | Adverse or inconclusive case to preserve |
| --- | --- | --- |
| State/output | Required values/relations and allowed alternatives at a named boundary. | Correct compilation with a wrong state update; representation changes that preserve behavior. |
| Identity/lifecycle | Creation, deletion, ownership and permitted reuse; observer/subscription lifetime. | A stale event reaches a replaced entity, or valid identity behavior differs from the reference's implementation. |
| Temporal response | Trigger, clock/event-order convention, permitted order and justified deadline/horizon. | Wrong order, cancelled action, absent trigger or a bounded trace that cannot establish eventual progress. |
| History/recovery | Start/checkpoint state, pending obligations, retained observations and restored external boundary. | Present values match but a pending obligation is lost; replay repeats an irreversible effect. |
| Effects | Permitted multiplicity/ordering and observable host boundary. | Duplicate or omitted effects; an unobserved environment makes the result inconclusive. |

**Endpoints and validity.** For later labeled cases, report false passes, false failures, inconclusive rates and per-class sensitivity alongside construction/observation cost. Establish a meaningful case denominator and lineage; generated variations of one fault are not independent external validation. Exercise evidence is needed for success obligations: a missing trigger is not automatic completion. Program failure to reach a required trigger differs from evaluator inability to observe it. Unknown observations do not become passes.

**Evidence consequence.** [S294](literature/full-reading/S294-industrial-game-regression-testing.md) supplies industrial observation/recovery constraints; [S281](literature/full-reading/S281-game-monitoring-thesis.md), S47/S53 and S220/S222 supply temporal and testing boundaries; S298 records configured/excluded checks; S299's preservation theorem depends on valid models and relevant boundary exits. These are tools for specifying coverage, not a theorem that the new evaluator is sound. S42's generated agreement is narrower than an independent repair oracle.

**Disposition and next action.** Ready for observation-specification review; oracle validity remains a construction dependency. Write source-bound satisfying, violating and inconclusive trace sketches for the R02/R03 contracts before proposing tests. Later checks must accept an alternative correct implementation and detect plausible order/history/effect faults. No tests, mutant implementations or executable monitor are constructed here. Demote a standalone methods-paper claim if the work only instantiates an established technique without a consequential new result.

## R06 — Runtime and state-retention costs

**Question and contrast.** At matched useful work, how much do a selected Nu retention/coordination policy and its observation facilities cost? The first candidate is the same supported workflow with current-state operation versus a declared bounded retention history. It is eligible only if the source supports both policies without inventing a facility. A copying/imperative or cross-engine comparison has a different contract and must be labeled separately.

**Workload specification.** Reuse the concrete R02/R03 behavior. Declare world size, changed-state fraction/rate, event fan-out, retained-history horizon, inspected/restored checkpoints and host/native resources. Choose boundaries that expose both low-change structural sharing and costly high-change/long-retention conditions, as source-grounded hypotheses. They are workload dimensions to justify, not an arbitrary large Cartesian product or a prediction that sharing always wins.

**Measurement plan.** Bind hardware, OS/runtime, build, dependencies, warm-up and useful-work count before later measurement. Report frame-time distributions/tails, allocation per useful update, managed and relevant native working set, retained memory, throughput and restore/rebuild latency. Use complete runs as the repeated measurement unit; frames within a run are correlated. Count observation overhead and record warm-up/steady-state separately under a rule fixed before outcomes. Record stalls and failed/unfinished work rather than presenting successful fast frames alone.

**Cost boundaries.** Include snapshot/root creation, referenced objects, history indexing, retention/disposal, GC and host/native work where relevant. Freeing managed references is not proof that native resources were released. A memory reduction can coexist with worse tail latency; a fast replay may require expensive input capture. Keep one-time integration and per-run resource cost distinct. Do not equate equal wall-clock duration, average FPS or source size with equal useful work.

**Evidence and scope.** [S238](literature/full-reading/S238-attribute-grammar-rendering.md) and [S239](literature/full-reading/S239-unity-mobile-optimization.md) supply workload/measurement trade-offs; [S248](literature/full-reading/S248-snowflake-manual-memory.md) has a distinct lifetime contract; S138–S151/S211–S214 and S237–S247 in the index cover representation/runtime alternatives. [S260](literature/full-reading/S260-unreal-energy.md) and [S261](literature/full-reading/S261-unity-unreal-energy.md) preserve workload-dependent power/engine findings. Those results do not calibrate Nu sample sizes or current performance.

**Disposition and next action.** Conditional on a source-supported retention policy and matched-work observation boundary. First inventory actual retained references and lifecycle/disposal paths for R03's selected operation, then prepare a measurement sheet and instrumentation-cost boundary. Later authorized repeatability/overhead checks determine resolution and run counts. If ordinary current-state and retained-history modes do different useful work, compare total cost to obtain the same required result or narrow the claim to the explicitly different services.

## Shared feasibility dependencies and falsification review

| Dependency | Affected claim | Next executable desk action | Later evidence required |
| --- | --- | --- | --- |
| D-source | Actual Nu capability and common initial behavior | Reinspect the pinned source paths for the selected ownership/history/retention contract; record any new pin and differences. | Supported environment and independent initial-behavior checks. |
| D-task | Relevance/diversity of maintenance tasks | Bind sketches to exact source/history/practice evidence, flag illustrative cases and remove redundant families before outcomes. | Feasible independent tasks/applications; claim restricted if only a local case exists. |
| D-oracle | Correct change and recovery | Specify satisfying, violating and inconclusive observations with independent requirements and valid alternatives. | Sensitivity, exercise and false-pass/false-failure checks under approved construction. |
| D-access | Agent use of relevant tools | Inventory actual existing interfaces and information/cost boundaries without a live probe or new adapter. | Separately approved compatibility/observation validation. |
| D-cost | Resource trade-off | Specify equivalent work and exact inclusion of retained/native/instrumentation/setup costs. | Repeatability, overhead and measurement resolution. |
| D-precision | Useful uncertainty and resource allowance | State the decision threshold needed, actual independent units and proposed paired/family estimand for review. | Justified sensitivity/precision and a separately authorized budget; no old allowance reused. |
| D-human | Human productivity or steering benefit | Retain R21 policies and source-grounded measurement candidates; distinguish actual review from AI synthesis. | Measurement reliability, task/person variability, participant design and separate authorization. |
| D-literature | A particular comparator/method or stronger novelty claim | Follow the exact primary/edition dependency in the continuation plan when it can change the design. | Actual required reading/coverage; access denial remains a gap rather than an exclusion on merit. |

Before later execution, the design must explain how it would report these outcomes: a correct fallback beating explicit cases; a local/coordinated crossover; known-fault history overhead; successful visible recovery with lost pending work; a valid reorganization unlike the reference patch; infrastructure missingness reversing a naive ranking; human rescue producing an otherwise successful artifact; and memory savings with worse frame stalls. These are specification-review cases, not executed tests or predetermined results.

The six proposals and agenda dispositions complete this preparation artifact. They do not complete the literature field or demonstrate feasibility. The immediate continuation is D-source/D-task for R02 and D-source/D-access for R03, using R05/R06's contracts, followed by any consequential primary reading. No experimental construction, candidate run, participant contact, added worker, new adapter or H execution is authorized by the packet.
