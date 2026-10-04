# S281 — Game monitoring: four cases, temporal verdicts and cost boundaries

**Reading date:** 2026-10-05 HKT. **Status:** complete institutional thesis, with bounded static comparison to the already inspected S280 source. No game, monitor, compiler or author code is executed.

## Identity and coverage

Simon Varvaressos, *Étude de faisabilité du runtime monitoring dans les jeux vidéo*, maîtrise en informatique, Université du Québec à Chicoutimi, January2014, [DOI10.1522/030622621](https://doi.org/10.1522/030622621). The primary title page establishes a master's thesis; Crossref's generic monograph label and July2014 OCR metadata do not change its degree or stated date. The [institutional PDF](https://constellation.uqac.ca/id/eprint/2791/1/030622621.pdf) contains87 PDF pages: twelve front-matter pages and printed1–75. All text is read, including52 bibliography entries; there are no appendices. Fifty-one targeted pages are visually inspected, covering all18 figures, all3 tables, all9 numbered game properties, the logic definitions/examples and seven blank pages. The scanned/OCR text loses operators and identifiers; consequential formulas and unknown table cells are checked against the original images.

Native collection `PKLXQNEE` was checked by DOI/title/edition before reading (310 parent records plus global identity searches). Parent `2IXS2XZF`, note `PAVDIEL7`, PDF `ZNGSJWM2`. The3,063,571-byte PDF has SHA256 `cc0f1c799b84673550a74ed135f60b8270cf9f0bc1023ba786bfa17ae90eeeca`; attachment bytes, membership, object versions and exact final note are verified through the local API. No JavaScript-window or GUI operation is used. Copyrighted bodies, extraction and renders remain outside Git.

## What is demonstrated

The thesis reports successful checking/detection in four games and no observed gameplay lag under its conditions. It connects a formal temporal specification to actual exported game observations and distinguishes two integration paths. These are useful feasibility results. Neither automatic play nor comparative tester-time savings is demonstrated.

| Game and primary location | Integration and fault selection | Evidential scope |
| --- | --- | --- |
| Infinite Mario, pp.47–50 | Java; manually emitted action events; monitor added and compiled into the game. Faults introduced by changing/deleting code; three properties shown. | Constructed demonstration, partly following Mayet's earlier Mario work. The height-under20 rule is explicitly artificial: ordinary gameplay can legitimately exceed that screen boundary. Its violation is a monitor demonstration, not independently established bad design. |
| The Timebuilders: Pyramid Rising2, pp.50–52 | Commercial BlooBuzz/Québecor Média game, Unity3D/C#, PC/Mac/tablets. Collaboration enables code access; manual event instrumentation and embedded monitor. Previously fixed developer problems deliberately reintroduced. Five properties developed, two shown. | Genuine commercial-game access and historical problem provenance strengthen applicability. They do not establish new production bug discovery, independent fault sampling, sustained adoption or saved developer effort. The Java-monitor/C# integration details are not reconstructed by this account. |
| Pingus, pp.53–56 | C++; game-loop state snapshots through `cpptempl` and a pipe to an external monitor. Seeded faults. Two properties shown. | Centralized instrumentation is reported much quicker than an estimated100-plus action sites, without a timed comparison. The thesis says one implementation file; the conference also mentions its header. Exported fields and integration work remain necessary. |
| Bos Wars, pp.56–59 | C++; snapshots from `mainloop.cpp`, separate monitor/pipe. Two properties concern historical tracker faults. | Demonstrates checks for actual previously reported problems. There is no held-out defect-recall or false-positive denominator; one printed tracker ID conflicts with the conference. |

Printedp.5 explicitly links the work to the2013 and2014 publications. [S280](S279-S280-game-runtime-monitoring.md) names five games: three overlap this thesis, while Pacman Canvas and Chocolate Doom replace its commercial case. Four thesis games plus five conference games are not nine independent cases. S279's six-game journal body remains unread; its roster cannot be inferred by taking the union. [S277/S278](S277-S278-mayet-runtime-repair.md) supplies the distinct host-repair contract and earlier demonstration lineage.

## Temporal and observation contract

**The inconclusive outcome is explicit**, not a missing concept inferred solely from source. Sections3.3.3–3.4, pp.33–36, explain why a global next-event requirement can fail on a finite prefix but cannot become definitively true while more events remain possible. An unbounded eventual response can remain inconclusive indefinitely. The example `qpq` does not settle `G(p → Xq)`. Ending acquisition therefore needs an explicit application policy before unfinished obligations can count as failures or successes. This resolves a primary-reading gap, but supplies no experiment-specific level-ending rule for the conference's omitted eventual-basher formula.

The two instrumentation paths also use different observation clocks: next exported action event versus next game-loop snapshot. Neither `X` alone means a duration in milliseconds. Keeping an object's identifier, exporting every required field, observing disappearance, and retaining the monitor's history are separate requirements.

| Printed property | Reconstructed condition | Qualification from the actual formula/context |
| --- | --- | --- |
| 1, p.49 | All reported jump heights stay below20. | Author-selected artificial bound; missing height fields are not a positive observation of height. |
| 2, p.49 | Enemy-fireball-death action is followed by fireball-disappear in the next message. | Adjacent event order is checked; this displayed formula does not correlate a particular fireball identity. |
| 3, p.50 | After a winged stomp, the next message must not report death for the captured enemy ID. | The antecedent universally quantifies a filtered field; an empty filter is not proof that a winged stomp occurred. The consequent concerns the next exported message, not the next matching event at arbitrary distance. These are static specification distinctions. |
| 4, p.51 | Once an elephant upgrade occurs, no further upgrade may occur in the remaining monitored trace. | Prose intends once per level. The formula has no level identifier; correct reuse requires a level-scoped trace/reset policy that is not specified here. |
| 5, p.52 | Cancellation starts a next-message/Until condition involving `CharacterStateWaitingOrder`. | The printed left predicate is **not waiting until waiting**, while prose forbids entering other states before waiting. Its first XPath tests existence of `objectID` without binding it to the canceled entity; the second uses the captured ID. The displayed formula does not establish the stronger prose claim. No actual monitor run or failure rate is inferred. |
| 6, p.55 | Bind deadly velocity, then require a too-fast falling character's next exported state to be falling, drowned or splashed. | This is a next-snapshot allowed-state condition, not an independent eventual-death proof. An absent next entity needs its own policy under universal quantification. |
| 7, p.56 | A faller must not be a bomber in the next message. | The original typeset XPath has an empty `id =` operand. This is an actual publication omission, not merely OCR loss; do not silently repair it or treat it as proof of the executable formula. |
| 8, pp.58–59 | A repair target must not simultaneously be a resource-harvesting target. | Thesis and conference both associate the description with bug29095; one of the two previously inspected public Bos Wars formulas supplies this condition. |
| 9, p.59 | New resource orders must not target a building. | Thesis labels this29765; conference labels the matching description37861 and uses29765 for jet fighters. The other inspected public formula corroborates the order/building condition, not the disputed tracker identity. |

Official Savannah pages29095/29765/37861 were attempted through web opens and ordinary HTTP; access failed/reset. Three exact-domain searches returned no results. Keep the issue-ID discrepancy unresolved rather than choosing a number or denying the historical bug. Bibliographic context for XPath2.0 second edition, the2007 Tracematches chapter, the2009 BeepBeep chapter and the2001 ECOOP AspectJ chapter is kept separate from differently dated works in S280.

## Measured cost and extrapolation

Table4.1, p.60, specifies Intel Core2Duo P7350 at2GHz,4GB, GeForce GT130M and Ubuntu12.04LTS64-bit. Event emission differs greatly: Mario2.9/s versus Pingus167/s. Pingus displays40frames/s, so monitor-message rate is not display rate. Table4.2's Pyramid frame-rate cell literally contains question marks; code size is unknown.

| Table4.2 game | Reported frame rate | Reported overhead | What §4.4.2 includes |
| --- | --- | --- | --- |
| Infinite Mario |24fps |approximately1.5% |Instrumentation **and embedded monitor** |
| Pyramid Rising2 |unknown, printed `??` |approximately5% |Instrumentation **and embedded monitor** |
| Pingus |40fps |approximately6.7% |Instrumentation only |
| Bos Wars |30fps |approximately7% |Instrumentation only |

These percentages cannot rank architectures or languages with an equivalent whole-system cost boundary. The thesis preserves a favorable feasibility observation, while the exact instrumentation/monitor preparation budget and net tester-time effect remain unmeasured.

The Pingus account reports2seconds instrumentation CPU time for5,000 events (0.4ms/event), about700bytes/event and approximately120KB/s. An uninstrumented179updates/s,39.4fps illustration and capacity above50 properties at60fps are **derived estimates**, not matched whole-game comparisons or an observed50-property workload. Figure4.13, p.63, contains two cumulative timing curves: about0.13ms/event for the simple all-alive condition and an early0.3ms/event region for the more complex falling condition, becoming cheaper as its quantified domain empties. Those stated values overlap the conference account; no trace identity establishes an independent repeated measurement.

The thesis reports a zero input buffer and immediate feedback in its tests, without a latency distribution. The already inspected later public revision's GUI/counter discrepancies in S280 prevent treating its display or selected timers as the exact thesis measurement procedure. Preserve the paper's positive results and that version boundary. Parallel monitor execution and automatic tracker filing/deduplication remain proposed extensions.

## Consequence for Nu and the survey

A compact state representation can make a monitor convenient to integrate, but exported state, correct predicates, complete temporal history and appropriate termination determine what it actually checks. Formal notation and successful selected-fault detection do not certify every prose requirement. Conversely, the scoped commercial-game and selected-fault successes are positive evidence for practical monitoring; they should not disappear into a catalogue of reporting limitations.

For Nu, compare actual observation coverage, monitor/state lifetime, integration work and consequential defect/change outcomes. Neither this thesis nor its overlapping conference establishes Nu-specific net value, a language effect or arbitrary successor-state preservation. A responsible residual empirical question is different from an unread method.

The next stronger independent gap is NCAlt (DOI10.1145/3549508), retained from the SuBViS/BPAlt lineage: resolve how alternatives are represented/compared, which game states survive a switch, and what its evaluation measures. Reuse the now reconstructed monitoring method; retain the2013 predecessor conditionally for a specific missing formula or implementation question, S279/S280 access/version gaps, and the wider practice, architecture and type-evolution frontiers. No construction, recruitment, new worker or experiment follows.
