# Local research workspace migration, 2026-10-08

The user requested moving current work to `A:/` to free space on `C:/` and selected a clean research workspace with a separate archive. The active directory is `A:/nu-value-research`; Interactive Software Evolution remains the repository's internal codename and GitHub repository. This changes local organization, not scientific conclusions or experimental authority.

| Location on this machine | Purpose |
| --- | --- |
| `A:/nu-value-research` | Independent active Git checkout, focused on the Nu literature and value investigation. |
| `A:/research-archive/interactive-software-evolution-2026-10-08/repository` | Complete pre-migration workspace, including all tracked, untracked and ignored files and original Git metadata. |
| `A:/research-archive/interactive-software-evolution-2026-10-08/linked-worktrees/alf-v3-calibration-3cfe99b-20260831` | Preserved older calibration worktree, with its Git connection repaired. |
| `A:/research-archive/interactive-software-evolution-2026-10-08/migration` | Local SHA-256 manifests, copy logs, original Git state and verification receipts. These records are not published. |
| `C:/Users/hadri/source/repos/interactive-software-evolution` | Retired checkout still held open by the application. Its entry files direct work to `A:/`; its large artifact folders are junctions to the active workspace or archive. |
| `C:/Users/hadri/source/repos/interactive-software-evolution.migrated-20261008` | Former staging location for verified old artifacts, results and environment files. This path was absent on the 2026-10-08 continuation check. |

The active checkout uses local Git sparse-checkout rules to show `docs/`, `reports/`, `protocols/`, the main research entry files, and the documentation CI classifier, tests and workflow. Earlier harness, benchmark, infrastructure and build files remain in the repository's Git history and full archive. Sparse checkout is local configuration, not a committed deletion. The root README now leads with current research; its complete previous version remains in the archived repository and at commit `772dd29c1b2f4f71010661d40ed537d7c6b54bb0`.

The two current literature directories, `.artifacts/nu-background-20260930` and `.artifacts/nu-literature-20260929`, are copied into the active workspace and remain ignored by Git. The archive retains the original copies along with prior experiment results, build outputs, environment and caches. Published reading IDs, attachment identities and historical evidence are unchanged. Existing Zotero storage remains in place; this move does not create or duplicate library records.

The sibling references `A:/Nu` and `A:/Nu Chat Analysis` are junctions to their existing repositories under `C:/Users/hadri/source/repos/`. Those separate repositories were not relocated. The old `.artifacts/` route preserves absolute paths recorded in local evidence; new work should use the `A:/` location directly. The old temporary calibration-worktree copy remains on `C:/`; the working, repaired archive is the `A:/` copy listed above.

## Verification and preservation

The starting branch was `main` at `772dd29c1b2f4f71010661d40ed537d7c6b54bb0`. Before relocation, the original workspace and archive matched by file roster, directory roster, size and SHA-256 for **38,253 files totaling 3,944,488,088 bytes**. The associated calibration worktree matched for **14 files totaling 327,944 bytes**. Local manifests retain each file's hash. Git metadata pointers were then repaired for the archived worktree; those administrative edits are recorded separately from the original byte comparison.

The active checkout retains the original main commit, seven backup branches, the existing tag and one stash entry, using an independent object store. The untracked `uv.lock` and the bytes of `S242-context-engineering-comparison.md` were preserved exactly. S242 had a stat-only modified indication but no textual diff before migration; its disappearance from status in the new checkout is not loss of an edit. No unrelated file was committed.

The active literature copies were independently checked against the original hashes: **13,844 files, 3,322,211,304 bytes**. Git integrity, the existing stash and backup references, critical local file hashes, Markdown links and all 11 documentation-routing tests passed.

**Latest cleanup state, 2026-10-08:** the 3.80 GB staging path is now absent. Its removal mechanism and exact free-space effect were not observed, so this is not a claim that the agent deleted it or that its contents bypassed the Recycle Bin. The retired checkout still contains **6,451 ordinary files, 142,287,311 bytes**, excluding its three junction targets. The old temporary worktree and three temporary junction probes under the archive's `migration/` directory also remain. The active checkout is usable independently of this residual cleanup.

During migration, the application held the original directory and `.git` open. A test confirmed that an empty locked directory could be redirected, but the `.git` lock prevented emptying the real repository root. The large `.artifacts/`, `results/` and `.venv/` directories were staged separately and replaced with verified junctions. Their **31,802 files, 3,802,170,067 bytes**, matched the original hash-verified snapshot by file roster, size and modification time. No reparse points occurred inside that staging directory. The remaining directory locks were not retested during the status check.

Automatic approval review rejected removal of both the staged repository files and the old temporary worktree with the stated reason **"blocked by policy"**. Neither requested deletion executed through the agent. The original manifests describe the pre-migration snapshot; they do not imply that the retired checkout's entry files or routing metadata remain unchanged afterward. The later absence of the staging path supersedes the initial pending-staging status.

The user explicitly approved cleanup after this rejection. A retry of the verified staging deletion was still rejected with the same policy message. User permission is established; agent cleanup execution remains blocked by the environment. Do not ask for that approval again; the residual cleanup listed above remains incomplete.

Migration checks cover file preservation, Git continuity, local links and the documentation change. Runtime, experimental and model checks remain outside this change's scope. The previous literature checkpoint's [CI run 37237550785](https://github.com/Happypig375/interactive-software-evolution/actions/runs/37237550785) passed its scope job; Linux, Windows, maintenance and E2 jobs were skipped under the documentation route.

## Working from the new location

Open `A:/nu-value-research` and read [PLAN.md](../PLAN.md). Continue the existing whole-background survey from the strongest consequential gap; the current named continuation is NodeGit, following the recorded SceneGit full-text access gap. Do not start fresh paper IDs, repeat completed readings or reinterpret this filesystem migration as permission for an experiment.

To expose the entire tracked source tree locally, run this in the active checkout:

```text
git sparse-checkout disable
```

This restores the files at the current commit. It does not restore ignored historical results or an old Python environment; those remain in the full archive. The archived `.venv` is historical and may contain paths from its original location. Do not use it as the active environment.

Use the active checkout for commits and pushes. Treat the archived repository as a recovery snapshot, not another place to continue the survey. The migration receipts preserve the original state if a later recovery needs more than Git history.

The active session now uses the `A:/` folder. Remaining local cleanup concerns the retired checkout, old temporary worktree and temporary junction probes; the former staging path needs no further action. Keep the active workspace and archive on `A:/`. The retired checkout and probe directories contain junctions to those locations, so later cleanup must remove link entries without traversing their targets. No deferred deletion process has been launched. Resume the authorized research while deletion execution remains unavailable.
