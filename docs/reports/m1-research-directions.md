# Research directions for echo chambers in Brazil’s 2022 election

**Milestone M1 · Research directions and literature review**  
**Roadmap recorded on 2026-11-24**

What can the Interfaces Twitter Elections Dataset (ITED-Br) tell us about echo chambers among accounts, and which methods would let us characterize those groups credibly? The earlier study gives us a baseline for hashtag co-occurrence and candidate-relative stance. This milestone uses brainstorming and a focused literature review to decide which extensions are worth testing, what data they require, and how the thesis could evaluate them. [Prior-study note](../prior-study.md)

## Scope and working record

The assistant carries out the brainstorming, literature search and review, feasibility assessment from existing documentation, and synthesis. Use available sources to resolve routine questions and document uncertainties that would affect a later pilot. If a critical fact cannot be verified with available tools, identify the specific input needed and continue the independent parts of the review.

M1 ends with a research synthesis and a proposed pilot. Empirical testing, pipeline development and formal expert evaluation belong to a later milestone. Keep the current task and its status in [STATUS.md](../../STATUS.md). Add each step’s findings to this report or link a supporting note from it. Record the alternatives considered, the evidence that changed a decision, and the unresolved questions that could affect the shortlist. Treat the five initial avenues as research hypotheses.

## Step 1 — Frame the questions and plan the literature review

Turn the proposed avenues into questions the review can answer. Define the outcomes of interest, from candidate-relative stance and selective circulation to interpretation of group-level language. Specify what would make an avenue add something to the prior study. Plan to search in English and Portuguese for work on political echo chambers, graph methods, campaign discourse, explainability and validation, including studies of Brazil and the 2022 election. Keep a search log with sources, dates, queries, inclusion criteria and key references followed.

**Deliverable.** A short set of research questions and a review protocol. For each retained study, capture the population and sampling, what it measures, how it validates the measure and what would transfer to ITED-Br.

**Result.** The [review protocol](m1-review-protocol.md) records five questions, the screening criteria, the evidence to extract for each study, and the trial search log. The main question asks what account-level observations would support an echo-chamber interpretation. Trial searches favored running each strand separately, with dedicated searches for Brazilian evidence and transferable methods.

## Step 2 — Establish what the data and prior study can support

Use existing dataset and study documentation to make an inventory of fields, coverage and access. Check what is known about account and post identifiers, timestamps, reposts, replies, quotes, referenced posts, text and links. Record how the election collection queries and time windows could affect comparisons, and flag missing targets or unresolved field availability. Locate the earlier graph specification, seed labels and code if available. Record the open question about how seed hashtags were selected. Where documentation leaves a field or assumption unverified, record the uncertainty and which proposed analyses depend on it.

**Deliverable.** A feasibility table that maps each proposed analysis to its minimum data requirements, records which inputs are documented or still uncertain, and identifies what could be checked in a later pilot.

**Result.** The [ITED-Br feasibility report](m1-ited-br-feasibility.md) verifies public linkage fields and October partitions, identifies which questions require hydrated data, and locates the earlier graph and stance code. A repost-to-target-author join is the first structural check proposed for a later pilot. The seed workbooks and original selection procedure remain unresolved.

## Step 3 — Review automatic detection, membership and information flow

Compare definitions of an echo chamber and methods that turn them into observable criteria. Brainstorm how to find candidate account groups, estimate core or uncertain membership, recover the posts and sources that members produce or share, and trace circulation within and across groups. Compare measures of selective interaction or circulation against plausible reference patterns, such as a null model that preserves account degree. Consider what conclusions are possible when only some repost or quote chains can be reconstructed. Favor validation evidence distinct from the signals that formed the groups, such as a held-out interval or a different observed interaction layer.

**Deliverable.** A comparison of candidate definitions and detection procedures, with the data each needs, the evidence that would support or weaken an echo-chamber interpretation, and the proposed outputs for groups, membership and circulation.

**Result.** The [Step 3 report](m1-echo-chamber-detection.md) proposes a directed account repost graph, validation on a separate time interval with a degree-preserving reference model, and explicit checks for missing endpoints. It identifies prior network studies of Brazil’s 2022 election and states what additional evidence would be needed to support political selectivity or trust claims. Supporting sources and search decisions are in the [Q1 evidence notes](m1-q1-evidence.md). The subsequent [Reflexive report 3](reflexive-report-3.md) extends this design to group-pair excess flows, viral-source sensitivity and distinct-original repertoires.

## Step 4 — Compare graph construction and label-spreading methods

Review alternatives for the earlier hashtag graph and for account-level interaction graphs. For each, specify nodes, edge meaning and direction, weights, time windows and expected scale. Use the prior study’s Gaussian Fields and Harmonic Functions (GFHF) method as the stance-propagation baseline. Shortlist alternatives to compare against it and against a simple baseline. Draft a comparison that can vary graph construction and label-spreading algorithm independently, account for possible bias toward frequent seed hashtags, and evaluate performance on held-out evidence. Compare the cost and interpretability of graph choices alongside their effect on results.

**Deliverable.** A small set of baseline and alternative configurations with the rationale, proposed evaluation and computational assumptions for each.

**Result.** The [graph methods report](m1-graph-methods.md) proposes crossing raw and fractional hashtag co-occurrence with GFHF and LGC, using fixed inputs and splits and testing sensitivity to frequent seeds. For account communities, it compares directed modularity and Infomap on matched repost graphs. Both tracks specify coverage, validation and cost measures. The [Q2 evidence notes](m1-q2-evidence.md) record the literature and implementation checks.

## Step 5 — Draft a taxonomy for political language and tactics

Review work on Brazilian Portuguese campaign language, stance and misinformation. Sketch categories for who is targeted, whether the message supports or attacks them, and how that stance is expressed. Give rhetorical tactics, factual verification and evidence of coordinated or deceptive behavior their own criteria. Decide whether the first coding unit should be a post, claim or interaction, and how those annotations could be summarized at group level. Include ambiguity, sarcasm, quotations and relevant election context in the annotation guidance.

**Deliverable.** A draft taxonomy with definitions, inclusion and exclusion criteria, provisions for ambiguous cases, and a proposal for comparing category frequencies across groups while accounting for their size and activity.

**Result.** The [draft political-language taxonomy](m1-political-language-taxonomy.md) defines the post–target stance unit, codes with inclusion and exclusion rules, and how to document claim verification and evidence of coordination. It includes Brazilian Portuguese examples and estimands for authored and amplified content that account for group size, activity and missing context. The [Q3 evidence notes](m1-q3-evidence.md) record the sources and search.

## Step 6 — Assess LLM-assisted explanations of groups

Review ways to explain why a group was identified and what characterizes it using graph measures, circulation summaries and permitted linguistic evidence. Define which claims an LLM could make from a supplied evidence set and what format would let a reader verify each claim. Compare against a structured evidence summary without an LLM. Plan to evaluate factual grounding, attribution of claims to evidence, unsupported inferences, and handling of Brazilian Portuguese and political context.

**Deliverable.** A candidate explanation format and evaluation rubric, illustrated with a hypothetical group. State what evidence an explanation would need for each type of claim.

**Result.** The [LLM explanation design](m1-llm-group-explanations.md) defines which claims a group description can make, a claim-level evidence format, and a comparison against a fixed summary using the same data. The worked example and rubric cover grounding, missing evidence, Brazilian Portuguese context and reader usefulness. The [Q4 evidence notes](m1-q4-evidence.md) record the research and search process.

## Step 7 — Design validation with political science experts

Draft a small review for a later milestone. Identify which claims would require independent judgment from the research group’s political scientists and what automated checks could establish beforehand. Define what they would see and judge, including whether selected groups meet the proposed echo-chamber criteria, whether the taxonomy captures meaningful distinctions, and whether explanations are accurate and informative. Include clear cases and near misses. Propose independent judgments before discussion, criteria for interpreting disagreement, and a practical estimate of reviewer effort. Where feasible, hide which method produced an output until after the initial assessment.

**Deliverable.** A draft protocol with sample selection, review materials, criteria and a plan to document agreement, disagreement and resulting changes to the methods.

**Result.** The [expert validation protocol](m1-expert-validation.md) defines the cases, evidence packets, Portuguese review form and effort for assessing group interpretations, language categories and explanations. It specifies automated checks, independent review, and how disagreement changes the analysis. The [Q5 evidence notes](m1-q5-evidence.md) record the methodological precedents.

## Step 8 — Select the most promising directions for a pilot

Compare the proposed directions on thesis contribution, data feasibility, strength of validation and effort. Cite the literature and feasibility findings behind the ranking. Explain which ideas depend on others, which merit prioritizing, and which can be deferred or revisited when evidence or data availability changes. Outline a bounded pilot for the leading direction with a baseline, expected outputs and criteria for deciding what to do next.

**Deliverable.** An advisor-ready synthesis with a ranked shortlist and a proposed first pilot. Flag any decision that genuinely needs the researcher’s or advisor’s input and explain what depends on it.

**Result.** The [advisor synthesis and first pilot](m1-advisor-synthesis.md) ranks the five directions and recommends a bounded public-data study of observed reposts, with target-author coverage as the first checkpoint. It records the baseline, expected outputs and criteria for expanding, narrowing or stopping the pilot.

## Milestone completion

M1 was completed on 2026-11-25. The [advisor synthesis](m1-advisor-synthesis.md) records the evidence and disposition of all five avenues, the major data uncertainties, and a proposed pilot with a route to validation.
