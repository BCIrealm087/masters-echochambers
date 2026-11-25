# Expert validation protocol for the echo-chambers pilot

**M1 · Step 7 · 2026-11-24**

Which conclusions about Brazil's 2022 Twitter communities would survive independent scrutiny by political scientists? The proposed review tests three things on a small, deliberately varied set of cases. Do the evidence and election context warrant the group interpretation? Can reviewers apply the stance and tactics taxonomy consistently? Do the explanations help reviewers recover the evidence without overstating it? The protocol uses two independent reviewers where context or interpretation matters. The research workflow prepares the materials and checks the measurable parts first. This is a design for a later pilot. [Reflexive report 1](reflexive-report-1.md) revises the explanation comparison, sampling and workload assumptions. [Step 3 group criteria](m1-echo-chamber-detection.md) · [Step 5 taxonomy](m1-political-language-taxonomy.md) · [Step 6 explanation rubric](m1-llm-group-explanations.md) · [Search and evidence notes](m1-q5-evidence.md)

## Which judgments require review

| Question | Establish automatically where possible | Ask political science reviewers to judge |
| --- | --- | --- |
| **Group interpretation** | Reproduce the discovery and holdout splits, fixed membership, event joins, within- and across-group counts, activity-preserving reference results, and missing-endpoint bounds. Flag when group conclusions change with a query, event day or large account. | Whether the documented results warrant the proposed interpretation in the 2022 context. Consider alternative explanations such as an episode of news sharing, a candidate-profile audience or a single event attracting concentrated activity. A political echo-chamber interpretation also requires genuinely independent evidence of stance or content selectivity. |
| **Language coding** | Preserve speaker roles, quote boundaries and completeness flags. Find eligible text, suggest candidate targets if useful, and deduplicate the sample. Track reason codes and review time. | Whether the author's words convey support, opposition, ambiguity, rebuttal or another tactic for the specified target. Check local nicknames, sarcasm and whether missing context makes the case undecidable. Review claim matching only where factual status is material to the argument. |
| **Explanation accuracy and usefulness** | Verify evidence IDs, dates, denominators, sums, directions and whether required evidence items are present in all three formats. Flag unsupported numerical values before review. | Whether each substantive claim is warranted by its cited evidence, whether linguistic and electoral qualifications matter to the conclusion, and whether the reader can find the evidence quickly enough to assess it. |

Political scientists adjudicate the interpretation and quality of the evidence. A split, rate or model parameter remains a computational result. Actual feed exposure, private beliefs, causal influence, and intentional coordination require evidence beyond a structural result or expert agreement. Validation tests whether a measure is adequate for the specific claim and domain. [Grimmer and Stewart, 2013](https://doi.org/10.1093/pan/mps028) · [Rashkin et al., 2023](https://aclanthology.org/2023.cl-4.2/)

## Select cases before seeing the reviews

Use two reviewers familiar with Brazilian political communication and the 2022 election, reading the same Portuguese materials. Where possible, select reviewers who did not fit the models or select the cases. Record prior involvement and preserve their separate forms. The case mix below is a proposed time budget for diagnosing failures and category boundaries. Later estimates of prevalence or model accuracy require a separate study sample. [Palinkas et al., 2015](https://doi.org/10.1007/s10488-013-0528-y)

| Material | Proposed sample | How to select it |
| --- | ---: | --- |
| Group cards | **4** | Choose two clear cases from apparently different group profiles when available, with stable membership and usable held-out evidence. Include a near miss whose internal clustering is strong during discovery but weaker in holdout or sensitivity checks. Include a sparse or coverage-limited case. Use a news-centered or event-centered group where relevant. Unless independent content evidence is available, a clear case is clear only for the structural result. |
| Portuguese post–target cases | **16** | Use four clear anchors across favorable and opposed stance, six boundary cases such as policy criticism versus personal attack, four quotation or correction cases, and two missing-context cases. Include both candidates and institutional targets where available. In the verification cases, include an exact fact-check match and a similar but materially different claim. Spread the sample across days, group assignments and activity levels. Keep the reference verdict evidence in the packet and retain the speaker’s original wording within approved access. |
| Explanation comparisons | **4 feasibility cases** | Include a clear group, a near miss, a graph-only or missing-context case, and a case where structure and language provide different indications. Use a separate set of evidence packets from the group-card exercise when possible. Produce a table, deterministic Portuguese prose and LLM prose from identical evidence and required topics. Freeze inputs before reviewing outputs. |

Freeze the holdout criterion, reference model and adequacy rules for coverage before assigning cases to the sample. Select from the audited data, distinguishing cases that pass the coverage rule from the coverage-limited controls. Save the eligible case pool, strata, exclusion reasons, selection seed where applicable, and which tests are unavailable. Use synthetic items for calibration or to test whether the form catches known errors. Score those separately from corpus cases. A near miss is a case chosen to probe a decision boundary. Reviewers receive evidence and a neutral case identifier without the expected class. A bounded review with fewer available cases can still diagnose issues if the unavailable strata are recorded. If approved text is unavailable, use the structural review where possible and mark discourse and political-alignment evaluations as pending.

## Prepare the materials

1. **Group card.** Include the discovery interval and graph relation, the holdout interval, eligible and resolved event counts, what an arc represents, observed and expected within-group shares, stability and sensitivity summaries, independent content evidence if available, and a short note on query coverage and the corresponding 2022 event. Show unresolved outcomes and explicit limits. Use a neutral group identifier. Keep the partition method name hidden at first when it is unnecessary for judging what the evidence supports. Retain the method and exact specification for audit after responses are locked.
2. **Text annotation card.** Show the author's original Portuguese contribution, item date, focal target, post type and documented context with speaker roles clear. For quoted or fact-check material, show the parent text or the missing-context flag and relevant source records. Mask surnames or handles where they identify an account and are unnecessary for interpretation. Preserve names of political targets and other context essential to the reading. Hide group ideology labels, predicted tactic labels and other reviewers' choices.
3. **Explanation review packet.** Give the underlying evidence with stable IDs, required information and the assigned first-pass artifact. Balance format and order across reviewers. Record the reader’s answer, supporting evidence, confidence and verification time before showing another version. Collect method guesses and any later preference separately. [van der Lee et al., 2019](https://aclanthology.org/W19-8643/) · [Belz et al., 2020](https://aclanthology.org/2020.inlg-1.24/)

Keep Twitter text, account identifiers and individual review records in protected project storage. The GitHub record can contain the protocol, identifiers that do not expose accounts, aggregate judgments, permitted examples, and the decision log.

### Calibration items

Use a few fictional items with documented answers before the independent pass. Discuss what the task measures and what counts as evidence. Keep them out of corpus agreement and pilot performance summaries.

| Calibration case | Expected boundary |
| --- | --- |
| A candidate group has many within-group reposts during discovery. Its held-out rate is 45% where the activity-preserving reference expects 46%, with adequate coverage. | A reproducible partition can still lack evidence of held-out selective sharing. With well-resolved events, this is a case that weakens the interpretation. |
| A post quotes *“O plano de A foi um desastre”* and adds *“Não concordo com essa crítica.”* | Attribute the criticism to the quoted speaker. The author rejects the criticism. Their general stance toward A remains unclear without further evidence. |
| The [fictional Step 6 group](m1-llm-group-explanations.md#worked-example-with-a-fictional-group) has 72 internal reposts among 100 resolved, 120 observed total. An output says 72% of all observed posts were internal. | The cited evidence uses a different denominator. This is a material scope error for the explanation rubric. |

After calibration, freeze the reviewed material version, codebook and scoring rules. Work through the text annotations, then group cards, then explanations. With two reviewers and four feasibility cases, rotate first-pass formats across cases, assigning different versions of each case to each reviewer. Report the resulting incomplete coverage by condition. For each case, reviewers submit their own classification and short rationale before seeing model identity, other judgments or any consensus label. If an explanation case reuses previously seen evidence, record that fact. Use first-presentation timing and comprehension tasks only for fresh cases, count per format, and treat the numbers as exploratory. Separate the later preference question from these first-presentation measures.

## Formulário resumido em português brasileiro

O formulário pode ser preenchido com referências aos itens do dossiê e trechos curtos permitidos. Para cada decisão, registre uma justificativa breve e indique qual informação, se ausente, poderia mudar a resposta.

| Bloco | Perguntas e respostas |
| --- | --- |
| **Grupo** | Na janela de validação, os dados sustentam a interpretação de circulação seletiva dentro do grupo? Marque **sustentada nas republicações observadas**, **sensível à especificação**, **enfraquecida pelo teste** ou **evidência insuficiente**. Cite um resultado e uma ressalva. Há evidência independente de seletividade política? Marque **sustentada**, **parcial**, **enfraquecida** ou **não avaliável** e aponte sua fonte. Indique uma explicação alternativa plausível, se houver. |
| **Publicação** | Identifique o alvo e o falante. Classifique o posicionamento e as táticas usando o [livro de códigos](m1-political-language-taxonomy.md). Sublinhe o trecho decisivo ou aponte a referência contextual. Se houver uma alegação factual, registre se o autor a afirma, questiona, rebate ou atribui a outra pessoa. Na checagem proposta, a fonte trata da mesma alegação, com o mesmo alcance, data e contexto? Se faltar material decisivo, marque **indeterminado** e indique o que falta. |
| **Explicação** | Para cada afirmação relevante, marque **sustentada**, **parcialmente sustentada**, **contradita** ou **não verificável com o dossiê**. Cite a evidência ou a lacuna. Indique erros graves de autoria, grupo, direção, denominador, checagem, intenção ou exposição, se houver. Responda às perguntas de compreensão e avalie a clareza do português de 0 a 2 conforme a [rubrica](m1-llm-group-explanations.md#evaluation-rubric-for-a-later-pilot). Registre sua confiança e o tempo de verificação antes de ver outra versão. Se comparar versões depois, indique sua preferência e o motivo. |

Use **sustentada nas republicações observadas** when the held-out evidence meets the operational criterion for the observed sample and the required coverage checks. Use **sensível à especificação** when comparable checks give different answers. Use **enfraquecida pelo teste** when informative data indicate a failure to exceed the reference or supply conflicting evidence on the claimed behavior. Use **evidência insuficiente** when missing endpoints, unavailable context or sparse data prevent a meaningful decision. These judgments have different implications. Only independent stance or content evidence supports the separate qualifier about political selectivity.

## Record agreement and turn disagreement into decisions

- Store both initial forms, the rubric version, case order, review time and cited evidence. For the group cards and explanation cases, report outcomes and disagreements case by case. For stance, report a count of matched labels, the total for which both provided a judgment, and the confusion table. For each tactic, report both-positive, one-positive and both-negative counts, plus the number of unavailable judgments. A rare tactic can look highly reliable if almost all agreement is negative. Treat **indeterminate** as a substantive response. A form skipped entirely is missing. If a later sample has enough independently rated items and variation, add an appropriate chance-adjusted measure and report its sample and category counts. [Artstein and Poesio, 2008](https://aclanthology.org/J08-4004/) · [Feinstein and Cicchetti, 1990](https://pubmed.ncbi.nlm.nih.gov/2348207/)
- Compare rationales after the initial forms are locked. For each consequential disagreement record the conflicting choices, evidence used, cause, whether it was resolved, and what changes. See the decision table. Preserve plausible alternative interpretations and use unresolved labels where context or evidence cannot settle them. Keep any adjudicated record alongside the independent forms. [Oortwijn et al., 2021](https://aclanthology.org/2021.humeval-1.15/) · [Mostafazadeh Davani et al., 2022](https://aclanthology.org/2022.tacl-1.6/)

| What caused the disagreement | How it changes the research |
| --- | --- |
| A data, attribution or denominator error | Correct the underlying analysis or evidence packet and check affected cases again. Preserve the first result under its original version. |
| A code boundary or insufficient context | Tighten the definition, add a scope example or record a missing-context state. Check a fresh small set after changing the codebook. |
| A plausible alternative group interpretation | Narrow the claim, preserve the alternatives, or identify what additional source or measure could discriminate between them. Record disagreement as a finding about these cases and reviewers. |
| An explanation introduces an unsupported claim or hides a limit | Flag the error, keep the verified structured summary for that case, and review the revised explanation on held-out materials before using it in the advisor report. |

A third reviewer is useful only for a decision-sensitive disagreement where the available record could resolve it. Ask for the contested judgment with its evidence, without the prior outcomes. Keep both existing responses and the third review. A discussion can clarify code definitions and document differing readings. It cannot supply an unobserved event, a missing quotation or an independent measure of belief.

## Workload and stopping point

The table records the original M1 two-format feasibility budget. Use measured timings and actual case-by-format assignments to budget the revised three-format review.

| Work per reviewer | Estimated minutes |
| --- | ---: |
| Orientation and calibration | 22 |
| Four group cards at 4 minutes each | 16 |
| Sixteen post–target cases at 2 minutes each | 32 |
| Four paired explanation cases at 6 minutes each | 24 |
| **Total for independent review** | **94** |
| Targeted discussion if needed | Up to 25 |

That is about **1 hour 35 minutes per reviewer** independently, or **about 3 hours 10 minutes of reviewer time** for two reviewers. With a 25-minute discussion for both, the total is about four reviewer-hours. Allow a separate short slot of 15–30 minutes for a third reviewer only if a specific case requires it. The time assumptions are planning choices. Record actual time and reduce low-priority items if the cases take longer, preserving the contrasting and missing-evidence examples. Split the tasks into two sessions if needed.

For the later pilot, archive the evidence inventory, aggregate ratings, paired comprehension results where available, disagreements, codebook or method revisions, and which decisions need more data. Record the scope of every conclusion. If a reviewer is unavailable, continue computational and material validation and leave claims that require domain judgment open. Expert feedback will enter after there are cases to review. [M1 roadmap](m1-research-directions.md)
