# Research progress

Last updated 2026-11-26.

| Current milestone | Current task | Status |
| --- | --- | --- |
| M3 · Within-corpus repost pilot | [Implement and verify discovery and freeze the run manifest](docs/reports/m3-repost-pilot-specification.md) | In progress. Holdout outcomes remain unopened. |

## M3 · Within-corpus repost pilot

**Objective.** Measure excess internal reposting in frozen account groups and test whether groups improve prediction beyond prior sharer–author ties.

**Completion condition.** Archive a reproducible discovery freeze, validated comparisons, holdout estimates and sensitivity results or a documented feasibility limit.

**Current task.** Complete the registered discovery grids and sensitivity fits, calibrate the rolling prediction models, and validate the reference before archiving the partition and executable manifest. Keep holdout outcomes unopened.

**Specification handoff, 2026-11-26.** Registered [protocol v1](docs/reports/m3-repost-pilot-specification.md) with a discovery-only selection rule, matched post-slot reference, history-aware prediction and interpretation thresholds. The executable manifest and fitted partition are pending implementation and verification.

**Implementation checkpoint, 2026-11-26.** Reconciled 6,764,928 eligible discovery actions, matching M2 coverage in all nine discovery strata. Both optimizers passed the directed fixture, and small synthetic inference and prediction checks passed. The empirical grid, discovery calibration and executable freeze are pending. [Implementation report](docs/reports/m3-discovery-implementation.md) · [Aggregate extract](docs/reports/m3-discovery-extract.json)

**Discovery fitting checkpoint, 2026-11-26.** Rechecked the M2 footer fingerprint and ran discovery-only calibration for context and tie history across 3,570,755 validation actions. Weighted and binary Leiden, fold Leiden, weighted Louvain and Infomap fits are underway. Group calibration and partition-dependent perturbations await the selected grids. [Implementation report](docs/reports/m3-discovery-implementation.md#discovery-fitting-checkpoint)

**Thesis direction handoff, 2026-11-26.** The [integrated synthesis](docs/reports/thesis-direction-synthesis.md) sets out the structural baseline, distinct-item circulation and a priority study of Brazilian Portuguese repertoires. The [M3 protocol](docs/reports/m3-repost-pilot-specification.md) governs the current pilot. The language extension starts with a coverage and attribution audit before independent coding, graph comparisons or prediction with language features.

## M2 · Repost feasibility and coverage

**Objective.** Measure which observed Lula- and Bolsonaro-context reposts from 16–21 October 2022 have a verified action date, sharing account and historical original author.

**Completion condition.** Archive the reproducible audit, input description, aggregate coverage by day and query, exclusions and a decision to proceed, narrow or stop. The [M2 report](docs/reports/m2-repost-coverage-audit.md) defines the counts and handoff.

**Inventory handoff, 2026-11-26.** Verified explicit repost types, UTC action timestamps, folder-based provenance and historical join fields. File dates differ from São Paulo action dates. The [inventory and aggregate counts](docs/reports/m2-repost-coverage-audit.md#host-inventory-completed-2026-11-26) document the checks. Distinct action counts and author resolution remain open.

**Audit handoff, 2026-11-26.** Reconciled 11,988,989 distinct verified reposts and identified both accounts for 11,960,224 (99.760%). The [advisor report](docs/reports/m2-repost-coverage-audit.md#what-did-we-learn) and [aggregate output](docs/reports/m2-repost-coverage.json) record losses by day, query, target reuse and sharer activity. Proceed with the within-corpus pilot. Freeze discovery-only choices and recompute missing-endpoint bounds for assigned sharers before interpreting holdout outcomes.

## Research design assessment

**Objective.** Assess what the prior article, M1 and the eight reflexive reviews contribute to a Computer Science thesis on political echo chambers, and identify the most consequential gaps.

**Completion condition.** Archive an advisor assessment that distinguishes evidence in hand from proposed tests, identifies a feasible core contribution and explains how the original questions about language, circulation and trust can develop from it.

**Handoff, 2026-11-26.** The researcher adopted the [assessment](docs/reports/research-seed-assessment.md) and opened [M2](docs/reports/m2-repost-coverage-audit.md). The audit comes first. Its results determine whether to test what frozen account groups add beyond familiar sources. The selected language follow-up compares authored and amplified candidate criticism.

## Incremental reflexive review

**Objective.** Revisit the completed M1 design one research review at a time, recording decisions, evidence limits and implications for the relevant protocols.

**Report 1 completion condition.** Consolidate the conversation and Deep Research output into a single advisor report and reconcile the explanation, expert-review and synthesis documents. The [revised design](docs/reports/reflexive-report-1.md) is ready for later testing. Real packets depend on the [proposed public-data pilot](docs/reports/m1-advisor-synthesis.md#proposed-first-pilot).

**Report 2 completion condition.** Consolidate the conversation and Deep Research PDF into one [advisor report](docs/reports/reflexive-report-2.md) and align the Q3 question, [codebook](docs/reports/m1-political-language-taxonomy.md), [evidence notes](docs/reports/m1-q3-evidence.md), expert protocol and ranked synthesis. The design is registered. Language estimates depend on recoverable text and independent validation.

**Report 3 completion condition.** Register the circulation review as one [advisor report](docs/reports/reflexive-report-3.md) and reconcile the Q1 question, feasibility audit, detection protocol and first pilot. The design is registered. The first empirical dependency is a dated, typed event table with measured target coverage. Distinct-post overlap is the first structural extension.

**Report 4 completion condition.** Register the stance review as one [advisor report](docs/reports/reflexive-report-4.md) and align Q2, the graph benchmark, feasibility record and ranked synthesis. The design is registered. A documented hashtag extract and independent reference labels are the first dependencies. Contextual evaluation additionally requires attributable Portuguese text.

**Report 5 completion condition.** Consolidate both reviews into one [statistical validation protocol](docs/reports/reflexive-report-5.md) and reconcile Q1, the eligible population, reference models and pilot decisions. The design is registered. Action provenance, empirical coverage, sampler validity and network power remain to be established.

**Report 6 completion condition.** Register the [graph-discovery benchmark](docs/reports/reflexive-report-6.md) and align the detection, graph-methods and first-pilot protocols with the discovery-only method choice. The design is registered. Verified event fields, the directed implementation check and empirical stability remain open.

**Report 7 completion condition.** Register the [feasibility review](docs/reports/reflexive-report-7.md) and reconcile the first pilot with the pinned schema evidence, historical-author lookup, event-time requirements and missingness decision. The design is registered. True repost classification, historical endpoint recovery, dating and robustness remain empirical questions.

**Report 8 completion condition.** Consolidate the [conceptual-validity review](docs/reports/reflexive-report-8.md) and reconcile the research questions, detection protocol and advisor synthesis with its terminology and falsifiers. The interpretation rules are registered. Feasibility, structural persistence, political coherence and selective uptake remain unmeasured.

## M1 · Research directions and literature review

**Objective.** Use brainstorming and a focused literature review to identify promising directions for extending the prior hashtag-network study and propose a first pilot.

**Completion condition.** The advisor report assesses all five initial avenues against the literature, data feasibility and validation needs, and records a ranked shortlist with a proposed first pilot.

[Advisor synthesis and first pilot](docs/reports/m1-advisor-synthesis.md) · [Eight-step roadmap and supporting reports](docs/reports/m1-research-directions.md)

## M0 · Repository setup

**Completion condition.** A collaborator can find the project scope, recover the methodological starting point, see what work is active, and tell where future research records and local data belong.

| Outcome | Evidence |
| --- | --- |
| Document the research aims and provide an entry point | [Project overview](README.md) |
| Establish working instructions for tracking, archiving, data handling and reproducibility | [Project instructions](AGENTS.md) and [local file exclusions](.gitignore) |
| Record the relevant methods, limitations and source revision of the earlier study | [Prior-study note](docs/prior-study.md) |

## Work log

| Date | Milestone | Progress |
| --- | --- | --- |
| 2026-11-21 | M0 · Repository setup | Opened the tracker in the empty repository. |
| 2026-11-21 | M0 · Repository setup | Completed the setup outcomes above. The research question, dataset slice, graph design and validation criteria remain open for a later milestone. |
| 2026-11-24 | M0 · Repository setup | Added [advisor reporting guidance](AGENTS.md#research-reports-for-the-advisor) for documenting substantive progress, conclusions and their supporting evidence. |
| 2026-11-24 | M1 · Research directions and literature review | Opened M1 and registered the [roadmap](docs/reports/m1-research-directions.md) with deliverables for each step. |
| 2026-11-24 | M1 · Research directions and literature review | Updated the [roadmap](docs/reports/m1-research-directions.md#scope-and-working-record) for autonomous brainstorming, literature review and analysis. The pilot and formal expert validation are planned for later milestones. |
| 2026-11-24 | M1 · Research directions and literature review | Completed Step 1. Recorded the [research questions and literature review protocol](docs/reports/m1-review-protocol.md), including a bilingual trial search log and the evidence to extract from each study. |
| 2026-11-24 | M1 · Research directions and literature review | Completed Step 2. Published the [ITED-Br feasibility and prior-code inventory](docs/reports/m1-ited-br-feasibility.md), including coverage limits, the public linkage fields and the missing inputs for reproducing the stance baseline. |
| 2026-11-24 | M1 · Research directions and literature review | Completed Step 3. Published the [echo-chamber detection and circulation review](docs/reports/m1-echo-chamber-detection.md) with a held-out validation design, missing-data checks, and a [search and evidence log](docs/reports/m1-q1-evidence.md). |
| 2026-11-24 | M1 · Research directions and literature review | Completed Step 4. Published the [graph and label propagation comparison](docs/reports/m1-graph-methods.md) and [Q2 evidence notes](docs/reports/m1-q2-evidence.md), including matched configurations, seed-selection checks and measures of coverage, performance and cost. |
| 2026-11-24 | M1 · Research directions and literature review | Completed Step 5. Published the [draft political-language taxonomy](docs/reports/m1-political-language-taxonomy.md) with Portuguese coding examples, verification rules and a group-comparison plan, alongside the [Q3 search and evidence notes](docs/reports/m1-q3-evidence.md). |
| 2026-11-24 | M1 · Research directions and literature review | Completed Step 6. Published the [LLM explanation format and evaluation rubric](docs/reports/m1-llm-group-explanations.md) with a fictional Portuguese example, a matched structured baseline and the [Q4 evidence notes](docs/reports/m1-q4-evidence.md). |
| 2026-11-24 | M1 · Research directions and literature review | Completed Step 7. Published the [expert validation protocol](docs/reports/m1-expert-validation.md) and [Q5 evidence notes](docs/reports/m1-q5-evidence.md), including a Portuguese review form, matched case selection, time estimates and a disagreement procedure. |
| 2026-11-25 | M1 · Research directions and literature review | Completed Step 8 and closed M1. Published the [advisor synthesis](docs/reports/m1-advisor-synthesis.md) ranking all five directions and proposing a public-data repost pilot with scope and decision criteria. |
| 2026-11-25 | Reflexive review · Report 1 | Integrated both source reviews into the [three-format comparison and expert evaluation](docs/reports/reflexive-report-1.md). Documented feasibility limits, disagreement handling and criteria for a larger thesis role. |
| 2026-11-25 | Reflexive review · Report 2 | Integrated both reviews into the [Q3 measurement design](docs/reports/reflexive-report-2.md). Recorded the text-coverage decision, independent Portuguese annotation and model benchmark, four authorship/circulation estimands, and outcomes that would narrow a group claim. The public-data structural pilot retains priority. |
| 2026-11-25 | Reflexive review · Report 3 | Integrated [held-out author flow and original-post repertoires](docs/reports/reflexive-report-3.md) into the [first pilot](docs/reports/m1-advisor-synthesis.md#proposed-first-pilot). Recorded endpoint bounds, viral-source sensitivity, audience-defined source groups and the data required for event, stance and interaction-layer comparisons. Empirical outcomes remain open. |
| 2026-11-25 | Reflexive review · Report 4 | Integrated the [stance benchmark and falsification criteria](docs/reports/reflexive-report-4.md) into Q2. Recorded the historical reconstruction limits, six controlled graph configurations, two distinct fractional weighting rules, matched text controls and the evidence needed for independent community interpretation. |
| 2026-11-25 | Reflexive review · Report 5 | Registered the [held-out statistical protocol](docs/reports/reflexive-report-5.md) and revised the [first pilot](docs/reports/m1-advisor-synthesis.md#proposed-first-pilot). Adopted global inference, a day- and collection-conditioned original-post reference, a prior-tie benchmark, missingness and concentration checks, and untouched replication. |
| 2026-11-25 | Reflexive review · Report 6 | Integrated the [comparative graph review](docs/reports/reflexive-report-6.md). Recorded the conditional Leiden primary, Louvain fallback, Infomap comparison, hub and date perturbations, and the evidence needed for role, bipartite and temporal extensions. |
| 2026-11-25 | Reflexive review · Report 7 | Integrated the [measurement-feasibility review](docs/reports/reflexive-report-7.md) and revised the [first pilot](docs/reports/m1-advisor-synthesis.md#proposed-first-pilot). Replaced the fixed join threshold and neighboring-day lookup cap with a global historical lookup, stratified bounds and sensitivity of the held-out excess. Public ITED-Br supports an audit now. A substantive result remains conditional. |
| 2026-11-26 | Reflexive review · Report 8 | Integrated the [conceptual review](docs/reports/reflexive-report-8.md) into [Q1](docs/reports/m1-review-protocol.md#research-questions) and the [first-pilot decisions](docs/reports/m1-advisor-synthesis.md#decision-criteria). A positive structural test supports excess internal sharing over the tested dates. Independent political labels and a documented opportunity comparison govern stronger terminology. The feasibility audit remains the next empirical dependency. |
| 2026-11-26 | Research design assessment | [Assessed the thesis seed](docs/reports/research-seed-assessment.md) against the original brief and prior manuscript. Identified the added contribution relative to same-election work, the missing empirical evidence, and a candidate-specific language comparison worth preserving. |
| 2026-11-26 | M2 · Repost feasibility and coverage | Adopted the assessment and opened the [six-day coverage audit](docs/reports/m2-repost-coverage-audit.md). Defined the first output and the Ubuntu host inventory that begins empirical work once access is available. |
| 2026-11-26 | M2 · Repost feasibility and coverage | Completed the [host inventory](docs/reports/m2-repost-coverage-audit.md#host-inventory-completed-2026-11-26) and verified that the audit needs action dates from the records and a wider partition search. |
| 2026-11-26 | M2 · Repost feasibility and coverage | Completed the [full reconciliation and historical-author audit](docs/reports/m2-repost-coverage-audit.md#full-action-and-historical-author-reconciliation). Verified the host manifest, confirmed raw repost row counts independently, and retained both windows and all three query strata for the next pilot. |
| 2026-11-26 | M3 · Within-corpus repost pilot | Registered the [pilot specification](docs/reports/m3-repost-pilot-specification.md) before opening holdout outcomes. |
| 2026-11-26 | Thesis design | Mapped the [prospective computational pipeline](docs/reports/thesis-computational-pipeline.md) from Parquet reconciliation to community discovery, held-out reference testing, author prediction and conditional political interpretation. The M3 specification governs pilot execution. |
| 2026-11-26 | Thesis design | Recorded the researcher's observation of culturally distinct hashtag clusters and mapped [prospective tests of linguistic repertoires](docs/reports/linguistic-repertoire-hypothesis.md) for community characterization, graph construction and held-out author prediction. |
| 2026-11-26 | Thesis design | Integrated the [research direction and study sequence](docs/reports/thesis-direction-synthesis.md). Defined the roles of the repost baseline, distinct-item circulation, independent language validation and matched tests of linguistic information. |
