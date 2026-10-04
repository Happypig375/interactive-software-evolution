# S267 — Ubisoft infrastructure change: preparation, propagation and recovery

Jose Bonet Faus, Pascal Le Masson, Benoît Weil and Antoine Bordas, *Managing technical debt at Ubisoft IT: interfaces and change propagation in engineering systems interventions*, Proceedings of the Design Society6,2741–2750,2July2026, [DOI10.1017/pds.2026.10632](https://doi.org/10.1017/pds.2026.10632). Main-agent reconstruction,2026-10-05 HKT. **Complete selected author edition:** all11physical PDF pages, comprising HAL cover plus10article pages, all six figures and24references are read in text and visually. This is one publication credit, not two editions or multiple independent cases. No original author code, model or system is executed.

## Editions and preserved evidence

Native parent **`GHE2RSLN`5712** and note **`IKE34KMY`5713** precede selected reading after collection/library DOI/title checks. Collection`PKLXQNEE` is preserved.

| Material | Identity and actual coverage |
| --- | --- |
| [HAL v1 author preprint](https://hal.science/hal-05636903v1), native **`MEGVQ3TS`5716** |4,856,827bytes; SHA-256`054693ed999da1d8ea5fca5f696c134c45f7b6d6672bc85207fad2b4e4612815`; MD5`61f58a82a43562c7fe14a5acc8b91c37`. All11pages/six figures. Cover cites2025 and deposit28May2026; API produced-date15November2025 is distinct. The article has DESIGN2026 formatting, a placeholder DOI and preprint watermark. |
| Final-publication indexed text, native **`7LTUV6AQ`5720** |39,649bytes; SHA-256`ba5c005b59545bf795945eadf7e049d48a6e5280abf43cb6932dd0e5023fd2e2`; MD5`66a82bc04bff4c9d9940fc9b97d1e4c5`. All695primary lines60–754, final DOI/pagination and24printed references; final figures not acquired. ResearchGate's26-reference panel is not the printed reference count. |

Publisher PDF and normalized public ResearchGate PDF requests return403; four figure opens fail. HAL's web landing/document route presents an access challenge, but its public metadata API supplies the file URL and ordinary GET successfully returns the PDF. No challenge is bypassed. Both native bodies/hashes verify. All pages were rendered; raster figure tables, poorly represented by extraction, were read visually. Standalone extracted images lose their soft-mask/background appearance, so page renders govern interpretation. Final-PDF byte/figure equivalence remains unverified; the bodies agree on the reconstructed method and reported examples.

## Case and intervention, located in the author edition

Sections3–5 concern one selected critical Perforce-based version-control infrastructure, not a game-engine rewrite. The first author participates in the project. Evidence collected October2024–November2025 comprises64documents/431pages,96meetings/120hours,170days of telemetry and45interviews/58hours with16stakeholders. Academic/Ubisoft steering reviews are reported. These are multiple evidence sources within one intervention.

The case migrates one active production server to virtualized hosting while retaining links to the wider system. Figure4 dates initial isolated tests toJune2024, preparation toJuly2024, migration toMarch2025 and operational stability toMay2025. The intervention thus begins before the reported data-collection window; the paper does not make every event a contemporaneous observation.

Figures2–5 separate the intended operational improvement from known and unknown propagation. Figure3 maps functional requirements to design parameters. Figure5 specifies disk-resize/deployment/scaling time as intended performance measures, alongside storage, identity, billing, replication and recovery dependencies. The article does not publish numerical before/after outcomes for those measures.

| Reconstructed provision or outcome | Location and interpretation |
| --- | --- |
| Change storage/security interfaces before migration | Figure5, DP4.2/DP8: preparation is part of the intervention. |
| Oversize compute/storage, then reduce capacity; retain old/new recovery infrastructure temporarily | Figures3/5, DP4.1/DP4.2/DP9: reversibility requires provisioned resources and a limited coexistence period. |
| Redirect some requests to a neighboring server; let IT absorb cost discrepancies | Figure5, DP3/DP12: technical containment and organizational cost allocation are explicit. |
| Replication-related slowdown identified and resolved | Section5/Figure4, FR3/DP4.1: a reported adverse event and recovery, not an incident-free migration. |
| Better backup/recovery enabled a previously infeasible optimization | Section5, FR9/DP9: preserve the reported positive surprise without inventing its magnitude. |

Figure6 proposes five stages: reduce known uncertainties, prepare containment/response, organize incident handling, transition into sustained operation, and use the learning in later changes. Its containment metaphor includes transient structures and actors able to absorb consequences, beyond network firewalls. Shared infrastructure motivates potential transfer; it is not a second observed replication.

## What follows, and what remains uncertain

This case makes an architectural-benefit claim more demanding: a local redesign can improve a target operation while redistributing load, expense and risk. For Nu, integration prerequisites, continued service, retained-state compatibility, observability and recovery work belong beside edit effort and runtime cost. A diagnostic or a successful initial transition does not alone establish the later service obligation. This is an inference about evaluation scope, not evidence that Nu requires this particular cloud architecture or that a specific Nu mechanism works.

The favorable reported recovery and backup optimization remain useful situated evidence. Their magnitude, counterfactual effort, total lifecycle cost and dependence on the support package are unresolved. Neither the quantity of interviews nor170telemetry days creates170independent interventions. A deliberate critical-case choice and participant-researcher role limit the target population; no claim of representative industry incidence or an isolated causal mechanism is warranted. The reviewed paper does not expose the telemetry, interview coding or operational runbook as a reproducible packet.

Static presentation discrepancies also limit literal reuse of the framework: Figure5 lists FR8 as both affected and unaffected and labels its unknown-interface section “known”; Figure3 labels the incident-resolution subrow FR12.2 under FR11, whereas Figure5 uses FR11.2. Record these as source-label ambiguities, not proof that an operational error occurred. The broad literature-gap claim about unknown interfaces is not independently validated by this single case; reuse existing live-update, migration and operational-change methods when characterizing prior art.

SC192's outward graph returns20edges/21nodes at its cap, marked truncated. All23returned snippets are read;18edges carry mentioning labels and two are unlabelled. They establish how S267 frames its dependencies, not those dependencies' validity. The edge mapped to10.1109/icse.2013.6606774 names a workshop, while the primary bibliography names McConnell's *Managing Technical Debt*; that correspondence is not accepted. All24printed references are screened without claiming their full methods were read.

For B10/B11/B12, reuse this operational boundary and retain [S266's distinct access gap](S266-postmortem-extension-access.md). Continue the strongest accessible team/studio practice or type/temporal method lead; do not repeat general technical-debt searches merely to increase coverage counts. Final-edition binding and a fuller case packet remain conditional follow-ups. No experiment or worker is authorized.
