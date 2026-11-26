# Can we reconstruct dated reposts in the October runoff sample?

**M2 · Repost feasibility and coverage audit · Adopted 2026-11-26**

The first empirical milestone is to measure how many distinct repost actions in the Lula and Bolsonaro collection contexts on **16–21 October 2022**, using the São Paulo calendar, can be dated and linked to their original authors. The first result will be a coverage table by day and query, together with a decision about which comparisons those observations support. The six-day window falls within the prior article’s sample and spans the post-debate activity peak. It provides a bounded test of the method. [Research assessment](research-seed-assessment.md) · [ITED-Br feasibility protocol](reflexive-report-7.md)

## Research decisions

- **Computational contribution.** Test whether account groups learned from reposts add predictive information beyond familiar sharer–author ties, and quantify how sensitive that answer is to incomplete collection, unresolved authors and popular originals. A precise finding of little added value also answers the question. [Statistical protocol](reflexive-report-5.md)
- **Political follow-up.** For Lula and Bolsonaro separately, ask how widely candidate-directed criticism appears in members’ own writing and how much of its visibility comes from repeated sharing of a few originals. This comparison requires attributable Brazilian Portuguese text and independent coding. Text availability is a separate feasibility question. [Discourse protocol](reflexive-report-2.md)
- **Interpretation.** A supported structural result describes persistent internal amplification in the observed window. Political coherence requires independent stance evidence. Selective uptake requires a credible comparison with available alternatives. Attributable statements can establish expressed distrust. Private trust and belief change require separate measurements. [Conceptual criteria](reflexive-report-8.md)

## Run on the data host

The data host is available. The [host inventory](#host-inventory-completed-2026-11-26) records the dataset snapshot, schemas, query provenance and historical lookup fields. Read inputs in place and keep raw records, identifiers and intermediate joins on the host. Archive the code, reproducible invocation, shareable input manifest and reviewed aggregates in Git. [Project data instructions](../../AGENTS.md#data-and-reproducibility)

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

## Host inventory completed 2026-11-26

Can the host archive identify repost actions, date them on the São Paulo calendar and recover their original authors? The host files contain explicit interaction labels, action timestamps and author identifiers. They provide a stronger starting point than the public Parquet samples examined in M1. Historical original-author recovery still needs to be measured. [M1 schema comparison](m1-ited-br-feasibility.md#what-was-verified)

### What was inspected

The input was the ITED-Br host snapshot at `/data/dados/twitter/corpus` on 2026-11-26. The inventory read every Parquet footer in the five dataset families. Tweet filenames span 20 July 2022 through 23 February 2023. File dates describe partitions. The row check projected five columns from the 16–21 October 2022 filename partitions in `query_lula`, `query_bolsonaro`, `retweets_query_lula` and `retweets_query_bolsonaro`. It counted copies as stored, including any duplication within or across contexts. It read no tweet text or user profile values.

| Evidence | Host representation | Use in the audit |
| --- | --- | --- |
| Interaction type | `tweets.type` is a string. Observed labels include `retweeted`, `quoted`, `replied_to`, `quoted, replied_to` and `tweeted`. `referenced_tweet_id` is a string that can contain comma-separated references. | Use the explicit `retweeted` label and check that the target is a single numeric post ID. |
| Action time | `tweets.created_at` is a string on the action row. The script compares it with the timestamp encoded in `tweets.id` at whole-second precision, then converts agreeing times to `America/Sao_Paulo`. | Select by the action's local date. Use partition dates to locate inputs and check for spillover. |
| Query membership | The immediate parent directory records collection context. The tweet schema has no separate query membership field. | Preserve every observed context when deduplicating by action ID. Folder membership establishes collection provenance. The original acquisition rules govern what that provenance says about keyword matches. |
| Original authorship | The repost row's `author_id` is the sharing account. Historical authorship is available through a candidate self-join from `referenced_tweet_id` to `tweets.id`, taking `author_id` from the matched target row. `users.account_id` keys account records. Profile quote and reply summaries contain `account_id`, `tweet_id`, `interaction_ids` and `interaction_authors`. | Search all historical tweet partitions for targets and distinguish absent targets, missing authors and conflicting authors. The inventory checks field availability and numeric IDs before measuring match coverage. |

### Aggregate counts

| Dataset family | Files | Stored rows | Empty files |
| --- | ---: | ---: | ---: |
| media | 4,050 | 30,673,896 | 815 |
| quotes | 780 | 6,456 | 208 |
| replies | 780 | 4,885 | 207 |
| tweets | 4,050 | 282,135,572 | 620 |
| users | 4,050 | 280,404,981 | 612 |
| Total | 13,710 | 593,225,790 | 2,462 |

The Parquet files total 43,786,109,554 bytes. The [aggregate inventory](m2-host-inventory.json) records all schema variants, folder counts and selected day-level diagnostics.

| Tweet collection context, 16–21 October file dates | Stored rows | Repost rows | Rows agreeing with ID time | Rows matching partition day in São Paulo | Rows dated within 16–21 October in São Paulo |
| --- | ---: | ---: | ---: | ---: | ---: |
| `query_bolsonaro` | 2,505,883 | 0 | 2,505,858 | 0 | 2,112,955 |
| `query_lula` | 2,305,045 | 0 | 2,305,033 | 0 | 2,020,565 |
| `retweets_query_bolsonaro` | 7,648,502 | 7,648,502 | 7,648,502 | 0 | 6,549,730 |
| `retweets_query_lula` | 5,547,017 | 5,547,017 | 5,547,017 | 0 | 5,024,871 |

Across the 24 selected files, 18,006,447 rows have usable post IDs and 18,006,447 have usable row author IDs. Of 13,195,519 repost rows, 13,195,519 carry a single numeric target reference. 18,006,447 timestamps parse and 0 carry an explicit UTC offset.

Of the 18,006,447 rows checked, 37 timestamps disagree with the UTC second encoded by the post ID, all in ordinary-query files. Every checked repost timestamp agrees. None of the checked timestamps maps to the São Paulo date in its filename. A separate check of the stored timestamps, interpreted as UTC, places 13,284,737 rows one local day before the file date and 4,662,467 two local days before it. The October 22 repost-query files also contain 1,586,888 rows timestamped on October 21 in São Paulo and 433,111 timestamped on October 20. The adjacent-file check uses timestamps alone. This shows why the full event audit needs to search beyond the six filename dates.

### How far the evidence reaches

The file inventory measures stored rows, including repeated copies, and the row check measures only the selected filename partitions. Neither supplies an acquisition-completeness denominator. The six-day local-time population requires a wider partition search and action-ID reconciliation. Candidate context records collection provenance. A repost records a sharing action. Claims about endorsement, exposure or trust require additional evidence.

### Reproduce the inventory

The deterministic script uses Python 3.10.12, PyArrow 25.0.1 and the system IANA time zone database (2026f). It applies no random sampling. The JSON includes a SHA-256 fingerprint over sorted relative paths, file sizes, footer row counts and schemas. The fingerprint identifies the inventory metadata and does not hash record contents.

```sh
mkdir -p runs/local
python3 -m pip install --target /tmp/m2-parquet pyarrow==25.0.1
PYTHONPATH=/tmp/m2-parquet python3 scripts/m2_host_inventory.py /data/dados/twitter/corpus > runs/local/m2-host-inventory.json
PYTHONPATH=/tmp/m2-parquet python3 scripts/m2_host_inventory.py --partition-offsets /data/dados/twitter/corpus > runs/local/m2-partition-offsets.json
```

### What follows

Search the candidate contexts across partitions for actions dated within the São Paulo window, deduplicate across files and preserve all observed memberships. Join the resulting repost targets to historical tweet rows across the corpus and report unique, missing and conflicting original authors by day and query. That coverage will inform the M2 decision on whether to proceed with the structural comparison.
