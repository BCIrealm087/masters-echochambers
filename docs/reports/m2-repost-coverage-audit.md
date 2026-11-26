# Can we reconstruct dated reposts in the October runoff sample?

**M2 · Repost feasibility and coverage audit · Adopted 2026-11-26**

The first empirical milestone is to measure how many distinct repost actions in the Lula and Bolsonaro collection contexts on **16–21 October 2022**, using the São Paulo calendar, can be dated and linked to their original authors. The first result will be a coverage table by day and query, together with a decision about which comparisons those observations support. The six-day window falls within the prior article’s sample and spans the post-debate activity peak. It provides a bounded test of the method. [Research assessment](research-seed-assessment.md) · [ITED-Br feasibility protocol](reflexive-report-7.md)

## Research decisions

- **Computational contribution.** Test whether account groups learned from reposts add predictive information beyond familiar sharer–author ties, and quantify how sensitive that answer is to incomplete collection, unresolved authors and popular originals. A precise finding of little added value also answers the question. [Statistical protocol](reflexive-report-5.md)
- **Political follow-up.** For Lula and Bolsonaro separately, ask how widely candidate-directed criticism appears in members’ own writing and how much of its visibility comes from repeated sharing of a few originals. This comparison requires attributable Brazilian Portuguese text and independent coding. Text availability is a separate feasibility question. [Discourse protocol](reflexive-report-2.md)
- **Interpretation.** A supported structural result describes persistent internal amplification in the observed window. Political coherence requires independent stance evidence. Selective uptake requires a credible comparison with available alternatives. Attributable statements can establish expressed distrust. Private trust and belief change require separate measurements. [Conceptual criteria](reflexive-report-8.md)

## Run on the data host

The researcher will provide a dedicated, limited-permission SSH account on the Ubuntu machine holding the data. The first task after access is to inventory the available dataset version, schemas, query provenance and historical lookup sources. The earlier public Parquet inspection provides a comparison point. Fields and coverage on the host await direct verification. Read inputs in place and run the scripts and tests in the assigned user environment. Keep raw records, account identifiers and intermediate joins on the host. Keep connection details and credentials out of the research archive. Archive the analysis code, reproducible invocation, shareable input manifest and reviewed aggregates in Git. [Project data instructions](../../AGENTS.md#data-and-reproducibility)

1. **Identify the actions.** Verify how the source distinguishes a repost from a quote or reply and how it dates the repost itself. Check boundaries in `America/Sao_Paulo` against dated records. Retain source partition and collection context for records with uncertain action dates. They can document coverage even when their eligibility for the six days is unknown.
2. **Reconcile events and authors.** Deduplicate by action ID, preserving all query memberships. Record duplicate copies, missing IDs, and conflicting type, time, sharer or source information. Resolve each referenced original to its historical author using all relevant lookup records available on the host, including older originals. Expanding that lookup adds evidence about endpoints while the six-day action population stays fixed.
3. **Produce the table and verify the totals.** Report day by disjoint query membership (Lula only, Bolsonaro only, both), discovery and holdout subtotals, and the six-day union. Preserve unknown provenance and dates separately. Reconcile duplicate rows and overlapping queries before totaling. Label every rate with its denominator and every unavailable count with the reason.

| Coverage measure | What the output must distinguish |
| --- | --- |
| Input and deduplication | Candidate rows by source, rows without usable action IDs, distinct action IDs and duplicate copies |
| Type and date | Confirmed reposts, other interaction types and unknown or conflicting types. Among reposts, distinguish verified in-window dates, out-of-window dates and unresolved dates. |
| Edge eligibility | Among confirmed in-window reposts, count usable sharers and original-post references. Split lookup outcomes into uniquely identified historical author, original absent, author missing and conflicting authors. Report the final count with both endpoints. |
| Uneven recovery | Report recovery across events, distinct referenced posts and distinct sharers. Compare days and query memberships. Report documented acquisition gaps separately from failures to resolve recorded events. |

## Completion and handoff

M2 closes when the dated advisor report contains the reproducible invocation and input description, the reconciled coverage table (or documented limits on identifiable counts), and a reasoned decision to **proceed, narrow the eligible population, or stop the structural comparison**. Compare plausible differential loss with the precision needed for the intended estimate. An overall join percentage alone cannot settle that decision. [Missingness analysis](reflexive-report-7.md#measure-the-effect-of-missingness)

If coverage supports proceeding, the next analysis will learn groups on 16–18 October, freeze the choices, and evaluate them on 19–21 October against the day- and query-conditioned activity and original-post popularity reference, with a separate prior-tie comparison. M2 may inspect coverage in both windows. Keep held-out group-sharing outcomes unopened until the analysis rules are frozen. If dating or author resolution proves inadequate, report which narrower questions survive and the specific evidence needed to recover the intended comparison. [First-pilot design](m1-advisor-synthesis.md#proposed-first-pilot)
