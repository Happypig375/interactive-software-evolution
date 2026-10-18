# Practice evidence and task eligibility

**Decision, 2026-10-11:** use the existing Nu cases as a source-grounded, purposively chosen mechanism set. They do not yet constitute a representative maintenance workload or a demonstrated adoption opportunity. This R14 preparation connects the cases to actual requests, contrary practice evidence, beneficiaries and missing work. It supports the [study designs](nu-research-study-designs-2026-10-08.md), without adding mandatory arms or changing [PLAN's holds](../PLAN.md).

The most consequential addition is **asset and engine-upgrade work**. Existing code-focused cases can miss copying, configuration, customized defaults, derived representations and integration. Preserve that gap when interpreting a result; promote an asset case only when it changes a practical decision and its common behavior can be specified. Gameplay history also needs a particular beneficiary and avoided reconstruction burden, rather than a general claim that developers need undoable gameplay.

## Evidence and units

Three GitHub searches cover `reload` in issue titles/bodies, `undo` in titles/bodies and `asset` in titles, within `bryanedds/Nu`. Each requests 100 results on page 1, ordered by creation date descending. They return 38, 17 and 28 positions, respectively, all with `incomplete_results=false`: **83 positions, 71 distinct issues**. All titles were screened; fourteen complete bodies and their twelve comments were read. These exact query ranges are exhausted, not the repository, other spellings, discussions, pull requests or the wider population. Seventy issues were opened by `bryanedds`, one by `Happypig375`; issue counts therefore cannot stand for independent users or a demand ranking.

The selected current wiki page and two propagation scripts were read in full. Nu code remains pinned to `064f7ae92a8506689cd91aff5e6804a375d6ef3d`; the separately versioned wiki is pinned to `263b0a2c898ef8ae711b669cb9db2c345c69df7d`. The [search ledger](literature/nu-background-searches-2026-09-30.md) records access, exact coverage, hashes and dispositions. No new paper/PDF reading, Zotero write, source execution or participant observation is credited.

An issue is a public account or proposal. Its body, comments, patch, affected release and observed behavior are different evidence. A closed label does not establish a fix, and an open request does not establish that a capability is absent at the research pin. Retain issue/thread identity across derived tasks; a withdrawn report remains useful counterevidence to its title.

The completed practice readings contribute complementary, bounded evidence:

| Existing primary reconstruction | Consequence for task selection and value claims |
| --- | --- |
| [S250](literature/full-reading/S250-game-industry-problems.md)/[S251](literature/full-reading/S251-game-problem-dataset.md): selected postmortems and their changing dataset | The two editions reuse the same 200 game identities. Mechanics, assets, developer iteration, tests and coordination interact; useful automation and engine reuse coexist with infrastructure and later-requirement costs. Coded entries are neither prevalence nor work hours. |
| [S266](literature/full-reading/S266-game-development-problems-reading-2026-10-15.md): unreviewed extended-postmortem preprint | The merged 267-document corpus reuses the S250/S251 200-postmortem baseline and adds 67 retained documents with 300 claimed problem instances; it is an expanded lineage, not an independent replication or 267-document addition. Its strongest usable result is source-conditioned task discovery: 14 Game Developer postmortems, 25 Reddit accounts and 28 GDC talks have markedly different production, feature, people and business profiles. Period and source/context change together, so the aggregate shift is not a clean longitudinal effect. Baseline totals of 927 versus 1,000, displayed extension totals of 297 versus 300, unsupported effect-size denominators and nested instances prevent carrying exact magnitudes or significance forward. |
| [S252](literature/full-reading/S252-game-practitioner-comparison.md): interviews and comparative organizational survey | Cross-discipline communication and changing requirements matter. Several architecture/reuse/debt predictions remain inconclusive, and one scripted-testing prediction reverses. A comparison should not presume universal game-specific difficulty or absent automation. |
| [S253](literature/full-reading/S253-tools-expectations-reading-2026-10-15.md): 27 role-structured sessions in seven Finnish game organizations | Existing infrastructure was generally acceptable while bugs, lost work, restrictive editors, extension and migration concerns remained. Compatibility, platform and asset integration, prototyping and change during production are situated requirements; mature third-party engines, assets and familiar editors are ordinary alternatives. The study supplies neither a unique-participant denominator nor observed task effects. |
| [S254](literature/full-reading/S254-game-reuse-reading-2026-10-15.md): two studios, five projects and four developers | Prefab, script, editor and asset reuse supplies real configuration and maintenance beneficiaries. Favorable designer/level-editor accounts coexist with setup expertise, redundancy, propagated errors, technical debt and dead prefabs. The reported 2–5 percent cross-project reuse is an unresolved participant estimate, not measured savings or prevalence. This is the same work lineage as the earlier preprint/package, not additional studios or games. |
| [S267](literature/full-reading/S267-ubisoft-change-propagation.md): one infrastructure intervention | Preparation, temporary coexistence, incident recovery and work shifted to other teams are part of the intervention. Favorable recovery and optimization reports coexist with a slowdown; no numerical net saving is supplied. |
| [S269](literature/full-reading/S269-unlimited-rulebook-architecture.md)–[S271](literature/full-reading/S271-rulebook-thesis-and-methods.md): overlapping architecture/course lineage, three jam games and four professional accounts | Preserve inconclusive course outcomes, useful cross-cutting mechanisms, learning/coordination costs and familiar alternatives. Professionals sometimes judge retaining a costly legacy mechanism cheaper than refactoring. Publications, games and participants are not interchangeable units. |
| [S288](literature/full-reading/S288-collaborative-arvr-practice.md): 26 professionals in overlapping roles | Direct engine prototyping can help while making artifacts less editable by a designer. Access to devices, mutual training and negotiation matter. The accounts supply situated requirements, not a Nu role-productivity estimate. |
| [S289/S290](literature/full-reading/S289-S290-game-practice-methods-partial.md): New Zealand studio survey/interviews | Reported activities can differ from process labels; useful adaptations coexist with communication and maintenance problems. Smallest studios are excluded, sample overlap is unresolved, and workflows were not independently observed. |

[S268's review](literature/full-reading/S268-industry-scale-game-software-review.md) broadens discovery but does not turn its 98 publications into 98 independent industrial interventions. At the 2026-10-11 checkpoint, S266's expanded corpus remained access-limited, so no expanded prevalence or corpus-overlap claim followed from its abstract. Reusing these reconstructions adds no publication count or repeated citation-screen credit.

**2026-10-15 continuation:** S253, S254 and S266 now close their selected final-PDF and visual gaps at the scopes above. S253/S254 broaden the practical basis for tool-package fit, asset/editor integration and within-project prefab maintenance while preserving strong existing alternatives and adverse reuse costs. S266 adds source-aware discovery across edited trade-postmortems, independent/small-studio Reddit accounts and established-studio conference talks. A selected task should retain the source stratum, beneficiary, represented artifact and outcome instead of citing an aggregate rank. The paper's constrained machine proposals followed by author/expert adjudication can organize the corpus, but proposal acceptance is not independent reliability and no time, cost or comparison supports the claimed coding-efficiency benefit. None of these readings establishes a representative workload, common-task frequency, Nu demand, causal trend or empirical Nu benefit.

## Public accounts that change the task frame

| Source and actual reading | Consequential interpretation |
| --- | --- |
| [#1232](https://github.com/bryanedds/Nu/issues/1232), body and one comment | The reporter withdraws the tilemap-reload complaint after realizing the file was unsaved. Do not assign its title as a confirmed reload defect. An authored saved/unsaved workflow case would have different provenance and success conditions. |
| [#1411](https://github.com/bryanedds/Nu/issues/1411), body and one comment | The maintainer says the build likely targeted Gaia rather than Nu.fsproj. This is a tentative correction, not a reproduced build trace or confirmed redundant-build defect. Exact project/target and setup belong in a cost claim. |
| [#359](https://github.com/bryanedds/Nu/issues/359), body and two comments | The initial proposal questions gameplay undo's usual value; a later comment favors functional mode despite a reported approximately 33% performance loss in a historical Scenery case, then closes the proposal for now. Preserve both judgments. This is neither a current benchmark nor proof that imperative mementos were implemented. |
| [#716](https://github.com/bryanedds/Nu/issues/716), body and one comment | Operational imperative undo and a user-supplied mutable-array snapshot hook are proposals. The author reports an unsuccessful earlier manual-divergence attempt. The thread does not establish shipped support or full gameplay recovery. |
| [#396](https://github.com/bryanedds/Nu/issues/396), body and four comments | A historical example describes a binding cache failing to propagate after undo/resume; discussion ends with a fix report. It motivates observing resumed behavior beyond restored values. No closing patch/current defect is reconstructed here. |
| [#917](https://github.com/bryanedds/Nu/issues/917), [#953](https://github.com/bryanedds/Nu/issues/953), [#979](https://github.com/bryanedds/Nu/issues/979), [#1222](https://github.com/bryanedds/Nu/issues/1222): all bodies and #979's one comment | Conversion assistance, eager/lazy timing, visibility of added properties and unwanted reset are concrete concerns. #979 says done and #1222 is closed; neither supplies a validated present task. The eager-conversion latency concern is a prediction. The existing [R10 source contract](nu-live-edit-contract-2026-10-11.md) governs actual fallback/default behavior; an issue's wording does not establish a general migration hook. |
| [#808](https://github.com/bryanedds/Nu/issues/808), body and one comment; [#1407](https://github.com/bryanedds/Nu/issues/1407), full body | Default-asset updates, local changes, version/provenance checks and multiple projects create a real upkeep question. #1407 proposes layered resolution and asset-graph merging tied to a future bundle design; it is not an implemented comparator. |
| [#1260](https://github.com/bryanedds/Nu/issues/1260), body and one comment; [#1408](https://github.com/bryanedds/Nu/issues/1408) and [#755](https://github.com/bryanedds/Nu/issues/755), full bodies | Cube-face invalidation, moving generated navigation files into project assets, and geometry/physics refresh motivate work across representations. #1260 explicitly concerns live reload; #755 is a conditional 3D request whose closure gives no implementation explanation. No current broken scene or common cross-engine behavior is established. |

### Existing asset automation and its boundary

The old #808 wiki link could not be retrieved, and its raw filename returns 404. A public wiki Git inspection recovers the current [Updating User-Created Projects on Engine Updates](https://github.com/bryanedds/Nu/wiki/Updating-User%E2%80%90Created-Projects-on-Engine-Updates) page at the pin above: all three lines, 821 bytes, SHA256 `7aecfabe25f3df015f3619a2a1eae0bfec6f057b4bfab1cad08e12b95036365b`. The changed title/path is a recovered current route, not verified rename history or proof of what the 2024 page said.

The page already recommends propagation scripts and describes Gaia defaults as the source of truth; it separately mentions resetting a changed editor layout. At the Nu pin, [Linux lines 1–16](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/PropagateDefaultAssets.Linux.sh#L1) and [Windows lines 1–19](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/PropagateDefaultAssets.Windows.bat#L1) enumerate engine/template/project destinations and copy from Gaia. Thus an open automation request cannot justify an automation-absent baseline.

The scripts contain no comparison with an earlier upstream version or policy for retaining deliberately customized defaults. Their literal operations also do not establish the wiki's broad clean-replacement description: the Linux deletion argument contains a quoted wildcard; Windows uses file deletion/copy patterns without a recursive directory-copy operation. Actual selected files, failures, stale files and destination results remain unexecuted. Preserve platform-specific correspondence and count inspection/reconciliation work; do not silently repair these scripts or execute them as a research check.

An **optional asset-upgrade case** would specify the old/new engine and default editions, local customizations, required new functionality, permitted deletions and asset-graph mappings before selecting a solution. Plain propagation may be appropriate when no customization must survive; manual reconciliation or another ordinary supported method can be valid when it must. Existing valid customizations, obsolete defaults and genuinely new required assets need separate outcomes. A newer timestamp, successful copy or visual refresh alone cannot certify integrated behavior. The case is conditional preparation for R01/R06/R17, not a new mandatory direction or experiment.

## Provenance of the proposed families

| Existing or conditional family | Basis and intended work | Selection and transfer boundary |
| --- | --- | --- |
| Local controls, pause/exit and staged policy changes: R02/R09/R13 | Authored control changes; #1145 supplies verified historical lineage for an adapted lifecycle requirement in the [source audit](nu-source-contracts-and-scenarios-2026-10-11.md). | The shipped quit guard is already present. A sequence of authored requirements is not an observed longitudinal user history. Keep independent, coordinated and legitimate no-change/default cases. |
| Platforms and gravity: R01/R02 | #1020/#1109 and the [diversity](nu-task-diversity-and-common-requirements-2026-10-11.md)/[platform](nu-platform-contract-2026-10-11.md) contracts connect requests to an application boundary and ordinary alternatives. | Requests establish relevance, not baseline equivalence, carrying behavior or prevalence. Record adaptation/alignment work and mismatches. |
| Distinct/default domain cases and projectile lifetime: R04 | Authentic source sites with authored successor requirements. | Technical probes of diagnostic guidance; no specific customer requested the selected command or reward. Correct catch-alls and no-case-extension changes remain valid. |
| Event bursts, contact/score and external effects: R02/R05 | Source differences plus reconstructed coordination/temporal methods. | Specify intended multiplicity and effects independently; two legitimate game designs are not automatically correct/defective variants. |
| Same-code history and continuation: R03/R06 | Inspected roots/native rebuilding, the selected [B0/B1 case](nu-history-application-contract-2026-10-11.md), useful S296 practice and the mixed historical accounts above. | Identify whose reconstruction is avoided, how often the selected workflow needs it and what continuation matters. Repeated restores of one prepared state do not establish broad demand. |
| Changed-code reward/schema retention: R10 | Source-bound conversion and authored mappings, now related to actual conversion/reset concerns. | The particular brick-reward edit remains authored. Existing progress, successful defaults and new-round behavior differ; no runtime preservation or productivity result follows. |
| Entity-tree reuse, title-scene handoff and role access: R11/R12/R20 | Existing artifacts and authored configuration/revision/rename cases; S288 supplies independent accounts of representation and handoff burdens. S253 adds ordinary engine/editor/asset-package practice, and S254 adds situated prefab configuration, designer tooling and maintenance burdens. | No actual Nu designer/team request or dedicated semantic-merge treatment is established. The S253/S254 accounts are purposive reports rather than task-frequency or effect estimates. Credit ordinary prefab/scene, Blueprint and helper/composition alternatives. Default-asset propagation is a separate facility from entity-tree propagation. |
| Setup, documentation and learned work: R07/R20 | Existing #1015/#991 accounts and the [learning contract](nu-learning-and-role-contract-2026-10-11.md), with professional practice reconstructions. | Report prerequisites, help and failed readiness. A maintainer-authored starter task does not establish an accessible non-programmer workflow. |
| Engine/default/derived-asset upkeep: conditional R01/R06/R17 | The new public accounts, recovered wiki and existing scripts above. | Exposes omitted work beyond source edits. Exact editions, valid customization policy and supported application/observation remain dependencies before selection. |

R08 supplies executor information/feedback rules; it does not add independent task provenance. R15 remains held, R16 retains the historical transfer and compactness counterevidence, and R18/R19 still need a real distributed or platform/energy use case. R21 remains future steering research. These families are not equal-weight strata or an all-factor design.

## Eligibility, missing people and the next decision

For each selected task, preserve **source/thread and edition; original need and beneficiary; historical/authored/adapted status; predecessor/patch correspondence; initial behavior and access; exact changed/retained obligations; valid alternatives; included assets and integration work; inclusion reason and strongest adverse case**. Record what has actually been verified. A concrete patch lineage can make a historical task reconstructable; it does not make the old defect present at the current pin. A withdrawn report can motivate a different authored workflow question but must retain that transformation explicitly.

Choose the source/task frame before candidate outcomes. Family and application labels must reflect substantive demands, not repeated wording or two styles of one game. Keep all selected failures and exclusions with their timing/reason; neither successful compilation nor successful agent completion determines entry into the workload. Technical preflight exclusions also narrow the target population and must remain visible. A common allowance does not make unequal setup, assistance or supported operations disappear. The [information contract](nu-agent-information-and-feedback-contract-2026-10-11.md) keeps source/requirements available to candidates separate from successor solutions and final scoring.

The near-term population is explicitly **these selected F# interactive-application changes in the specified Nu workflows**, with adoption/package comparisons conditional on common requirements. It excludes a claim about all game studios or the economics of 2027 development. Public discussion is actual human input; it is not our participant evidence. The user's preference for human steering guides the practical research objective, while its effectiveness remains unmeasured. Repeated prompts or additional AI reviewers would not supply independent beneficiary coverage.

Missing perspectives include independent Nu adopters and abandoners, less experienced F# users, artists/designers working without a specialist beside them, production QA/release and asset maintainers, very small/cancelled projects, and teams targeting different hardware or longer-lived commercial services. Existing professional studies illuminate some of this work under their own sampling limits; the current Nu issue frame does not fill it. Document this omission instead of compensating with issue counts or assuming every role wants the same mechanism.

**Next:** use this provenance/eligibility record when choosing the practical decision behind a separately reviewable feasibility case. R03/R10 especially need a stated beneficiary and avoided reconstruction burden; an asset-upgrade case is worth promoting only if its total-work question changes the adoption assessment. Broader adoption/population claims need an expanded independent source frame and, where necessary, later authorized participant work. Continue a named accessible primary/source gap when it can change that decision; repeating these narrow searches or creating more cosmetic tasks would not resolve it. No construction, recruitment, adapter, extra worker, model probe or candidate execution follows; new allocation remains zero.

## 2026-10-18 R12 artifact-backed revision preparation

The [Terra Firma family continuation](nu-reuse-and-authoring-contract-2026-10-11.md#2026-10-18-existing-terra-firma-family-and-next-revision-case)
now supplies an existing project artifact behind a concrete R12 candidate:
32 linked palms with placement/scale variation across four Villa trees. The
game's source loads this scene; a new successful load has not been observed.
This closes an artifact-provenance gap left by the initially authored GUI
family, without establishing a designer request, prevalence or savings.

A shared foliage tint revision, with a separately authored local roughness
condition, remains an **authored task on an existing artifact**. The relevant
beneficiary is a level author maintaining placed props. S254's already-read
accounts support the general configuration/maintenance concern, not this
specific requirement or its expected effect. Preserve the difference between
supplied existing links/history and the cost of constructing a new reusable
family. Ordinary batch field updates and parameterized composition are valid
alternatives with different setup/integration burdens.

Eligibility next depends on actual unchanged-scene loading/save/reopen,
equivalent starting information, the exact override policy and observations
of all affected configuration, including ancestor reconstruction. Source
whole-record comparison predicts a potentially adverse field-update case;
it does not establish a runtime failure. These additions prepare local
feasibility without allocating candidates or participants or resuming the
returned R02/R10 gates.

## 2026-10-18 continuation: material revision rationale and observed limits

The [unchanged Terra Firma scene](nu-terra-firma-reopen-feasibility-2026-10-18.md)
and [four revision/reopen pairs](nu-terra-firma-revision-feasibility-2026-10-18.md)
now supply the native observations that were still missing in the preparation
entry above. Both shared cases deliver the tint; propagation with the selected
local roughness preserves that choice but misses the same palm's tint. The
first batch/local attempt fails input integrity before editing and has no
material outcome. Its later revalidated continuation delivers all 32 tints and
preserves local roughness, declared configuration, links and old histories.
Preserve the invalid startup and its ineligible reopen alongside the separate
accepted continuation in the [integrity record](workspace-integrity-return-2026-10-18.md).

A new bounded public-source check supplies a closer **maintainer rationale**
for this task. It does not turn the particular tint/roughness requirement into
an external request. The [search ledger](literature/nu-background-searches-2026-09-30.md#2026-10-18-r12-propagation-practice-and-material-intent)
records exact retrieval ranges, reading depth and considered-source decisions.

| Primary account and coverage | Consequence for R12 | Limit |
| --- | --- | --- |
| [#725](https://github.com/bryanedds/Nu/issues/725), body and three comments | A shared-material proposal would make one edit affect referring entities, while requiring cloning and serialization support. The maintainer later judged entity-structure propagation sufficient for that need. This directly grounds shared material revision as an intended use. | A maintainer's design judgment supplies neither observed user work nor a promise about preserving one field while changing another. |
| [#186](https://github.com/bryanedds/Nu/issues/186), body and six comments | Persistent edits to prefab children were explicitly discussed as deltas applied after instantiation. | The design changed, and the maintainer also reported no personal need for that general feature. Retain this contrary account; do not infer demand from the initial proposal alone. |
| [#335](https://github.com/bryanedds/Nu/issues/335), body and fifteen comments; [#574](https://github.com/bryanedds/Nu/issues/574), body and five comments | Nested composition retained a property-delta problem; manual delta updates and synchronizing unchanged portions were proposed. These accounts justify making shared versus local intent explicit. | These are historical alternatives, including incomplete/archived work and a later change of approach. Their complexity/performance expectations are not comparative measurements. The external comment on #574 concerns skeletal animation, not this need. |
| [#729](https://github.com/bryanedds/Nu/issues/729), complete checklist, no comments | The intended propagation workflow includes retaining existing history on entity read, managing targets and distinguishing linked from unlinked duplication. | Checklist completion does not establish current source correspondence or behavior. |
| [#739](https://github.com/bryanedds/Nu/issues/739), [#745](https://github.com/bryanedds/Nu/issues/745), [#748](https://github.com/bryanedds/Nu/issues/748), [#946](https://github.com/bryanedds/Nu/issues/946), complete current titles/bodies and #745's one comment | Historical reports concern missed dispatcher changes, incorrect propagation links, history loss on save and child reordering. Keep these obligations separate from successful material delivery. | No fixing-patch lineage was reconstructed. These reports do not show defects remaining at the R12 pin. #748 has an empty body; its title is the entire account. The child-order report is distinct from R12's fresh timestamp-Order correspondence findings. |
| [#383](https://github.com/bryanedds/Nu/issues/383), title and three comments; [discussion #993](https://github.com/bryanedds/Nu/discussions/993), complete release body, no comments | A requested drag workflow and an announced Gaia Propagation Sources UI make authoring access and selection work explicit dependencies. | The release does not demonstrate the requested drag workflow or its usability. Public mechanism calls do not measure ordinary editor work. |

**The exact field policy remains authored.** None of these accounts specifies
that a local `RoughnessOpt` change inside `MaterialProperties` must permit a
later shared `AlbedoOpt` change inside that same record. The experiment
prospectively required that combination. Its missed tint is valid adverse
delivery against that requirement, not proof that Nu violated a documented
field-wise merge promise. Whole-material overrides are a plausible alternative
policy; a practical comparison must expose the chosen intent and count any
translation, selection and repair needed to deliver it. The later source
search does not retroactively change the frozen requirement or oracle.

All credited accounts are authored by the Nu maintainer. The search examined
34 distinct issue results and 11 distinct discussion results, plus one linked
issue; 13 complete issue threads (38 comments) and two complete discussion
bodies were inspected. The parent checked the decision-critical retained
texts. This narrows a provenance gap without establishing independent demand,
prevalence, authoring savings or steering effectiveness. Current bodies can
include later edits; unqueried vocabulary and other communities remain outside
this frame. The general prefab maintenance accounts in the already-read S254
remain separate evidence, not independent corroboration of this exact Nu task.

**Next:** retain the material case as an authored task on an existing artifact
with a specific maintainer rationale. The bounded storage prerequisite and
batch/local delivery question are now resolved. Bind a practical repair or
completion comparison with complete work and later history obligations before
any additional execution. Creating more cosmetic variants or counting related
issues will not resolve demand or benefit. The new evidence does not resume
the R02/R10 returns, authorize candidates or participants, or certify broader
propagation behavior.

## 2026-10-19 development-history follow-through

The [refined objective](nu-research-agenda-2026-10-08.md#2026-10-19-objective-improve-evolution-of-stateful-software)
promotes relevant repository history as supplementary evidence for selecting
an improvement and its baseline. For each consequential lineage, record:

- The originating need, reporter/beneficiary, complete relevant discussion and
  contrary or withdrawn accounts.
- Introducing/changing/reverting commits, their exact parents and diffs,
  linked pull requests/tests, and the affected release or research pin.
- The behavior actually reproduced before and after, with unexecuted claims
  marked as source inference; a commit title is not a behavior check.
- Existing workaround and alternative workflows, their observed or still
  missing costs, and whether the research task is historical or adapted.

Prefer lineages that can change R12's revision/override requirement or R03/R10's
recovery/evolution task. Existing maintainer-only accounts do not establish
independent demand, and the already-present #1145 workaround remains an
adaptation boundary. The later comparator must follow the practical decision;
Unity, Unreal, Godot and non-game implementations are candidate contexts until
relevant support and ordinary workflows are inspected. This addition records
future evidence requirements, not a new history search, experiment or source
reading. It does not resume the R02/R10 returns.
