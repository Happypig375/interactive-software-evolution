# S301 — Documented rule interfaces improve selected maintenance outcomes

J. Steve Davis, *Effect of modularity on maintainability of rule-based systems*, International Journal of Man-Machine Studies 32(4), April 1990, pp. 439–447. [DOI 10.1016/S0020-7373(05)80141-5](https://doi.org/10.1016/S0020-7373(05)80141-5).

**Coverage updated 2026-10-08:** the newly attached journal-layout PDF resolves the earlier body-access gap. All nine pages are read textually and visually, including Figure 1, Tables 1–4, the acknowledgment and all eleven references. There is no appendix. The original access assessment remains in Git history; this filename is retained to preserve existing links. No program, participant artifact or analysis is executed here.

## The actual treatment

The study evaluates Jacob and Froscher's method for grouping rules and documenting information flow (§§2–3, pp. 440–441). It separates facts used to enable/disable firing from facts that carry information, groups rules to minimize inter-group data flow, and documents the facts each group produces or uses. The experiment uses IBM's fourteen-rule ANIMAL demonstration, a small familiar classification problem. The original version has an unstructured rule listing; the treatment documentation organizes the same system into CLASS, BIRD and MAMMAL groups with declared interfaces and short explanations of produced facts.

**This is structuring through documentation.** The conclusion explicitly distinguishes it from future work using software encapsulation to enforce the interfaces (p. 446). Both groups receive documentation and the original system file; the contrast combines grouping, interface information and presentation. It is not a comparison of enforced module boundaries, pure versus mutable code, programming languages, or different runtime algorithms. Figure 1 shows an abbreviated documentation example, with simplified rule syntax, rather than the complete experimental packet.

## Task and observation boundary

Participants incorporate two pieces of knowledge from a supplied biologist-interview handout: paddling identifies the bird class, and a hairless bird is a Coot-duck (§4). The intended staged solution updates or adds a classification rule and a specific-animal rule. Participants are asked to preserve the logical organization if they recognize it. The example knowledge is a laboratory specification, not a test of biological realism.

The investigator desk-checks each knowledge item on a 0–3 scale: no attempt, severe errors, minor errors, or correct. Correctness is explicitly intended to cover the new classification and previously represented animals (p. 442). The published method does not supply a complete executable test oracle, individual submissions, assessor blinding or inter-rater reliability. Participants can test their own changes and stop when satisfied; their stopping decision is distinct from the subsequent correctness score.

A separate **quality** score is 3 for a correct modification consistent with the staged logical structure and 0 otherwise. This includes conformity to the requested organization. It is not a general measure of behavioral correctness or future maintenance cost. The author criticizes a one-rule identification patch as awkward; a future Nu protocol must independently specify which behavior is required and allow correct alternative organizations when the treatment does not require structural preservation.

## Two experiments and their outcomes

Experiment 1 uses twenty volunteer graduate students who have just completed a semester expert-systems course with IBM ESE (§5). After an introduction to the modularity method, they are explicitly randomly assigned to documentation groups of ten. They work on a time-sharing mainframe for up to two hours, can leave when finished, and submit a listing plus a seven-point confidence/helpfulness questionnaire.

Experiment 2 uses 54 volunteer undergraduate MIS students, with extra course credit and an introductory expert-systems sub-course (§6). It converts ANIMAL to the easier-to-learn TIGER PC shell and allows one hour because of scheduling constraints. There are 27 participants per documentation group. The procedure says it follows Experiment 1 except for the described differences; it does not separately describe the allocation sequence. These are two samples with different experience, systems and time limits, not a randomized comparison of expertise or platform.

| Endpoint | Experiment 1: modular / non-modular | Experiment 2: modular / non-modular | Published inference |
| --- | --- | --- | --- |
| Bird-knowledge score, maximum 3 | 1.60 / 0.80 | 2.26 / 1.04 | Experiment 1 score differences are not significant in the reported ANOVA; Experiment 2 reports p < .05 for both knowledge scores. |
| Coot-duck-knowledge score, maximum 3 | 3.00 / 2.60 | 2.63 / 2.26 | Preserve the favorable direction in both samples without turning the Experiment 1 null into equivalence. |
| Correct-and-structure-conforming quality | 1.70 / 0.60 | 1.56 / 0.56 | Experiment 1 reports no significant difference; Experiment 2 reports significantly higher quality. |
| Mean elapsed modification time | 46.4 / 62.8 minutes | Not reported | Experiment 1 reports significance at the .05 level. Its means include unsuccessful or imperfect submissions, rather than establishing time to verified correct completion. |

The mainframe time difference is 16.4 minutes. The author says slow system responses inflated elapsed time and that these times need not equal working time; no measured response-time decomposition is supplied. There is no reported timing effect for Experiment 2. Neither experiment reports dispersions, exact test statistics, confidence intervals or participant-level data sufficient to reproduce the inference. Tables retain the stated 10/10 and 27/27 sample sizes; no success-only restriction or attrition is reported. This does not identify the joint distribution of time and correctness.

There is a small reporting inconsistency that cannot be repaired from the paper: with ten participants and a quality score restricted to 0 or 3, the Experiment 1 modular mean would occur in increments of .3, whereas Table 1 visibly prints **1.70**. Preserve the printed value and stated scoring rule; do not invent corrected counts or a different scoring scale. The inconsistency does not erase the independently reported timing result or Experiment 2 outcomes.

Tables 2 and 4 preserve the attitude results. Experiment 1 confidence in correctness is 6.7/6.1 and confidence about side effects 6.3/5.7, while documentation-helpfulness ratings slightly favor the other group (5.6/6.0 and 5.2/5.5); available-time ratings are 6.2/6.2. The author reports no appreciable attitude difference. Experiment 2 reports generally greater confidence with modular documentation: correctness 5.0/4.8, side effects 5.5/4.5; usefulness 4.6/4.3 and 5.0/4.8; available time 5.1/4.9. These self-reports do not replace the scored submissions or establish a preference between documentation forms that each participant has not compared.

## What this changes for Nu

Preserve the positive evidence: explicit rule grouping and documented interfaces can help people perform a selected change, including undergraduates with little relevant experience. This is a closer outcome comparison than a modularity metric or an abstract benefit claim. It complements the task-dependent understanding/progress evidence in [S300](S300-cognitive-fit-and-modification.md) and the formal contract in [S299](S299-modular-reactive-verification.md), while measuring a different intervention and outcome.

For B01/B03/B10/B11/B12, the useful hypothesis is that making dependencies and intermediate classifications legible can reduce the work of locating and integrating a change. A Nu comparison must account for the information and training each condition supplies, rather than crediting the language or runtime for a documentation difference. Source organization, actual behavior, preferred structure, confidence and total effort remain separate. The study's two student samples, one small program and one change do not establish a Nu, professional-game or coding-agent effect.

The paper predicts benefits for larger systems and negligible added development effort and recommends adoption pending further evaluation. These are author expectations, not measured construction costs, evidence of no harm or demonstrated scale transfer. The original Jacob/Froscher account remains a conditional method dependency if a stronger interface-enforcement claim needs it; it is not necessary to erase this study's documented-treatment result.

## Native attachment, identity and remaining evidence

The existing native parent **`3F9RPR99`** version 6045, note **`G65JEDJC`** version 6044 and membership in collection `PKLXQNEE` are checked before reading. Newly supplied PDF **`2VYSC6MS`** version 6092 contains nine printed journal pages 439–447 and agrees with the title, author and 1990 journal identity. Its **470,562 bytes** have SHA256 `2b465b8a86313241112c239ccda691cd0a722c4ce7f0a41e60aee524517d9922` and MD5 `f6370299aef04bb8366ea03f89d3dfa9`. The 22,924-character extraction contains OCR errors; all rendered pages resolve the tables, figure, layout and relevant wording. No PDF hyperlink provides a supplemental packet.

The previous publisher 403 and denied Scite body are superseded for reading by the user's attachment; no fresh failed access route is counted. Complete code, handouts, raw scores, timing logs and analysis are still unacquired, and no independent replication is claimed. Final native versions, exact-note verification and the source-decision audit are recorded in the [search ledger](../nu-background-searches-2026-09-30.md). Copyrighted PDF bytes, extraction and renders remain outside Git.
