# R06 first measured series: feasibility disposition and release

**Prospective maintainer decision, 2026-10-15, before H1 or any other measured
assignment.** This supplements the [original contract](pre-execution-contract.md)
without changing its twelve assignments, operations, output contract, clocks,
or failure policy. It is an execution decision under the user's existing local
experiment authorization, not human scientific approval.

## Feasibility evidence and retained failure

The original history process FH passed the complete common setup, acquisition,
ten-pair drift and recovered B0 checks. The original reconstruction process FR
timed out at 600 seconds with configuration as its only trace event. Its
callback entry and startup cause remain unknown; it supplies no observation
of acquisition or reconstruction.

The separately assigned FRD1 diagnostic used the identical accepted executable,
application, checkpoint and recovery code. It passed in 35.75 seconds, before
the prospective 60-second conditional stack boundary. No stack was attempted.
Its concurrent start/exit process observations are diagnostic context, not part
of the measured protocol. Parent verification checked every raw output identity,
the common clear, complete seed/drift/ready models and projections against the
verified FH observations, the positive event word and deltas, sampled Left/Right
states, phase, counts and clock arithmetic.

FRD1 is an additional unscored reconstruction feasibility observation. It does
not replace FR, make the original feasibility record all-successful, or enter
the measured denominator. It establishes that the unchanged reconstruction
route can produce the declared output in this environment; it does not explain
the earlier timeout or establish startup reliability. The original contract's
two initial feasibility assignments are therefore supplemented by this explicit
diagnostic and disposition, rather than silently rerun or relabeled.

This evidence is sufficient to attempt the first descriptive component series.
Both supported routes have reached the same complete declared output after
the same drift. The unresolved startup failure remains a material limitation
and a reason to retain the strict interruption policy. No feasibility or
diagnostic duration is a measured cost sample.

## Frozen execution

Use the accepted build02 receipt, SHA-256
`6945a68aa7e1bbea5084a3ed822e1370ff2e35a384c6c752c5439fd32df19fb2`,
and unchanged `RecoveryCost.dll`, SHA-256
`207d6027af9a793e1b3fabfcdd8f073ee572d89b72d33dfd632bb90bc8298fd4`.
The receipt binds all source, fixed-input and common-binary identities. The
public run driver remains SHA-256
`759868b586b25aebc682598551d19961a12644abc0b47a3e16f07d337c072892`.
It must recheck those identities before each launch. Preserve the build-time
README bytes until the series has stopped or completed; publication corrections
must not change a running series' recorded inputs.

Run exactly the original order, serially:

```text
H1 R1 R2 H2 H3 R3 R4 H4 H5 R5 R6 H6
```

Use new directories `runtime-H1-01`, `runtime-R1-01`, and equivalently named
directories for the remaining assigned IDs under the existing private R06
artifact root. Never reuse an output directory. Each target retains the
600-second deadline and 1,200-callback watchdog. Do not attach diagnostic tools
to a measured target, add warm-up, change GC policy, or alter the observer.
Keep other maintainers from launching concurrent Gaia experiments during the
reservation. Ordinary host load is not controlled, and this reservation is
not evidence of machine quiescence.

After each terminal process, inspect its retained exit/timeout status and
semantic result before launching the next assignment. On any unexpected
semantic or infrastructure failure, stop the remaining series and preserve
the failed attempt and all unrun assignments. No retry, replacement, reordered
successor, or sample extension is released. A later new measured series would
require its own prospective amendment; it cannot fill this series' missing
slots.

## Reporting and verification

The previously accepted v4 `summarize.py` remains SHA-256
`12238b28ba61ce6c823810175e43df368baba913fdf9051815701ac3b2b28e95`.
Pass explicit original FH/FR and measured process receipts to it once the series
stops or completes. Keep FRD1 in the separate diagnostic record because it is
outside the original assigned-attempt schema. The summarizer preserves failures,
invalid records and unrun slots; it does not perform semantic replay.

Independently verify completed traces against the accepted output, drift,
phase and event contracts before interpreting their costs. Describe valid
observations with the predeclared route medians/ranges and paired differences,
showing actual denominators and every assigned outcome. Preserve zero durations,
collections, approximate process-wide allocation and first-use/cache/temporal
limits. Unequal retained payload scope and unmeasured construction, integration
and repair work preclude an isolated persistence or maintenance-benefit claim.

Private acceptance lineage remains in
`.artifacts/r06-recovery-cost-20261015/`: the FH verification, original FR
receipt, diagnostic plan/driver/preflight and independent review, FRD1 raw
manifest, and parent semantic verification. The latter has SHA-256
`d44ac9dfcc1a58f9fc18eb2d15444bfe3c2cc9bb277f8740d0359e8c3b3137b3`.
The complete execution record and compact publication receipt will distinguish
this prospective decision from the subsequently observed outcomes.
