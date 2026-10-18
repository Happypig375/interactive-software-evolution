# Workspace integrity return, 2026-10-18

The requested re-check initially found A: `Healthy / OK`. A later native
staging attempt demonstrated changed input bytes despite that status. Local
native execution and writes to the A: workspace have stopped. This is a
storage/input-integrity return; its physical cause is not established.

## Observed failure

The seventh process of the [Terra Firma revision series](nu-terra-firma-revision-feasibility-2026-10-18.md),
`terra-revision-B-local-L0-01`, exits 2 after 3.468 seconds, without timeout.
Its original-scene SHA guard fails before engine callbacks or any setup,
operator or propagation write. The recorded pre-launch manifest has the
expected bytes; the after-manifest has three changed files:

| Staged input | Bytes | Before SHA-256 | After SHA-256 |
| --- | ---: | --- | --- |
| `original-Scene.nugroup` | 218,933 | `1dff90c5679233f6b282e03bcb2f2fd7524a6e6e93a7df814a72f5260d3a421a` | `22424fd5f851780f72ad2ab3ed18ea2d82797690b215de251cffeb2f6b3138c3` |
| `Assets/Gui/Credits.nugroup` | 744 | `d7f0151319ba55a70c3e6979fac8f4d4f0b1cf795f4bcd579506db21cfe7f8a2` | `0783275f31a089d8ca4f6d7aca8df16aaba6f962f3ea1c68d98b3b97a261b142` |
| `Assets/Gui/Gui.ogg` | 966,697 | `2a7e356d3c32fc938d96b5339fbd87b8dbdf6964cd3f5f89172c4e6ef848c7d1` | `ef1f2b48d189a51245e14db48a33fa756c908652b5ad562dd45e47bbabce657d` |

Each damaged file returns the same after-hash on three consecutive reads.
Their sizes are unchanged. The scene is no longer valid UTF-8, so scoring
returns invalid/incomplete with a decode error. There are zero callbacks,
captures, setup writes, operator writes or propagation calls, and no usable
save. The dependent reopen is ineligible, not silently replaced.

The selected original source scene and the P-local L0/L1 original-scene copies
still match the pinned expected hash on this check. Current observer/protocol
bytes also match the accepted build. These selected successes do not certify
every file on the volume.

## Volume and event evidence

At the later check A: still reports NTFS, `Healthy / OK`, with 757,638,008,832
bytes free; its disk is online and writable. Windows System events earlier on
October 18 record NTFS transaction-log flush I/O failures, corruption/online
scan notices, and failures to correct the filesystem. Repair-completed notices
follow through 18:40 local time. The failing native process starts at 20:54:23
local time (12:54:23 UTC). The inspected log does not establish a new storage
event at that process time or the physical cause of its changed bytes.

The agent performed no filesystem repair, dismount, format or deletion.
`Get-StorageReliabilityCounter` returned no objects; no SMART or hardware-health
conclusion follows. The status flag alone is insufficient evidence that this
workspace is suitable for continued native experiments.

## Verified recovery copy

Recovery root:
`C:/Users/hadri/nu-value-recovery/20261018-205753-integrity-stop`.

- `worktree/` preserves all 36 then-uncommitted Git files, 3,360,237 bytes,
  including unrelated R02/R10 drafts. Every copied file matches a repeated
  source read and its recorded SHA-256.
- `private-evidence/` preserves 4,993 selected experiment files,
  2,096,043,140 bytes, with the same per-file checks and no copy errors. This
  covers `terra-revision-*` records, controls, reviews, build/source evidence
  and observations, excluding native `application/` trees and Python caches.
  The three damaged application inputs are included separately as evidence.
- `recovered-evidence-verification.json` checks all seven native receipts
  against hashes observed before the backup, all 157 observation files against
  their receipt-bound manifests, and the ten frozen package files in each
  attempt. This verifies retained evidence, not the complete application hosts
  or all earlier private artifacts.

The original backup manifests and copied bytes remain unchanged. A separate
stop addendum records the final invalid attempt and ineligible reopen. Private
storage-event details, damaged bytes, assets and extraction bodies remain out
of public Git.

## Publication and resumption boundary

A temporary `publication/` checkout under the recovery root starts from remote
commit `fca2547c7d37c9af13db574d137d5152e54f0759`. Only the verified owned research
changes and this return are integrated there for ordinary checks and direct
push. The A: working tree and its unrelated edits are preserved; it is not
silently synchronized or repaired by that publication.

Before native continuation, establish reliable execution storage and revalidate
the exact source, prepared assets, host, compiled observer/checker and retained
evidence. Bind any resumed/replacement assignment prospectively, retaining the
failed B-local attempt and the original chronology. A status flag, successful
copy or repository CI cannot supply the missing runtime result. The R02 and
R10 five-failure returns remain separate and unchanged.
