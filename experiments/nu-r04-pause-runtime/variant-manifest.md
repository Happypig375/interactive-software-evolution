# Prepared runtime variant manifest

All variants start from exact Nu commit `064f7ae92a8506689cd91aff5e6804a375d6ef3d`. The preparation receipt verifies original `Gameplay.fs` SHA-256 `571E2A5CE3F0630972F2FBE4E9A6A3C376BCF4D1A74589D14C882B2EE0DB1423` before transformation in every fresh tree.

## Reference application sources

| Variant | Probe | Prepared Gameplay.fs SHA-256 |
| --- | --- | --- |
| `baseline-explicit` | baseline | `571E2A5CE3F0630972F2FBE4E9A6A3C376BCF4D1A74589D14C882B2EE0DB1423` |
| `baseline-wildcard` | baseline | `5FF5CB277FAD9359405EE0341C70837319221EC710F2178E632675A856E38566` |
| `pause-explicit` | pause | `247EF4E432030F254B7A67D991D7EFD7D75511965AA542717E4043A9C77AE976` |
| `pause-wildcard` | pause | `E0019708E97C935A1E814F5527D01F067FAB8E3007716860D44B68596CFB0064` |

Direct complete-file diffs bind each explicit/wildcard pair to its one terminal-clause alternative.

## Single-fault sources

Each fault starts from `pause-explicit`, changes only `Projects/Breakout Mmcc/Gameplay.fs`, and uses the same pause probe. `Simulants.fs`, `WorldAudio.fs`, `Gaia.fs`, `Probe.fsproj`, `Common.fs`, `BaselineProbe.fs`, and `PauseProbe.fs` have the same hashes as `pause-explicit`.

| Variant | Exact change | Gameplay.fs SHA-256 | Generated patch SHA-256 | First gate |
| --- | --- | --- | --- | --- |
| `fault-missing-toggle` | remove only `Entity.ClickEvent => TogglePause` from Pause | `52249D510EAA2933DBAE352FDE733BB324243142CC84D881175BC22458E23997` | `6B1CDEA25021D07914FA65085442FC4DDA13A7B09E919CDC5168E9B2D9EEA382` | `pause-reached` |
| `fault-hidden-content` | change the content predicate to `GameplayState = Playing` | `6893371D3CCE507C25431D46AFADF5BEAB541AE20218190D6C92F580A73A2A8C` | `24AA3EEFA3E92B402F7F74AB32411669D6AC2FD921BA8A28557FD58B6D51BA4C` | `pause-projection` |
| `fault-advancing-time` | restore unconditional GameplayTime increment | `3A7229DF9E0FFF1DAABAB997889DFDA7042D9EE7B4BB9537F01B777273EBA808` | `24680D90FD9804704D6A50F87FFD8F2CFECAFDDFCBFEA7D0C7E0A422B7773FDD` | `pause-frozen-model` after first pair |
| `fault-reset-resume` | return `Gameplay.initial` from the Paused resume branch | `7C44D792E453C3B877DF8D35386D53F3A438C345EF1CF0BD67586FF3F4631371` | `65C5D54AD591CD548A5BC4533012B42ABEBD22B8D84CEE17139236B599E92D10` | `resume-retained` |
| `fault-stale-quit` | remove only the `Gameplay.empty` assignment from FinishQuitting | `FEB7DA1D55884783A4C984286F7B1A464ECE5FC5EBCC0EF25ED58597C6AA6F1D` | `B19B7BF3B827AC4905FC735ED9B535C7D221DEFA528FA57932272EF42EB8076E` | `quit-reset` |

The exact generated unified patches remain with the immutable private preparation receipt. Their content is also fixed by the anchored replacements in [prepare.py](prepare.py). Build success is recorded separately and is required before each variant’s launch.

## Common identities

- `Simulants.fs` in completed pause and all fault variants: `CB5A05FEE046ECA1E5AB11F1557E17F0CC508E575D63458CC42C54E47B67CF6F`
- instrumented `WorldAudio.fs` in every variant: `8CC92031BC086DCFFE1EC1670BE4D834484C2730E9A0F35A1D0EF3CB00301CA6`
- instrumented `Gaia.fs` in every variant: `38CE5E708FAEE04F6C100E98C46CE7CB357EA68F0D8B6726E67A8206D9835093`
- `Common.fs`: `0C8B7249D895FAC895B67E911CD615AB9FE3CDB8B4F3FED2BBA32D16B0EE9643`
- full-build `BaselineProbe.fs`: `AC78B6A8E0ED8FBC8453D51DA4968C6909E71A74A037B26782AAE1F4AA216725`
- full-build `PauseProbe.fs`: `0FBA3A20605605AFCEF73D6932AA3449505CA02338DA9CF08C2DA8D36D16BA15`
- amended `BaselineProbe.fs`: `CAA56557185D77738AC5B868F038DE24AB2FDC2D4EC93C28860A39D7EB0A5211`
- amended `PauseProbe.fs`: `AC9D0B7955EA384B3487BE5C22A44BF80527AF835D9F6BEA9318820850E5846B`

The amended probes add the prospective common empty-content reconstruction boundary and safe pause failure observations. They were compiled against every unchanged preflight-08 arm; no application or engine source changed after the full builds.

The historical preflight-06 receipt predates the explicit `Vector3` annotation. That annotation-only repair is preserved in [preflight-06-to-final-common.patch](preflight-06-to-final-common.patch), SHA-256 `20D004991029ABE8B5CA8A3E9FDE5CB2272B47BFF39A2E2F673FABDBA8366E38`. The later preflight-07 preparation was stopped before build when review showed that binary32 rounding permits the RGB endpoint `1.0f`; its exact three-comparison correction is [preflight-07-to-final-common.patch](preflight-07-to-final-common.patch), SHA-256 `CE705DFA783371592AB9CEC140644DBD0D6CC4C1EF88A8B3FBEA663A7C74F197`.
