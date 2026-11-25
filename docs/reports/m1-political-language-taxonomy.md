# A draft taxonomy for political language in ITED-Br

**M1 · Step 5 · 2026-11-24**

How can the thesis compare the ways account groups supported or opposed political targets in Brazil’s 2022 election? The proposed unit for stance is a **post–target pair**, read in its original Brazilian Portuguese and attributed to the post’s author. A short section of text supports each rhetorical label. Each checkable claim gets its own evidence record. Reposting is recorded as an observed action, and coordination requires evidence across actions. This design allows a group comparison to distinguish how often members wrote a given kind of message from how widely they circulated it. [Step 4 methods](m1-graph-methods.md) · [Search and evidence notes](m1-q3-evidence.md)

## Rationale from the literature

- Furlani and Mitozo distinguish topics, communication strategies and orientation in their study of a candidate’s official campaign posts. Ferreira et al. study emotions and discourse in the most-reposted posts of two groups discussing the electoral system. The approaches suggest coding both the target of an evaluation and the way it is expressed. For this thesis, prominent posts answer a question about amplification. Estimating how typical a tactic is within an account group requires a broader sample. [Furlani and Mitozo](https://doi.org/10.26694/2317-3254.rcp.v12i2.6000) · [Ferreira et al.](https://doi.org/10.26694/2317-3254.rcp.v13i2.6933)
- Casadei and Ito examine how some 2022 election messages borrowed credibility through testimony, statistics or cues associated with journalism and expertise. These functions can occur in accurate and inaccurate messages. Record how a source is invoked and verify any factual assertion through separate evidence. Span-level persuasion work offers an annotation technique, with fresh decisions needed for short Portuguese posts and quoted material. [Casadei and Ito, 2024](https://doi.org/10.22409/rmc.v18i1.58480) · [Da San Martino et al., 2019](https://aclanthology.org/D19-1565/)
- Stance annotation concerns the evaluation of a particular target. Anger or humor may be directed at a different entity from the one named in the post. The draft combines target-specific stance with notes on how implicit language was interpreted. Brazilian Portuguese stance corpora provide design examples, with different topics, sampling and definitions. [Mohammad et al., 2016](https://aclanthology.org/S16-2021/) · [UstanceBR](https://doi.org/10.1007/s10579-025-09896-3)

## Coding unit, speaker and targets

Start with unique original posts and the added text of quotes and replies. Keep one record for each post and one stance record per identifiable political target in the author’s message. Record whether the post is original, a reply, a quote or a plain repost. Recover parent and quoted material when it is available and retain who said what. Plain reposts can inherit a link to the source post’s annotation for circulation analysis. The sharing account’s own stance remains undetermined unless separate authored evidence supports it. A quote with no added text is likewise an observed share without an authored stance.

Start the comparison with Lula and Bolsonaro as distinct targets. Permit a party or coalition, an electoral institution or process, a media outlet or other source, or a policy or political action where a post evaluates one directly. Keep the specific entity and its type. A comment about a policy, the Tribunal Superior Eleitoral (TSE) or a party only transfers to a candidate if the author actually connects that position to the candidate. Where an implicit reference is resolvable, note how. An unresolvable target takes an uncertainty code. Preserve text available versus context missing as coverage fields for all sampled posts.

### Stance toward a named target

| Label | Inclusion rule | Boundary |
| --- | --- | --- |
| **Favorable** (*favorável*) | The author endorses, defends, praises, or expresses a preference for the named target. | Code a comparative preference toward the favored target. Opposition to another target requires its own evidence. |
| **Opposed** (*contrário*) | The author rejects, criticizes, or expresses opposition to the named target. | Policy disagreement qualifies where the relevant target is actually opposed. Personal attack is a possible tactic within opposition. |
| **Mixed** (*misto*) | The author expresses both favorable and opposing evaluations of the same target in the same post. | Praise for one candidate and criticism of another get two separate stance records. |
| **No expressed stance** (*sem posicionamento expresso*) | The text mentions or discusses the target, and available context shows no evaluation by the author, such as an attributed factual update. | For material that cannot be interpreted without the missing parent, use unclear. For posts without any relevant target, record that at the post level. |
| **Unclear** (*indeterminado*) | The target or stance cannot be resolved because context is missing, plausible readings conflict, or a quotation has no discernible author response. | Where explicit evidence resolves sarcasm or an alias, code the inferred stance with its contextual support. |

Record the shortest span that supports each stance and tactic, or the available context required to interpret it. Preserve capitalization, accents, hashtags, emojis and quotation boundaries in the annotation view. Use normalization for search and grouping. Treat lists of aliases or campaign expressions as retrieval aids. The use of a slogan, nickname or hashtag by itself can reflect endorsement, quotation, criticism or irony. Analyze it with the author’s surrounding text and verified context. [Target-based stance methods](https://aclanthology.org/S16-2021/)

## Rhetorical tactics in the author's contribution

Apply zero or more codes to the shortest supporting spans. Keep subject matter, such as electoral administration, policy, or corruption, as an optional topic field. Apply the same rules to supporters and opponents and to institutional or media targets.

| Tactic | Include when | Exclude or flag when |
| --- | --- | --- |
| **Program or record advocacy** | The author promotes a policy, record, competence, or promised outcome to support a target. | A schedule announcement or an unendorsed quotation of a promise is reporting. Code a factual assertion about the record separately for verification. |
| **Substantive criticism** | The author disputes a specified policy, performance, decision or action and states a concrete reason or instance. | An insult or blanket dismissal without a specific issue is a different tactic. An allegation tied to a specific act may also need a claim record. |
| **Personal or categorical attack** | The author belittles a person or group through insult, derogatory labeling, or explicit ridicule of character or identity. | Critical evidence about an action alone is substantive criticism. Quoted abuse with a clear rejection belongs to the quoted speaker. |
| **Claim to authority or evidence** | The author presents an expert, institution, testimony, a document, statistic or graph to support a proposition. Record source type and whether it is named or identifiable. | Mentioning a source in passing is insufficient. The fact that it is invoked leaves its accuracy and actual reception open. |
| **Delegitimization of an institution or source** | The author explicitly urges dismissal or distrust of an institution, source or procedure as fundamentally unreliable or illegitimate. Record the target and exact basis. | A specific criticism of an error, or a request that evidence be checked, may be substantive criticism or a correction without blanket dismissal. |
| **Threat or urgency framing** | The author depicts a target, outcome or event as a concrete threat, or makes urgency central to a call to act. | Strong sentiment or routine scheduling alone is insufficient. If a claim about danger is checkable, record it at the claim level too. |
| **Mobilization or civic appeal** | The author directly urges an action such as voting, checking information, participating, or sharing. | A description of others’ actions without an appeal is reporting. |
| **Rebuttal or correction** | The author expressly challenges a claim, asks readers to disregard it, or supplies a correction. | A link with no interpretable position requires contextual evidence. Code the proposition being rebutted and the correction as separate claims where each is checkable. |

Mark sarcasm, parody, slogan form or ambiguity as **interpretation flags**. Clear humorous form can coexist with any tactic. Use an uncertain tactic flag when the reading depends on a missing image, video, thread or outside event. Keep topics and code definitions stable for both political groups. The categories are adapted to this thesis from Brazilian campaign research and persuasion annotation. A pilot can merge codes that reviewers repeatedly confuse or split a broad code when there is evidence that the distinction matters. [Furlani and Mitozo](https://doi.org/10.26694/2317-3254.rcp.v12i2.6000) · [Casadei and Ito](https://doi.org/10.22409/rmc.v18i1.58480) · [Da San Martino et al.](https://aclanthology.org/D19-1565/)

## Claim verification and behavior

### Claim records

Split distinct checkable propositions within each post and record the speaker, subject, time, place, scope, modality and negation. Record whether the author asserted, endorsed, questioned, refuted, or merely attributed the proposition. For a checkable assertion, assign one of these verification statuses.

| Status | Required evidence |
| --- | --- |
| **Supported** | A directly applicable record supports the proposition with its relevant qualifiers. |
| **Contradicted** | A directly applicable record contradicts the proposition with those qualifiers. |
| **Misleading in context** | Evidence supports some of what is stated or shown and establishes that missing or altered context materially changes the implication. Record both the literal assertion and the implication. Divide separable claims instead when they can be independently assessed. |
| **Unresolved after checking** | Relevant sources were reviewed, but conflict, missing evidence, uncertain attribution or a near-match prevents a conclusion. |
| **Unchecked** | No review has been performed for this specific proposition. |

When a post contains an opinion, value judgment or nonliteral expression without an empirical assertion, record that it contains no checkable claim of that kind. An uncertain assertion is distinct from opinion. A post can contain rhetorical language with no claim and another sentence with a checkable claim.

For verification, retrieve candidate matches using the TSE’s 2022 *Fato ou Boato* archive, original records relevant to the proposition, and independently documented Brazilian fact-checks. Confirm that the match concerns the same subject, event, scope and version. Record the URL, source date, claim date, verdict and rationale. A shared topic, name or similar phrasing is insufficient for a match. Keep the archive’s original verdict as provenance and record the reason for the project’s mapping. For a quote that refutes a contradicted claim, preserve the contradiction in the claim record and count the quoting post as a rebuttal. Coverage of previously checked claims is selective. Report unmatched claims and how verification work was sampled. [TSE 2022 archive](https://www.justicaeleitoral.jus.br/fato-ou-boato/checagens/2022) · [Hale et al., 2024](https://doi.org/10.1093/ijpor/edae032) · [Shaar et al., 2020](https://aclanthology.org/2020.acl-main.332/)

### Behavioral evidence

Record reuse, shared sources, or temporal concentration as observations when independently supported by event data. A later coordination analysis would need multiple accounts, time or behavioral traces of adequate granularity, and a comparison that accounts for activity, source popularity and common election events. Deduplicate the same event and distinguish ordinary reposts from independent authored posts. Describe an excess pattern as **consistent with coordination** while other explanations remain viable. Claims of deception, inauthenticity or deliberate disinformation require separate evidence about attribution, fabrication, control or intent. A false proposition, a slogan, a dense cluster or a repeated link is insufficient evidence for those claims. Keep individual and sequence-level material in protected research storage. [Pacheco et al., 2021](https://doi.org/10.1609/icwsm.v15i1.18075) · [Wardle and Derakhshan, 2017](https://edoc.coe.int/en/media/7495-information-disorder-toward-an-interdisciplinary-framework-for-research-and-policy-making.html) · [ITED-Br feasibility](m1-ited-br-feasibility.md)

## Worked examples in Brazilian Portuguese

The following examples are fictional. Bracketed context is supplied solely to illustrate coding decisions.

| Text or event | What to record |
| --- | --- |
| “Apoio o plano de transporte da candidata A. A proposta do candidato B deixa o bairro sem linha à noite.” | Favorable to A and opposed to B, with program advocacy and substantive criticism respectively. The assertion about B’s plan is a separate checkable claim, unchecked in this example. |
| “A candidata A acertou no transporte, mas errou ao cortar o atendimento noturno.” | Mixed toward A. Program or record advocacy and substantive criticism can coexist. The asserted change in service has its own claim record. |
| “A candidata A anunciou a agenda de amanhã, segundo a assessoria.” | No expressed stance toward A. Record reporting and attribution. A source reference that merely identifies where the announcement came from is insufficient by itself for the tactic of invoking authority as support for an argument. |
| “Nossa, que genial esse plano 🙃” [parent unavailable] | Mark irony or ambiguity and leave stance unclear. If the available parent and the author’s words resolve the target and direction, attach that context as evidence when coding. |
| “Esse vídeo está cortado. No trecho completo, a fala era sobre outro bairro.” [quotes a post attacking A] | Record a rebuttal by the quoting author and keep the quoted attack with its speaker. The assertion about the clip is checkable. A verdict depends on retrieving the relevant original material. |
| “O relatório prova que fecharam cinco postos.” [only a shortened year-end excerpt is available] | Record a claim to evidence and a checkable proposition. Keep the verdict unresolved if the reviewed record refers to a different period or the full source is missing. |
| Plain repost of the first example | Count an amplification event for the source. The source’s two stance records can describe what was shared. The sharer’s own stance is undetermined by this event. |

## Comparing group frequencies

1. **Fix the groups and the sampling frame first.** Use the assignments from the account graph without recalculating them from tactic labels. Define the same event dates and eligible language criteria for all compared groups. Use a probability sample of eligible posts stratified by group, day and post type as needed. A separate sample of highly reposted content answers the amplification question. If rare categories need additional examples for codebook development, set them aside from prevalence estimates or retain their inclusion probabilities.
2. **Use denominators that match the question.** For a tactic, report the weighted share of eligible, codable authored posts containing it, each tactic counted at most once per post. For stance toward a candidate, use the eligible codable post–target pairs for that candidate. Show counts for no target, unclear, missing context and unassigned accounts alongside the rates. For amplification, report the share of codable distinct source posts carrying the tactic and the share of codable repost actions linked to a source carrying it, each within the sharing group. For verified claims, report the verified denominator, the unchecked or unresolved share and how claims were selected. Comparing verdicts among checked assertions describes that checked sample. Multi-label tactic rates can sum to more than 100%.
3. **Account for activity and unequal coverage.** Show a post-weighted rate and an account-weighted view that averages each eligible account’s own rate, with low-activity coverage reported. Compare like periods, post types and targets. Where the groups overlap, standardize to a shared day and post-type distribution, using sampling weights and uncertainty intervals that keep posts from the same account together. For amplification, check whether a few source posts dominate and assess uncertainty with repeated source posts taken into account. Mark cells with little overlap or missing text or parents, and report how the comparison changes on a common covered subset. Limit inferences to the observed sampling frame and the scope of the available annotation.
4. **Review the codebook where judgment matters.** Start with a bounded excerpt sample containing clear cases, adjacent categories and borderline implicit language. Use assisted retrieval and suggested annotations to reduce routine work. For the later reference set, have independent reviewers judge ambiguity, attribution and contested claim matches where credible validation requires it. Check agreement per code and class, and preserve adjudication reasons. Step 7 will define the expert review protocol. [Prior research on annotator agreement](https://aclanthology.org/J08-4004/) · [Step 3 group outputs](m1-echo-chamber-detection.md#outputs-for-membership-and-circulation)

## Handoff to Step 6

Carry forward the target, speaker, evidence span, claim status and denominator as the minimum evidence for a group-language statement. An explanation can describe what was measured, what text or aggregates support an inference, and where coverage limits it. The taxonomy needs approved Brazilian Portuguese text and enough quote or reply context to apply the author-level rules. The public ITED-Br samples supply structural linkage fields. This draft defines what the text work would measure when those additional fields can be established. [ITED-Br feasibility](m1-ited-br-feasibility.md) · [M1 roadmap](m1-research-directions.md)
