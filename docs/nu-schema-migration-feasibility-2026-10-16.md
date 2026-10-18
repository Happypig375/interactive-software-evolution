# R10 explicit reward migration: feasibility record

## Question and current status

This separately assigned treatment asks whether ordinary application code can
introduce reward 200 when the old gameplay record lacked that field, retain
deliberate values of zero and 75, and handle repeated reloads and a failed
compilation notification without resetting progress. The
[prospective contract](../experiments/nu-r10-schema-migration/pre-execution-contract.md)
and [oracle](../experiments/nu-r10-schema-migration/oracle.json) were accepted and
frozen before source preparation. The executed migration application now
compiles, with its exact source checksum bound through the PDB to the resulting
DLL. Build 23 compiled the preceding observation probe against the original-schema predecessor.
Three harness candidates have failed independent pre-launch review; parent
inspection also rejected an intervening draft's unassigned rescue reload.
Four harness/conformance failures remain unresolved. Further construction has
now stopped at a separate objective-control return: attempts 11–18 failed
consecutively, crossing the required five-failure threshold at attempt 15.
Attempts 19 and 20 subsequently passed their included synthetic controls, but
those later passes do not authorize crossing the return. The current draft is
uncompiled and unaccepted; the last build remains 23. No native migration
process ran. This record publishes the accepted protocol/oracle and the return;
the unfinished implementation remains local. Ordinary continuation does not
resume this gate.

The preceding [initializer-only observation](nu-schema-reload-feasibility-2026-10-16.md)
remains a valid failed mapping: ordinary conversion produced zero despite the
new initializer of 200. The new treatment adds explicit application work and
cannot repair or replace that result. The
[source audit](nu-live-edit-contract-2026-10-11.md#2026-10-16-handler-installation-and-witness-storage)
binds the supported access and subscription route; source availability alone
does not establish its runtime behavior or practical value.

## Frozen comparison

| Case | Incoming state | Required first reward | Required one-hit score |
| --- | --- | --- | --- |
| M0 | Original seven-field model; reward absent | 200 | 300 |
| M1 | Eight-field predecessor; deliberately configured zero | 0 | 100 |
| M2 | Eight-field predecessor; deliberately configured 75 | 75 | 175 |

Six native processes are assigned: the three live cases, then their three fresh
required-state references. No native process has been accepted or run at this
preparation checkpoint. Each live case has a first migration, identical-source
repeat using actual inherited state, and deliberately invalid compilation. Its
one-step continuation and synthetic new-round diagnostic depend on valid,
preserved input. Fresh references explicitly reconstruct the required state;
they do not establish what live conversion supplied. Later results must retain
each delivery separately, including withheld phases and adverse predecessors.

The application stores a pre-conversion schema witness in a non-persistent,
integer screen property. It captures absence or presence before normal typed
conversion, allows normal content synchronization, then consumes the witness in
a new-typed reload message. Only the absent-field branch supplies 200. A zero
value after conversion is insufficient evidence of absence. The clear-before-
model-return policy has an explicit failure window; it supplies no transaction,
rollback or retry guarantee.

The protocol requires binding actual model, dispatcher and message types to each
returned FSI generation. They include the intermediate converted state, actual
handler counts, witness consumption and complete selected model/projection.
The failed-compilation control must exercise exactly one retained marker-zero
handler, not merely observe a notification and equal endpoints. A new-round
reset must invoke the current StartPlaying handler exactly once; matching final
counts alone could hide duplicate delivery.

Fully observed wrong mapping, extra/missed capture, stale marker, duplicate or
missing handler, wrong ordering and unwanted reset are evaluable mechanism
failures. Missing/corrupt observation, an observer exception, unbound identity,
deadline, cleanup failure or violation of the assigned zero-input/one-step
schedule instead limits validity. An explicit application
rejection is retained as an adverse outcome and withholds dependent phases.

A failed requirement alone does not withhold the remaining sequence. Before
the prescribed step, the seven checkpoint fields and selected projection must
remain preserved, the current reward must be an integer in [0,1000], and the
observations and source identities must be usable. Reward-only drift within
that range becomes the actual input to the following phase, without repair.
After the step, stability is judged against the actual resulting state; an
incorrect continuation cannot be hidden by suppressing its next observation.

## Oracle and review provenance

The oracle copies the earlier independent seven-field model checkpoint and
zero/200 continuation templates, plus its hash-bound, pre-reload projection
templates. Reward 75 changes only the declared score and score text. Baseline
projection properties originally came from direct scene getters before the
preceding reload; the post-step geometry was precomputed. This is independent
of the current run, but it remains a relative projection oracle rather than a
separate reconstruction of every scene constant.

Reset constants come from the pinned initial model and content. Random ball
direction, brick identities and colors are retained rather than predicted
across processes. The checker must compare every resulting model key, geometry
and color with its projection and reject remnants outside the new model. A
legitimately reused key is judged against the new model, not automatically
treated as a remnant.

| Frozen artifact | SHA-256 |
| --- | --- |
| Prospective contract | `382ab672344f766bd47250852c0729655b955e0a066097a0422993f7d723b1eb` |
| Independent oracle | `1bc0a29c71b77985774bd54ac151516acd51eba4fe86aebf28f7606aa42dccda` |
| Protocol review 01 | `fe4a2f30fa340b0ff5c6d44b53086d77b407b43f1dfb1d740bb3385e504ec00c` |
| Focused protocol review 02 | `18675a30f0e1ce37fac24f800f4a3d91b7e4b733d853c5b31d00d584b6fa6dc8` |
| Independent oracle review | `3c8f11d5baa5945726287b7546f8fe2b74d04a6fb8d65c4187c7a6cf91daa8b6` |
| Application-source review 01 | `f855bbc2e6e01321de18d17eb8047781301fc2f91d8768b9980f78bb728691fb` |
| Focused application-source review 02 | `fe3a84bea46855395a31267758a5acd7c46e3f81a3989e0c33b5e7422af83b6e` |
| Focused application-source review 03 | `69762b988880ba061f507080aa25caf8ed5fe158c98ece38c587744026c566ff` |
| Rejected harness review 01 | `fc661bf3301b8320fe8b36b60b627704b373585a4e199bac1ea8f3436015acc8` |
| Rejected harness review 02 | `6ee267b0843394751d8818a3a5c26adee8cd9dbfb82715b86c31c2d33a12fb68` |
| Review 02 decisive classification controls | `49d94ab339bd4c494c9b622c4ed37d09f19dfc887488166f2c63eedd2022e724` |
| Review 02 identity/pair-binding controls | `95fa8e7f46bbbe1d92d19934604b0a0c444c56190363b7db7fb9a57dcad3c42e` |
| Parent review 02 disposition | `800c16cc5433a7ebe44cb117fb22c0bc6fa21184f7dfdfaffee3dc0f1785a8d6` |
| Parent protocol-conformance disposition 03 | `790c7a1fc1bc28985ac70c8c9811d549dced655172c646c0d7f018637a810c7d` |
| Compile-only handoff 03, rejected by review 03 | `3169e238848ebb217669b25513e89e6ca03cc664f51ddf9db2cb30707f26a21b` |
| Corrected objective attempt 10 | `6942c7c4ad777db5d55cc23f59d01dfcf85539b322effc981c41ea028ab8db86` |
| Rejected harness review 03 | `0f363b7ee966e29dc17dc1f46a6c4b48016546136d9e2e5369f960fbe2131b36` |
| Review 03 decisive controls | `8b0077f8bc3f1c01c3fe700528d01ae309700ca4abc84183798258726b3c3b09` |
| Parent review 03 disposition | `1408a13673b7d69049d0eaafba4d9ddcb31335eaf222f6476f4bb0dceaccdc3a` |
| Parent handoff 03 reset-order finding | `497c4bce01dc5345671d7e203436dd13c1b7f11129b7fe4563312edfa41d0830` |
| Returned current-draft snapshot | `677602ffb846e800adf0e563ddc3c31ffb189c577a6de428fd0d68293ea4e25d` |
| Parent stop-rule return | `3e2270af0d559bddd8bf4d5ccb9c788d83c8fd99ce5ef167ee1c0505b2f6c62a` |
| Review 01 process-order erratum | `d58913bd0ba8f3f788aa29e038c8eba991fa071c7c1018f3800c3bcecd365e41` |
| Independent harness mutation controls | `1b60eb512964b4aede9eec484abf88995b9e5f3d7c3c13c5c4743150d054cf70` |
| Parent protocol acceptance | `42fa9c9cb9a69f07f8d7a9efd4715b986cd65f82f969639b7d7d46bb32891a1f` |
| Build 10 compiler-source proof | `cf7b32d80cde7a7990476e4e27d3bc3061314394b1816d5f6b2c891056a182f0` |
| Parent build 10 acceptance | `14dddfbf4b0cb5b0b914e59681e77e61a6c415be9478d4da6147b7f317c36f8c` |

The first review found four blockers and a required rejection-policy decision.
The second accepted their corrections before source preparation. These are AI
maintainer reviews and parent acceptance, not human sign-off or independent
empirical replications. Original drafts, both reviews and acceptance receipts
are retained under `.artifacts/r10-schema-migration-20261016/`.

The subsequent oracle review verifies every copied template, the 75-only
arithmetic and the reset relations at their stated provenance. Application-source
review accepts the frozen third derivation set's public API use and separation
of mapping from observation. Two earlier derivation failures are preserved.
These source-level checks do not establish compilation, probe correctness or
runtime success. The migration target must compile in the actual project graph
before the first assigned native process; its original-schema predecessor must
then be rebuilt and separately sealed for that process.

The initial harness review found that its checker accepted incomplete or wrong
reset, marker, generation and fresh-initialization evidence, while rejecting a
fully observed adverse reward mapping. The probe also classified an explicit
application rejection as invalid observation. The original objective checks did
not expose these gaps; independent mutation controls did. Their passing result
therefore does not establish compliance with the frozen observation contract.

The same review found that the claimed executed-target build retained the V0
application DLL. Copying source variants preserved an older modification time,
so the successful build command did not recompile Gameplay. Build attempts 05
and 06 retain their zero exit codes but fail target-artifact validation. Their
snapshots remain preserved and cannot authorize a native launch. The correction
must force rebuilding and bind compiler source checksums to the resulting
application, in addition to source/output file identities. The original
initializer-only package and execution record remain byte-identical.

The forced application rebuild, attempt 08, then exposed two F# syntax errors
that the stale build had hidden. Derivation 04 parenthesizes the type-test guard
and replaces the illegal inherited-object alias with `base.TrySynchronize`.
Focused review accepts those exact changes at source scope; the intended
mapping, observation insertion points, V0/V1 bytes, contract and oracle remain
unchanged. Attempt 09 then failed on the shadowed `Game.Handle` name. Derivation
05 qualifies it as `Nu.Game.Handle`; focused review accepts that name-resolution
change without changing the event target or migration policy.

Application-only rebuild 10 passes with 120 warnings and zero errors. The
independently copied executed DLL, PDB and source pass all eleven compiler-proof
checks: the exact Gameplay source checksum, DLL/PDB debug identity and required
record, message, witness, migration and observer metadata agree. Parent
verification accepts that evidence and clears the target compilation/provenance
gate after four retained failures (05, 06, 08 and 09). The inspector separately
accepts preserved V0/V1 fixtures and rejects stale source, mutated source and
wrong-PDB fixtures, including a wrong PDB with the same Gameplay checksum. This
does not establish runtime assembly resolution or validate the corrected probe.

The corrected probe failed compilation on attempts 11–13, then passed attempt
14 with 122 warnings and zero errors. Its independent snapshot retains 250
files, including the exact executed application DLL/PDB from build 10. V0
application rebuild 15 also passed, with 120 warnings and zero errors, before
the user paused work. On October 18, resumption checked both completed build
logs, every file in the retained probe snapshot, and all 18 protected prior
package/record/lock identities. No build or native process from that work was
still running. These checks preserve the completed attempts; they do not accept
the current V0 probe, its final seal, or the corrected harness behavior.

The October 18 parent inspection found a remaining classification defect in
the corrected draft. Readable wrong markers, duplicate handlers, repeat drift,
failed continuation and incorrect reset still reach generic assertion/error
paths. The checker likewise requires several expected behavioral values before
it can return a valid adverse result. Its selected adverse fixtures therefore
do not establish the full contract distinction. The next correction must derive
phase outcomes from raw observations and preserve observed failures separately
from missing or corrupt evidence; native execution remains unstarted.

Probe build 16 subsequently passed against V0 with 122 warnings and zero errors.
The accepted inspector verifies V0's source/PDB/DLL correspondence, including
the application copies reachable from the probe. The second frozen handoff
retains all four output roots and the 3,240-file source manifest. Independent
review accepts that repaired build/seal integration at compile-only scope.

Review 02 confirms the classification defect and finds connected gaps in
partially completed runner handshakes, intermediate reward/type checks, fresh
reset identity and exact live-to-fresh checkpoint binding. It also exposes an
alleged preservation-failure fixture whose raw state never changed: agreement
between two supplied failure flags is not an observed failure. Its corrected
counterexamples preserve truthful subsequent snapshots and message counts;
earlier confounded control attempts remain recorded and are not the decisive
evidence. These are checks of the research harness, not native application
observations. The next repair keeps the frozen application, oracle and six
assigned processes while changing the observer, runner, checker and fixtures
together. Two harness candidates have failed the unchanged review gate.

The combined correction's probe builds 17–19 failed on F# expression and
tuple/list grouping. After parent inspection of all remaining compiler
diagnostics, build 20 passed with 122 warnings and zero errors. That clears
this compilation gate while retaining all three failures. Their commands,
logs and exit codes survive, but contemporaneous per-attempt F# source copies
were not captured for builds 17–20. This is a construction-provenance limit;
later reconstruction would not supply the missing original captures.

Objective attempt 07 passed its included fixtures but omitted several frozen
controls. The expanded attempt 08 failed on inconsistent later snapshots in
its wrong-brick fixture; attempt 09 corrected those snapshots and passed its
included checks. Parent inspection then found that the draft repaired an
unexpected invalid-source installation with another reload. The frozen
protocol permits restoring the executed source bytes only. Build 21 had
already compiled successfully; its exact input, outputs and logs are retained
as compiler-pass, protocol-rejected evidence. No native process ran.

That parent rejection is the third unresolved harness/conformance failure,
even though final packaging had not finished. The correction removes the
rescue, retains the actual bound generation and state, and applies the frozen
continuation prerequisites. Objective attempt 10 accepts the included
filesystem-restoration cases and rejects an extra driver action. Compilation,
complete control coverage, independent review and parent acceptance remain
separate requirements before native execution.

Build 22 then failed on one F# method-application expression; build 23 corrected
it and passed with 122 warnings and zero errors. Both exact source inputs and
the successful outputs are retained. The corrected V0 package is sealed with
all four output roots and the 3,240-file source manifest. Parent identity checks
rehash all 38 evidence source/copy pairs and all 14 package copies against the
current files. These identity checks do not accept harness behavior or the
native launch.

Review 03 rejects this frozen handoff. Its complete synthetic counterexamples
show that eligible eight-field predecessors can lose their assigned later
phases solely because a valid-source delivery failed; that the checker can
accept a future-only assembly identity, two equal but wrong type names, or a
retained-identity flag without raw evidence; and that it can classify nonzero
input or a wrong continuation schedule as valid application failure. Source-
version resolution, exact live/fresh binding, filesystem-only restoration and
V0 compile/seal integration pass this review's bounded scope.

Parent acceptance counts that rejection as the fourth unresolved conformance
failure. Actual schema/state/projection/reward must decide later eligibility.
With fewer than two successful FSI installations, the invalid-source control
lacks its specific second-generation dependency; that does not automatically
withhold an otherwise eligible continuation. Each attempted delivery needs its
own source, script, diagnostics and returned-state evidence. No rescue reload,
reward repair or replacement process is added.

The same correction must bind exact type names, including FSI's prefix. Parent
inspection of the previous native trace finds `FSI_0005.Breakout.Gameplay`, while
the current probe's raw-snapshot helper assumes `Breakout.Gameplay`. Observations
inside a reload call can be bound by that call's returned types; a later call's
returned generation cannot establish an earlier identity. Static 60, zero
sampled input and the assigned TimeUpdate/Update order with delta 1 are validity
conditions. Wrong application state under that delivery remains adverse. These
are harness corrections, not amendments to the application or frozen experiment.

Parent source tracing also finds that the old probe marks reset publication
after the synchronous SelectEvent/StartPlaying callbacks, while its checker
starts the observation interval at that late marker. The corrected interval
must surround the single assigned publish and reflect the actual callback
order. This is another connected finding on rejected handoff 03, not a native
reset result or an additional assigned attempt.

## October 18 return at the objective-control gate

The final correction attempted to address failed-delivery eligibility, temporal
identity, diagnostic provenance, assigned schedule validity and synchronous
reset observation together. Its control attempts have the following retained
outcomes. These are synthetic harness checks, not native application runs.

| Attempt | Outcome at the unchanged objective-control gate |
| --- | --- |
| 11–12 | Failed: reset summary contradicted the trace. |
| 13 | Failed: extra-capture validation raised an indexing error. |
| 14 | Failed: a future-only generation was correctly unknown, but the old fixture still expected an adverse result. |
| 15 | Failed: positive invalid-source-installation reset summary contradicted the trace. This was the fifth consecutive failure and required return. |
| 16 | Failed after the threshold on the same reset contradiction. |
| 17 | Failed after the threshold: stale-start raw/property type did not match its bound earlier generation. |
| 18 | Failed after the threshold: a diagnostic control changed obsolete aggregate evidence and was accepted. |
| 19 | Passed its included 6 success, 32 adverse and 21 invalid cases after the threshold. |
| 20 | Passed the same included cases with strengthened receipt-file checks after the threshold. |

The parent should have enforced the return at attempt 15. The delegated work
continued through 20 before the parent interrupted it. No compilation or
native launch followed; no fifth independent harness review occurred. The four
unresolved harness/conformance failures and the separate objective-control
threshold are both retained. The later passing controls neither establish
native migration nor retroactively authorize the overrun.

Every attempt directory remains under the private construction record. Attempts
11–18 retain partial fixture traces, process receipts, generated-script and
handshake artifacts, source copies and fixture logs, but have no top-level
receipt, separately retained command output/traceback or contemporaneous
package-source snapshot. The failure descriptions above use the worker audit
and tool history. The current draft cannot reconstruct those missing inputs.

An independent 14-file copy preserves the exact returned draft at
`.artifacts/r10-schema-migration-20261016/construction/returned-draft-01/`, with
file manifests for all ten attempt directories. The parent verified those
copies and manifests. Attempts 19 and 20 retain receipt hashes
`af597a9398993f5e6d237dced590a3d2ec4590d17a678975f69d7e3ce469c73e`
and `835769ebe0902da1f9df5991c7202d5787b4a3584a7fdd6afe61e0cc203231e8`.
This is preservation of unfinished work, not a build seal or acceptance.

Further R10 edits, controls, builds, sealing, candidate review and native
execution are stopped. If explicitly resumed, first bind the exact returned
draft and its provenance limits, then accept coherent controls, the current
compiled probe and predecessor seal, and independent plus parent review before
any of the six assigned processes. For resumed delegation, allow one objective
or build attempt per dispatch, capture its exact inputs and output before
another attempt, and have the parent record the unchanged-gate failure count.
This prevents an internal correction loop from silently crossing the return.
The accepted application derivation, contract, oracle, no-rescue policy and
prior initializer-only result remain unchanged. The separate R02 return also
remains in force.

## Execution and interpretation boundary

Source preparation must use the same exact Nu pin and Gaia bridge in a new
private tree. Source, observer, runner, objective controls and copied build
snapshots require acceptance before any native launch. All construction and
assigned native attempts remain visible; five unresolved failures at one
unchanged gate require return. The separate R02 construction return remains in
force.

Count application mapping/storage/subscription work separately from observation,
oracle, reconstruction, review and integration work, including failed attempts
and reuse. The six purposive cases do not measure human or agent productivity,
ordinary agent access, general schema migration, history branching, external
effect preservation, atomicity or comparative benefit. The broad survey and
other research directions remain open at their recorded scopes.

The frozen application derivations make the authored work visible: adding the
field/default/scoring edits replaces 3 lines with 5; the explicit migration
composition replaces 1 further line with 73; observation instrumentation
replaces 2 more lines with 20. These are textual diff counts, not effort or
performance measurements. They exclude the much larger probe, runner, oracle,
checker, review, failed construction and integration work. Any later practical
comparison must account for that work according to its own production and
measurement boundary.

## Publication checks, October 18

Publication `98d47d1e9bc9dc78cefa60426fae1ca76b8c21a9` passed
[CI 39105756658](https://github.com/Happypig375/interactive-software-evolution/actions/runs/39105756658):
routing checks took 7 seconds, full Linux validation 12 minutes 32 seconds and
full Windows validation 13 minutes 22 seconds. The separate maintenance job
and optional E2 baseline job were skipped; maintenance fixture checks ran
inside both full validation jobs.

Local publication checks passed staged whitespace, UTF-8, oracle JSON parsing,
566 local Markdown target checks, exact staged bytes for the three published
package files, and preservation of the 18 protected initializer-only package,
record and lock files. The unfinished migration implementation was excluded
from this publication. These checks do not compile or accept that returned
draft and establish no native migration result.
