# A public XState persistence decision: Showtime

The transfer search now binds a public application, a reported failure and a
specific persistence-policy change. It does **not** yet bind a demonstrated
machine-evolution failure or independent demand for cross-version preservation.
Retain this as a conditional case for the
[non-game transfer agenda](nu-status-quo-and-transfer-audit-2026-10-23.md#non-game-transfer),
alongside the stronger existing-application but different-scope alternatives
below. No application was installed, built or run.

## What is actually bound

In [Showtime issue #150](https://github.com/vishnujayvel/showtime/issues/150),
the owner reports losing an in-progress show's locked beats, lineup and current
act after relaunch. Machine changes, a date check and Electron storage scope
are proposed causes. These are hypotheses in a self-report, not our diagnosis.
The [repair PR #152](https://github.com/vishnujayvel/showtime/pull/152) adds
versioning and state-value validation. It identifies Claude Code generation,
and its manual same-day and next-day relaunch checks remain unchecked. Reported
passing tests are upstream claims; we did not execute them.

The pre-fix source is `74474089be9f4a8487cd3034c5d4c6a087765499`, and the
selected fix head is `5a4e415733e8048a146c84600f90d94fc7134c5d`. The intermediate
`ce92cba382e8fc6a0ea95532eb247289b9c6d05a` has the exact pre-fix parent.
The two persistence commits change the actor/loader and its tests, while
`showMachine.ts` is byte-identical across the selected endpoints. The package
declares XState `^5.30.0`; that range is not an exact resolved dependency pin.

| Boundary | Exact source policy |
| --- | --- |
| Old saved record | Stores `{stateValue, context, savedAt}` without a version. It is an application-defined partial record, not `actor.getPersistedSnapshot()`. |
| New loader, missing or unequal version | Deletes the saved record and initializes afresh. This includes every old unversioned record. |
| New loader, matching version but invalid state value | Resolves `no_show`/`idle` with saved context merged over initial context. The PR prose's `writers_room` fallback disagrees with the inspected code. |
| Known valid same-day record | Resolves the saved state value and merged context. A different UTC day is discarded. |

These policies follow the [pre-fix loader](https://github.com/vishnujayvel/showtime/blob/74474089be9f4a8487cd3034c5d4c6a087765499/src/renderer/machines/showActor.ts#L18-L57),
[selected new loader](https://github.com/vishnujayvel/showtime/blob/5a4e415733e8048a146c84600f90d94fc7134c5d/src/renderer/machines/showActor.ts#L18-L122)
and [unversioned-record rejection test](https://github.com/vishnujayvel/showtime/blob/5a4e415733e8048a146c84600f90d94fc7134c5d/src/__tests__/statePersistence.test.ts#L309-L327).
The parent inspected the issue/PR bodies, these decision-critical source ranges
and the identical machine hashes. The repair is a concrete **persistence-schema
and reset-policy change**. It cannot alone be called a changed-machine migration.

## A fair comparison, if preservation is useful

If maintaining an active show across the selected deployment is a real
requirement, the first rival is an ordinary application-owned transformation
from the old record to the new envelope, followed by `resolveState`. A schema
tag or explicit mapping is already ordinary machinery. Extra validation must
justify its construction and use against that baseline; a fresh show is a
matched outcome only if its required progress and recovery work also match.

The [machine and context](https://github.com/vishnujayvel/showtime/blob/5a4e415733e8048a146c84600f90d94fc7134c5d/src/renderer/machines/showMachine.ts)
include parallel phase/animation state, nested live/writers-room substates,
lineup/current-act data and timer values. The
[actor integration](https://github.com/vishnujayvel/showtime/blob/5a4e415733e8048a146c84600f90d94fc7134c5d/src/renderer/machines/showActor.ts#L171-L320)
adds an external celebration timeout, timeline/SQLite updates and notifications.
Some transient context flags are deliberately omitted from persistence. A
later contract must specify timer and transient meaning, observe the immediate
restored state and one meaningful continuation, and inspect omitted/duplicate
effects. A serializable record or successful start is insufficient. No durable
event log was found in this path, so replay is not a mandatory baseline here.

The case remains conditional. The repository and report are owner-maintained;
at retrieval it had no stars or forks, which limits demonstrated independent
adoption rather than proving non-use. The source explicitly invalidates old
versions, and no inspected statement establishes that preserving an active show
across deployments is the desired policy. A cross-version requirement would
currently be authored. For a **machine**-evolution claim, separately pin an
actual shape change and its correspondence. For the already-bound persistence
upgrade, do not add a cosmetic machine change merely to fit a preferred label.

## Alternatives retained by the search

| Evidence | Disposition |
| --- | --- |
| [Aipictors #165](https://github.com/aipictors/aipictors/issues/165), [#357](https://github.com/aipictors/aipictors/issues/357) and [PR #358](https://github.com/aipictors/aipictors/pull/358) | #165 reports a settings-restoration defect; #357 reports manual persistence-maintenance burden, and #358 switches to storing an XState persisted snapshot. Subsequent context fields changed under the same application storage key without an inspected application schema version/migration. This is a concrete evolution exposure, but no inspected report establishes a resulting old-snapshot failure. Retain as a configuration-restoration case. |
| [Node-RED XState node #108](https://github.com/sonntam/node-red-contrib-xstate-machine/issues/108) | A maintainer describes V4/V5 chart/tool migration burden. The inspected node recreates the interpreter; no durable runtime snapshot-transfer route was found. Definition migration and active-state migration remain different tasks. |
| [XState #941](https://github.com/statelyai/xstate/issues/941) | Reports an actual 4.6-to-4.7 persistence-format break and application-owned transformation work. All 20 comments were read. The affected applications are not bound public artifacts, and a later V5 resolution claim does not establish arbitrary machine-schema safety. |
| [Lineup prototype #13](https://github.com/nopivnick/lineup-prototype-03/issues/13) | Excluded from an existing-workflow case: the issue states the feature is unbuilt. Its apparent migration match is not an observed maintenance task. |

## Coverage and next action

The [search ledger](literature/nu-background-searches-2026-09-30.md#2026-10-23-xstate-application-and-material-policy-follow-up)
records returned ranges, narrowing, alternatives and the one-time 14-source
decision audit. This is public-software evidence, not a paper-reading segment
or a systematic prevalence sample. No new PDF, Zotero record or completed
primary-paper reading is claimed.

Private evidence is in `r12-intent-policy-20261023/xstate-practice/` under the C:
recovery root. The final source/search handoff has SHA-256
`12fd51fc844511004003f81ed494ef210bc78558866a78a05c1ad181232f5368`.
Pre/post machine bytes both hash to
`6cbf763b94d057d3a58027b3de8d887f44c63f527a992df4cd319c92d375fb50`.
The new actor source hashes to
`074936dde34eb8dbac7776fb4a2f6fb7c5eb571fa5b718041fac1f84bf9c6bd4`.

Next resolve the practical preservation requirement and, only for a
changed-machine claim, the actual machine-change lineage. Retain current reset
as a valid policy under its own requirements. This case supplies neither a Nu
advantage nor an executed transfer result, and it does not reopen stopped R10.
