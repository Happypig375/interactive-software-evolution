# S288 — Collaborative AR/VR development: roles, handoffs and prototype costs

**Work:** Veronika Krauß, Alexander Boden, Leif Oppermann and René Reiners, *Current Practices, Challenges, and Design Implications for Collaborative AR/VR Application Development*, CHI 2021, 1–15. [DOI10.1145/3411764.3445335](https://doi.org/10.1145/3411764.3445335).

**Disposition:** complete selected author-manuscript reading. Interviews with 26 professional creators identify overlapping roles, useful collaborative prototyping and training practices, and costs of translating designs across tools and skills. Reported prototype reuse can accelerate delivery while creating later maintenance burdens. These are situated practitioner accounts, without an assigned intervention, comparative effort measurement or Nu effect estimate. They make the accessibility of a representation to collaborators part of the value question.

## Identity and actual coverage

The [Zenodo author manuscript](https://zenodo.org/records/7348332) has **15 pages, 639,226 bytes**, SHA256 **`1cde8a72ad6784489221e8657ab52ccbd4f8bbc3f54a12f27015e26c79686cf7`**. The [German National Library copy](https://d-nb.info/1225793041/34) is byte-identical. Zenodo's advertised MD5 matches the downloaded bytes. All fifteen text pages, **98,918 extracted characters**, were read, including both tables and all 81 references. Rendered pages **1, 3, 4, 5, 7, 8, 9 and 13** were inspected; these include the complete participant table and challenge/solution/artifact table. There are no numbered figures or appendix. All fifteen pages were rendered, but only these eight page images were visually inspected. No rendering warning was returned.

The PDF identifies itself as an author version, with the exact title, four authors, CHI2021 and DOI. Its first-page copyright year is2020 and PDF creation metadata is2021-01-22; Crossref publication is2021-05-06 and Zenodo records2021-05-07. These date differences are preserved rather than silently equated. Byte equivalence to the final publisher edition remains unverified. The URN route redirects to a repository landing page whose ordinary response is an Anubis challenge; no challenge bypass was attempted. The independently available author copies supplied the reading.

Native collection **`PKLXQNEE`** parent **`F8YBQQCG`** and note **`SHM5G8XQ`** existed before selected reading. PDF **`ZTHZHHDK`**, version5906, passed native byte/hash readback. The two identical download routes do not create two studies or duplicate attachments. Final object versions and audit checks are in the search ledger. No private interviews, complete interview instrument, codebook, raw dataset, software artifact or supplement was acquired or executed. The PDF, extraction, renders and receipts remain ignored and are not redistributed in Git.

## Recruitment, interview and analysis method

Section3, pp.3–5, describes semi-structured remote interviews with **26 professionals actively creating AR/VR applications**. Recruitment uses the researchers' creator networks, social/community channels and snowball contacts. Participants are mostly in Europe, with some in the US and Canada. The sample includes ten women, fifteen men and one person recorded as other; seventeen participants are25–34, with the remaining nine spread across four other age bands. This is a purposively reached professional sample, not a prevalence estimate for the industry.

Table1 distinguishes **two managers, seven designers without coding skills, thirteen designers with coding skills and four coders**. Reported AR/VR experience spans0.6–12years; nine formal-training marks are present. These skill classifications are different from the four overlapping task roles derived later. Except for managers, participants have prior2D application-development experience. The authors describe fifteen customer-driven and nine internally initiated projects, totaling24 rather than26; the paper does not identify the two omitted cases. It asserts application maturity above TRL5 without supplying an independent maturity assessment.

German or English video interviews use recent or ongoing work as an anchor. Questions derived from DAkkS usability-context guidance cover preparation, execution, evaluation and transfer, tools and artifacts, information exchange, comparisons with2D work and future wishes. Screen sharing permits showing tools/artifacts; this is not a longitudinal observation of every reported workflow. German transcripts are translated by a German native speaker with reported C1 English. The paper does not supply the complete question schedule, interview durations or a collection-date window.

Analysis uses open coding in MAXQDA and affinity diagrams in Miro. The coding scheme is developed/evaluated on eight interviews and then applied to the remaining eighteen. The authors explicitly describe an exploratory analysis without axial or selective coding. Coder count, an agreement statistic and saturation procedure are not reported. These limits bound reproducibility and population inference; they do not negate the specific practices and difficulties participants report.

## Work crosses overlapping roles

Section4, pp.5–6, describes project teams of one to ten creators. Participant employment contexts comprise three freelancers, ten in mixed core/freelance teams, one in a design department, one in a software department and eleven in mixed teams without freelancers. These are26 participant contexts, not26 independently sampled companies.

| Derived role | Participants performing it | Work and handoff |
| --- | ---: | --- |
| Concept development | 22/26 | Clarify need, context and feasibility; use requirements, photos and video to convey the intended situation. |
| Interaction design | 23/26 | Specify interaction modalities, movement and flows through sketches, storyboards and wireframes. |
| Content authoring | 10/26 | Supply meshes, animation, materials, sound and interface assets; only two participants report dedicated3D modeling skills, so premade or outsourced content matters. |
| Technical development | 15/26 | Consult on feasibility, select devices/frameworks/plugins/networking, integrate others' work and implement interactive prototypes. |

People perform multiple roles; the role counts must not be added as distinct participants. Artifacts can serve both as communication aids and as parts of the eventual product. The authors report that all participants' teams use Unity onp.6, while the limitation section says a majority of participants use Unity as an IDE. The wording and units differ; neither licenses a precise industry engine-share estimate. A few quote suffixes also differ from Table1's skill labels: ID23 is markedD in a quote butDC in the table, and ID3 is markedD in a quote butC in the table. The table classification is retained rather than reconstructing sample groups from quote suffixes.

Access to expertise and equipment is part of the workflow. Collaborators can resolve skill gaps, but some designers lack headset access because budgets prioritize people who produce code. A tool's nominal capability therefore does not imply that every relevant collaborator can inspect and change its output.

## Useful practices and reported costs

Sections5.1–5.3 and Table2, pp.6–10, group problems into three families. Preserve both the successful responses and the remaining burdens:

| Family | Reported challenge | Practices participants find useful; remaining boundary |
| --- | --- | --- |
| Understanding the medium | Marketing expectations, device limits and2D habits can obscure spatial attention, tracking, lighting, field of view and performance constraints. | Involve developers and designers early, try existing experiences, examine the intended site, and use quick feasibility mockups or mood boards. These are reported ways to build shared understanding, without a measured reduction in rework. |
| Moving between tools and representations | Specialized tools expose different features, exports, devices and skill requirements; rapid tool/hardware change adds learning and reuse work. | Prototype directly in an engine, combine physical and digital representations, and train across disciplines. Direct implementation can shorten the handoff while making code less editable by a non-programming designer. |
| Communicating intended behavior | Static sketches or prose can under-specify dynamic/spatial interaction; misunderstanding can produce incorrect implementations and rework. | Use animation, enacted or graybox prototypes, joint live coding and conversation. These artifacts support negotiation; producing and explaining them also costs time. |

The representation issue is concrete. Onp.8, ID11 describes putting interface layout into code and then losing a designer's ability to edit it. Mutual training is a positive response: designers learn the engine while developers learn design tools such as Figma. This is coordination work with an adoption cost, not evidence that either a graphical or textual representation universally wins.

Onp.8, ID1 wants to explore the timing of an interface that follows or rotates after a user's head moves away. This locates a real temporal/spatial intention that a prototype can help discuss. It does not establish that a formal temporal obligation, complete input coverage or a correctness oracle has been supplied. Physical prototyping similarly helps with scale and bodily context while carrying setup, remote-participation and spatial-sound limitations.

The prototype-to-product path onp.9 has both benefits and adverse consequences. Participants use an engine directly to save time and reuse work. Budget, deadlines and a client's impression of visible polish can then lead to shipping that prototype. Accounts describe consequent readability, reuse and maintenance problems, and reluctance to discard invested work. These are reported mechanisms and experiences; the study measures neither their prevalence nor a causal lifecycle-cost difference. Historical statements about specific tools, export support or device compatibility are retained as participant accounts, not verified current product specifications.

The shared-language theme concerns agreement among stakeholders. It is not automatically evidence for a programming-language type system or a particular domain vocabulary. Some participants describe implementing interactions from memory because writing an exact specification is difficult. That finding strengthens the need to distinguish visible/prototyped behavior, jointly understood intent and behavior actually checked.

## Discussion claims and transfer limits

Section6, pp.10–13, interprets the roles and artifacts and proposes task/role/goal-oriented tooling, reuse of familiar methods, adaptable shared artifacts, templates and structured exchanges. These are design implications, not evaluated interventions in this paper. Immersive authoring is proposed where appropriate to spatial work; the authors also recognize that abstract program logic may require other representations. No general immersive, low-code or template superiority follows.

The comparison with Ashtari et al.'s21-creator study is an author interpretation across studies, not a paired professional/end-user experiment. Section6.1 explicitly leaves detailed testing/evaluation practice outside its account. This reading therefore does not close the survey's temporal-oracle/testing frontier. Apparent use of agile processes also does not establish formal process adherence; the authors point to McKenzie et al.'s game-industry study for that distinction. Its original method must be read before adopting stronger claims about studios.

There is no randomized assignment, controlled treatment, measured defect/time contrast or Nu deployment here. The sample and engine concentration limit generalization. The evidence nevertheless supports specific reported benefits of collaborative prototyping, feasibility discussion and cross-training, alongside specific handoff, equipment, learning and maintenance burdens. Treating this solely as a catalogue of missing controls would discard its actual contribution.

## Consequence for Nu's value assessment

For B01/B08/B10/B11, the relevant unit is a **change completed across the roles and tools needed to deliver it**. A source representation can help one programmer while shifting translation or editing work to another person. Connect Nu's actual domain/state/history mechanisms to who can inspect and alter the representation, which intent can be shared, and the complete learning, integration, refactoring and maintenance burden. Compact source, rapid preview and prototype reuse remain useful candidate mechanisms; none alone supplies net team value.

Use this professional practice account alongside [S287 VRGit](S287-vrgit-history-and-collaboration.md), [S284 LevelMerge](S284-levelmerge-scene-merge.md) and [S283 NCCollab](S283-nccollab-collaboration-history.md). Their usability and comparative authoring findings retain their separate populations, tasks and outcome scopes. S288 helps interpret when those capabilities might matter; it does not retroactively turn them into industrial maintenance-effect estimates.

The next consequential primary route is **McKenzie, Morales Trujillo and Hoermann's2019 game-development practice study, DOI10.1145/3341215.3354647**. It directly addresses game teams and the relationship between claimed process labels and reported practices. Check the later2021 agile-study lineage before counting independent cases. DART's ten-year account, Ashtari's creator study and Musil's heterogeneous-team process work remain conditional dependencies when they can alter the mechanism or adoption account. The wider type, temporal, generation and primary-access gaps remain open. No construction, worker or experiment is authorized.

## Discovery and audit boundary

SC227's existing exact metadata supplied the selection; it is not repeated as a new S288 search. W722's resolver open fails; W723's two exact-title queries return14 panels and recover author-copy routes. Ordinary Zenodo and DNB acquisitions establish byte identity. All81 printed references were screened and aligned with the Crossref deposit by reference number;51 have deposited DOIs. That alignment is not independent DOI/title verification or81 primary readings.

SC228 requests **limit20, offset0**, for the DART and McKenzie DOIs and returns2/2. DART metadata includes three outgoing mentioning edges without citation snippets; they are dependencies, not incoming validation. Its truncated abstract and denied-content flag do not supply a method reading. McKenzie's readable/OA flag similarly does not establish body access. W724's exact-title query returns18 panels for the game-practice continuation, including a later-study route and already read S268. No S288 citation graph is newly requested, and these bounded routes do not establish field saturation. The search ledger records the considered-source decisions and inspected citation report.

Audit **`nu_background_s288_20261008`** accounts for124 occurrences and109 identities:2 credited,99 deferred and8 not used for this question. The176-file historical check identifies nine matches; S288 receives one material full-reading update and eight unchanged screens, including S268, are withheld. The101 submitted decisions comprise1 credited,92 deferred and8 not used, with100 reference/discovery stages and one full-paper stage. Receipt and inspected report each match all606 checked fields, with zero skips, missing reasons, linkage warnings or truncation. These are audit identities and routes, not109 independently verified studies.

All experimental and worker holds remain. No engine, candidate, model, benchmark or reproduction was run.
