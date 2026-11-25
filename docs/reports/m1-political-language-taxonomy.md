# A draft taxonomy for political language in ITED-Br

**M1 · Step 5 · 2026-11-24 · Revised by [Reflexive report 2](reflexive-report-2.md) on 2026-11-25**

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

Record speaker role, target surface form and normalized identity, explicit or inferred target/stance, coder confidence and the reason for uncertainty. Retain alternative readings when context admits more than one. Record the shortest span that supports each stance and tactic, or the available context required to interpret it. Preserve capitalization, accents, hashtags, emojis and quotation boundaries in the annotation view. Use normalization for search and grouping. Treat lists of aliases or campaign expressions as retrieval aids. The use of a slogan, nickname or hashtag by itself can reflect endorsement, quotation, criticism or irony. Analyze it with the author’s surrounding text and verified context. [Target-based stance methods](https://aclanthology.org/S16-2021/)

## Rhetorical tactics in the author's contribution

Code the authored contribution in two passes. Identify its function, then mark the spans that express each rhetorical mechanism. Several functions and mechanisms can coexist. Record topic separately so an electoral-administration discussion can be compared with another on the same subject.

| Communicative function | Inclusion and boundary |
| --- | --- |
| Praise or acclaim | The speaker celebrates or endorses the target. Attribute praise reported in a quotation to its speaker. |
| Substantive advocacy | The speaker defends a concrete policy, achievement or proposal. General admiration is praise. |
| Substantive criticism | The speaker challenges a specified action, decision or record. Record any factual allegation separately. |
| Character or competence attack | The speaker challenges honesty, fitness or ability. A specific policy objection can coexist with an attack if each has support. |
| Defense or rebuttal | The speaker contests an identifiable accusation or argument. Keep the initial accusation attached to its speaker. |
| Explicit correction | The speaker identifies a factual error and offers or requests correction. Any replacement proposition receives its own verification record. |
| Mobilization | The speaker asks others to vote, share, verify or participate. Record the requested behavior. A description of a rally alone is reporting. |
| Information or reporting | The speaker reports an event or attribution. An author can add an evaluation elsewhere in the same post. |

| Mechanism family | Distinctions to pilot using the shortest supporting span |
| --- | --- |
| Attack and legitimacy | Separate insult/ridicule, hostility aimed at a defined protected or vulnerable identity, rejection of institutional or procedural legitimacy, and an appeal to dismiss a source as inherently untrustworthy. A question about one TSE decision does not by itself justify the broader codes. |
| Argument and framing | Identify authority/evidence appeals, explicit comparisons, moral or religious evaluation, collective identity, and people-versus-elite framing. For authority, record the source invoked and what claim it is used to support. A mere attribution can be reporting. |
| Emotion and urgency | Code the expressed emotion or the appeal to an audience, and record explicit threats or urgency. Record textual evidence before assigning anger, fear, hope or pride. Detailed emotion subtypes are optional. |
| Pragmatic form | Separate observable humor, satire or parody from irony that reverses a literal reading. Record insinuation or strategic questioning without turning an implication into an asserted fact. Keep ambiguous readings and missing media visible even when humor is evident. |

For example, *Faz o L* and *Mito* can be praise, mockery or quotation. *O TSE errou nessa decisão* identifies a particular decision as mistaken. *Compartilhem até chegar em todo mundo!* is a request to share. These constructed examples test boundaries across speakers and groups. When the same phrase supports several readings, retain the evidence and uncertainty. Pilot the compact functions first. Add fine-grained mechanisms to quantitative comparisons only when independent readers and held-out measurements support them. [Reflexive report 2](reflexive-report-2.md) · [Q3 evidence](m1-q3-evidence.md)

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

Freeze community membership before inspecting language and audit permitted text recovery by group, query, day, post type and source. The four primary comparisons weight authored posts, individual authors, distinct amplified originals and repost events. Keep unresolved counts, design weights and target-specific stance denominators alongside the estimates. Use representative samples for prevalence and a separate challenge set for ambiguous or rare cases. Report raw and standardized contrasts, source concentration and uncertainty from repeated actors, shared originals and classification error. The [group-comparison specification](reflexive-report-2.md#4-compare-groups-using-four-explicit-denominators) defines each calculation and its interpretation. The [annotation and model benchmark](reflexive-report-2.md#3-establish-an-independent-reference-before-automating) sets out the reliability decisions before scaling.

## Handoff to Step 6

Carry forward the target, speaker, evidence span, claim status and denominator as the minimum evidence for a group-language statement. An explanation can describe what was measured, what text or aggregates support an inference, and where coverage limits it. The taxonomy needs approved Brazilian Portuguese text and enough quote or reply context to apply the author-level rules. The public ITED-Br samples supply structural linkage fields. This draft defines what the text work would measure when those additional fields can be established. [ITED-Br feasibility](m1-ited-br-feasibility.md) · [M1 roadmap](m1-research-directions.md)
