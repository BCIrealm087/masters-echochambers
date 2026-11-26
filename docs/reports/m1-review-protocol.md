# Research questions and literature review protocol

**M1 · Step 1 · 2026-11-24**

Do account groups discovered in Brazilian election discourse predict excess internal reposting later, and how much political meaning can independent evidence give that pattern? The review will start with observed interactions and circulation among accounts. It will assess stance, discourse and explanations in relation to that evidence. This extends the earlier study, which used hashtag co-occurrence and candidate-relative stance. The five questions below guide a focused scoping review and the choice of a later pilot. [Prior-study note](../prior-study.md)

## Research questions

| Question | Unit and evidence to look for | What would extend the prior study |
| --- | --- | --- |
| Q1 · How much internal reposting persists after accounting for activity, original-post popularity, collection context and prior ties? Which groups amplify the same authors or originals, and are they independently coherent in political orientation? | Assess account-group stability across directed objectives, weights, hubs and dates using discovery data. Freeze the primary partition before testing later reposts. [Discovery benchmark](reflexive-report-6.md) Test global excess under the stratified post-level null, then compare historical-tie prediction with and without group membership. Assess distinct-original overlap separately. | Observed and expected rates, percentage-point excess, Holm-adjusted group comparisons, coverage bounds, source concentration, item overlap and untouched replication. Report congruence and cross-cutting amplification using independent labels. Selective uptake requires observable alternatives. [Report 8](reflexive-report-8.md) [Circulation measures](reflexive-report-3.md) · [Statistical protocol](reflexive-report-5.md) |
| Q2 · How reliably does candidate-relative hashtag stance generalize across graph constructions, seed choices, frequency bands and contextual uses? | Score conventional hashtag meaning and stance in each authored use separately. For account orientation, require independently coded histories over a defined interval. Match graph and text controls at each unit. | Independent human reference labels, cross-unit agreement, errors and coverage by class and frequency, robustness to seed and graph choices, and incremental value at comparable coverage. [Report 4](reflexive-report-4.md) |
| Q3 · How do frozen repost communities differ in candidate-relative stance and rhetoric, and how does what members author compare with what they amplify? | Attribute stance to speaker and target, ground functions and mechanisms in spans, and distinguish verified propositions from observed sharing. | Compare posts, authors, distinct sources and repost events with coverage, independent validation and uncertainty. [Reflexive report 2](reflexive-report-2.md) |
| Q4 · What can an LLM add to a verifiable explanation of a group? | Checkable claims in a group explanation, supported by supplied graph evidence, circulation summaries or permitted textual evidence. Seek evaluations of claim support, evidence coverage and factual errors, with a structured summary of the same evidence as a comparison. | Evidence of added interpretive value while reviewers can trace each claim to evidence and detect unsupported inferences. |
| Q5 · Which judgments need independent political science expertise, and how could they be evaluated consistently? | Annotated examples and group explanations. Look for review protocols with independent judgments, explicit criteria, examples near category boundaries, and ways to report disagreement. | A feasible way to assess construct validity and interpretive usefulness alongside computational checks of stability, reproducibility or agreement. |

Q1 distinguishes five questions about structural persistence, political coherence, competing explanations, uptake given observable opportunities, and expressed distrust. The latter two require additional data. Their evidence requirements and negative outcomes are specified in the [conceptual review](reflexive-report-8.md#research-questions-and-evidence-needed-to-answer-them).

A graph partition identifies candidate groups. An echo-chamber interpretation requires further evidence about the interactions or circulation in scope. When reviewing a paper, check whether its validation reuses the same signals that defined its groups or assigned their stance. Where possible, consider a held-out interval, a different interaction type or independent judgments. Record inferred exposure or trust alongside the evidence and additional assumptions that such a claim requires.

## Search and screening protocol

1. **Run focused searches in English and Portuguese.** Search the scholarly web for each question using the terms below. Supplement results with targeted searches of SciELO and Brazilian communication and political science journals for local studies, and of disciplinary sources such as ACL Anthology and proceedings archives for methods. Verify publication details against the publisher or official proceedings. Keep the 2022 Brazilian election as the primary empirical context and allow earlier foundational or transferable work from other contexts.
2. **Screen by relevance and available evidence.** As a starting limit, screen the first 20 returned records per query, or all available when fewer are returned. Deduplicate by DOI or normalized title before screening by title and abstract. Retain work that addresses a question directly or contributes a method, measurement distinction or contextual finding that could transfer. Include substantive peer-reviewed articles and conference papers, scholarly reviews, and primary dataset documentation. Where a pertinent preprint is the only source, label its publication status. Record whether the methods and validation details could be inspected. Keep abstract-only items as discovery leads until enough evidence is available to assess the method. Exclude opinion pieces, tangential papers and duplicate versions, recording the reason after full-text screening where applicable.
3. **Follow the strongest references.** For each question, select at least one promising source when available and check one round of its cited work and later work that cites it. Record both the starting reference and which records were found through it. Run a targeted follow-up if the evidence still lacks an important context, comparator or counterexample. Document any expanded search, inaccessible papers and unresolved gaps so the bounds of the review are clear.
4. **Extract comparable evidence and synthesize by question.** Use the record below even when a result is negative or inconclusive. Note whether apparent disagreements reflect different graph definitions, samples or meanings of “echo chamber.” In the milestone synthesis, compare candidate directions on contribution, required data, validation strength and effort.

| Topic | English query terms | Portuguese query terms |
| --- | --- | --- |
| Q1 · Groups and circulation | “echo chamber”, “selective exposure”, “political homophily”, “retweet network”, “information diffusion” | “câmaras de eco”, “exposição seletiva”, “homofilia política”, “rede de retuítes”, “circulação de informação” |
| Q2 · Graphs and stance | “weighted graph”, “graph-based semi-supervised learning”, “label propagation”, “stance detection”, “Gaussian fields harmonic functions” | “grafos ponderados”, “aprendizagem semissupervisionada”, “propagação de rótulos”, “detecção de posicionamento” |
| Q3 · Political discourse | “campaign discourse”, “political stance”, “rhetorical strategies”, “misinformation narratives” | “discurso eleitoral”, “apoio e ataque”, “estratégias discursivas”, “desinformação”, “eleições 2022” |
| Q4 · Verifiable explanations | “grounded generation”, “citation evaluation”, “faithfulness”, “evidence attribution” | “modelos de linguagem”, “explicabilidade”, “explicações com evidências”, “avaliação de citações” |
| Q5 · Expert validation | “construct validity”, “expert annotation”, “inter-annotator agreement”, “human evaluation” | “validade de construto”, “anotação por especialistas”, “concordância entre anotadores”, “avaliação humana” |

Use context modifiers such as `Brazil Twitter 2022 election` and `Brasil Twitter eleições presidenciais 2022` for local evidence. Run methods queries without the geographic modifier where the goal is to find a transferable method. Use a second terminology variant when results consistently retrieve a neighboring topic instead of the intended one.

### Evidence to record for each source

- Citation, stable link, version, question addressed, query or parent citation, and access or screening decision.
- Population, platform, country, language, dates, sampling and exclusions. For empirical papers, record the sample size if reported.
- What the study treats as an observation, what it infers, and how it turns the concept into a measure. For network studies, record nodes, edges, directions, weights and time windows. For annotation or model evaluations, record the unit, labels, evidence and procedures.
- Baselines, controls, validation data or independent judges, and whether the test reuses the signals that defined the result. Capture the main finding, effect sizes or agreement where reported, counterexamples and author-stated limitations.
- Implications for ITED-Br. Note the required fields, whether the evidence is directly relevant or transferable by analogy, and what would still need to be checked.

For each full search, log the date, source or index, exact query, filters, search depth, number screened and retained, and notable exclusions. For seed searches record whether the output was pooled, since a pooled result has no reliable per-query screening count.

## What the trial searches changed

On 2026-11-24, a combined scholarly web search emphasized Brazilian discourse studies. Several methods queries produced no distinct item in that shared output. Focused searches recovered the GFHF paper, a target-specific stance benchmark and a review of annotation agreement. This supports searching each strand separately. Searches about Brazilian interaction networks also returned campaign discourse, so inclusion under Q1 will depend on whether a paper actually measures interactions or circulation. The sources below are starting points for screening. The trial establishes retrieval and scope only.

| Starting source | Why it is in scope |
| --- | --- |
| [ITED-Br collection article](https://doi.org/10.1371/journal.pone.0316626) | Source for Step 2 to check collection design and documented coverage. |
| [Terren and Borge-Bravo, 2021](https://rcommunicationr.org/index.php/rcr/article/view/16) | Starting review of competing approaches to echo chambers and a source for citation tracing under Q1. |
| [Zhu, Ghahramani and Lafferty, 2003](https://mlanthology.org/icml/2003/zhu2003icml-semi/) | Original GFHF formulation for the prior graph-based stance baseline in Q2. |
| [Mohammad et al., 2016](https://aclanthology.org/S16-1003/) | Example of target-specific stance labels and evaluation for Q2 and Q3. |
| [Casadei and Ito, 2024](https://doi.org/10.22409/rmc.v18i1.58480) | Brazilian election case study on how voting fraud narratives claim credibility, relevant to Q3. |
| [Gao et al., 2023](https://aclanthology.org/2023.emnlp-main.398/) | Starts Q4 with a way to assess correctness and citation quality in generated text. |
| [Artstein and Poesio, 2008](https://aclanthology.org/J08-4004/) | Starting reference on measuring annotator agreement for Q5. |

### Trial search log

All rows use scholarly web search on 2026-11-24 with no date or domain filter. P1–P7 shared a single result batch. P8–P13 each requested up to three results, and P14 requested up to two. Screening counts and paper-to-paper citation tracing begin with the focused review.

| ID | Search | Exact query | Outcome |
| --- | --- | --- | --- |
| P1 | Combined | "The Interfaces Twitter Elections Dataset" 2022 Brazil data collection PLOS | Located the ITED-Br collection paper. |
| P2 | Combined | "echo chambers" political Twitter retweet network homophily diffusion Cinelli methodological review Terren Borge | Combined output did not surface a distinct result for this query. Reworked as P8 and P14. |
| P3 | Combined | "eleições 2022" Twitter "câmaras de eco" polarização rede retuítes desinformação Lula Bolsonaro | Combined output did not surface a distinct result for this query. Reworked as P9. |
| P4 | Combined | "learning from labeled and unlabeled data" "Gaussian fields" harmonic functions Zhu Ghahramani Lafferty label propagation graph stance Twitter | Combined output did not surface a distinct result for this query. Reworked as P10. |
| P5 | Combined | "eleições de 2022" Twitter Brasil desinformação taxonomia estratégias discursivas apoio ataque stance Portuguese eleições Lula Bolsonaro | Returned several Brazil 2022 discourse studies. P12 isolates this strand. |
| P6 | Combined | grounded explanations language model citations ALCE Gao generative search verifiability evaluation | Located Gao et al. on evaluating generated citations. |
| P7 | Combined | inter coder agreement computational linguistics Artstein Poesio political stance annotation independent human validation Portuguese | Combined output did not surface a distinct result for this query. Reworked as P11. |
| P8 | Standalone | political Twitter retweet networks homophily diffusion PNAS Cinelli echo chamber effect on social media Terren Borge Bravo review | Surfaced multiple copies of the same cross-platform echo-chamber study. Deduplicate by DOI and search reviews separately. |
| P9 | Standalone | Brasil Twitter eleições 2022 redes de retuítes polarização câmaras de eco eleições presidenciais difusão comunidades | Surfaced relevant election discourse studies. Add searches for interaction features such as redes de retuítes and circulação without insisting on câmaras de eco. |
| P10 | Standalone | Zhu Ghahramani Lafferty Gaussian fields harmonic functions learning from labeled unlabeled data ICML | Located the original GFHF paper by exact method name and author. |
| P11 | Standalone | Artstein Poesio inter-coder agreement computational linguistics ACL anthology | Located the annotation agreement survey. |
| P12 | Standalone | "eleições de 2022" Twitter Brasil discurso desinformação análise estratégias discursivas apoio ataque Lula Bolsonaro | Located context-specific qualitative work on discourse, including Casadei and Ito. |
| P13 | Standalone | stance detection Twitter SemEval target specific stance Mohammad 2016 ACL Anthology | Located a target-specific stance benchmark in English. Use as a methodological reference. |
| P14 | Standalone | Terren Borge-Bravo 2021 Echo Chambers on Social Media A Systematic Review of the Literature review communication | Located a review to seed the search for competing echo-chamber definitions. |

## Handoff to Step 2

Use Q1–Q5 to inventory what the dataset and the prior study actually provide. Which interaction and reference fields can be established from documentation? What is known about the text and link fields needed for Q3–Q4? Can the prior labels and their selection procedure be recovered for Q2? The earlier October 2022 slice is a candidate for continuity. The dataset inventory and later literature review will inform the window, graph choice, thresholds and eventual pilot design. [M1 roadmap and advisor report](m1-research-directions.md)
