# Can we reconstruct dated reposts in the October runoff sample?

**M2 · Repost feasibility and coverage audit · Completed 2026-11-26**

How many distinct reposts in the Lula and Bolsonaro collection contexts on **16–21 October 2022** can be dated on the São Paulo calendar and linked to their original authors? The audit verified **11,988,989 distinct reposts** and recovered both accounts for **11,960,224 (99.760%)**. Proceed with the planned within-corpus chronological pilot. Keep missing endpoints in sensitivity analyses and preserve the two discovery and holdout intervals. The six-day window falls within the prior article’s sample and spans the post-debate activity peak. It provides a bounded test of the method. [Research assessment](research-seed-assessment.md) · [ITED-Br feasibility protocol](reflexive-report-7.md)

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

## Registered completion criteria

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

The reconciliation below implements the full-partition search, deduplication and historical join defined at the inventory handoff.

## Full action and historical-author reconciliation

### What did we do, and why?

The unit is a distinct action ID. The audit searches every available partition in the four Lula and Bolsonaro candidate contexts. A combined search on the stored action timestamp and the time encoded in the action ID seeds a candidate if either places it in the local window. The second pass retrieves all copies of seeded IDs, including copies from other partitions. This lets records outside the initial date filter expose conflicting evidence or add a collection membership. Rows without IDs remain in the input counts. Rows whose timestamp and ID supply no date cannot be assigned to the window.

The action clock is verified when the usable stored timestamps support one instant and it matches the whole UTC second encoded in the ID. The São Paulo offset was UTC−03:00 throughout the analysis window. Reposts require an explicit `retweeted` label and no competing nonmissing type label. Missing values in one copy are reported separately from disagreements among usable values. Usable sharers and references require a single positive numeric identifier in the reconciled copies. The two ordinary-query folders help corroborate type and provenance alongside the two repost-query folders. They share the corpus acquisition pipeline, so the agreement is a consistency check. A separate historical validation sample would be needed to estimate classification accuracy.

All 4,050 tweet files across the 20 host contexts are eligible for the post-to-author lookup. The join uses exact post IDs and counts distinct usable historical author IDs across matching rows. Conflicting authors and targets recorded as repost actions have their own exclusions. Lookup uses older and later partitions to recover historical identity. The six-day action population and its discovery/holdout split are fixed before this join. No text, profiles or present-day API records enter the calculation.

### What did we learn?

Across 753 files in the four candidate contexts, the audit scanned 224,097,425 stored rows. The date search retained 19,026,364 copies representing 16,325,094 distinct actions. The four source counts in the window were 2,441,210 from `query_lula`, 2,636,553 from `query_bolsonaro`, 5,880,014 from `retweets_query_lula` and 8,068,587 from `retweets_query_bolsonaro`. The other 205,071,061 scanned rows fall outside the candidate population, including 137,811,095 verified out-of-window repost rows. These outside-window counts describe stored copies.

There were 2,701,270 duplicate copies. The distinct actions comprise 11,988,989 reposts, 2,661,101 replies, 1,212,430 standalone tweets, 427,836 quotes, 34,686 combined quote/replies and 52 actions with conflicting type labels. No seeded ID had unresolved or out-of-window dates, unknown provenance, conflicting timestamps, conflicting sharers or conflicting repost references. The four-context scan found zero missing action IDs and zero rows whose two clocks were both unavailable.

Across all scanned dates, every repost-query row carries the `retweeted` label and no ordinary-query row carries that label. The 13,948,601 in-window repost copies yielded 11,988,989 actions. Each of the 1,959,612 actions observed in both candidate contexts supplied one duplicate copy. An independent PyArrow scan recovered the same raw repost row totals by source partition using stored timestamps. The in-window repost rows span filename dates October 17–23. The 354,001 copies stored under October 23 all record actions on October 21.

All 11,988,989 verified reposts have a usable sharer and one reference. Of the 28,765 unresolved actions, 28,762 reference posts absent from the tweet lookup, and three reference posts with no usable author. No references yielded conflicting authors or pointed to a target recorded as a repost. A lookup miss describes the archive's coverage. It supplies no evidence about why the source is absent.

**Table 1.** Reposts with both accounts identified / verified distinct reposts, with percentages. Query membership columns are disjoint. The union counts each action once.

| São Paulo date or interval | Lula only | Bolsonaro only | Both | All |
| --- | ---: | ---: | ---: | ---: |
| Oct 16 | 856,869 / 862,511 (99.346%) | 1,717,140 / 1,722,396 (99.695%) | 625,639 / 627,313 (99.733%) | 3,199,648 / 3,212,220 (99.609%) |
| Oct 17 | 621,814 / 624,263 (99.608%) | 917,368 / 920,853 (99.622%) | 394,268 / 394,523 (99.935%) | 1,933,450 / 1,939,639 (99.681%) |
| Oct 18 | 624,406 / 626,467 (99.671%) | 776,782 / 778,115 (99.829%) | 243,926 / 244,235 (99.873%) | 1,645,114 / 1,648,817 (99.775%) |
| Oct 19 | 748,604 / 749,393 (99.895%) | 683,747 / 684,806 (99.845%) | 242,615 / 242,688 (99.970%) | 1,674,966 / 1,676,887 (99.885%) |
| Oct 20 | 571,538 / 572,241 (99.877%) | 1,001,953 / 1,002,865 (99.909%) | 222,956 / 223,142 (99.917%) | 1,796,447 / 1,798,248 (99.900%) |
| Oct 21 | 484,356 / 485,527 (99.759%) | 998,627 / 999,940 (99.869%) | 227,616 / 227,711 (99.958%) | 1,710,599 / 1,713,178 (99.849%) |
| Discovery · Oct 16–18 | 2,103,089 / 2,113,241 (99.520%) | 3,411,290 / 3,421,364 (99.706%) | 1,263,833 / 1,266,071 (99.823%) | 6,778,212 / 6,800,676 (99.670%) |
| Holdout · Oct 19–21 | 1,804,498 / 1,807,161 (99.853%) | 2,684,327 / 2,687,611 (99.878%) | 693,187 / 693,541 (99.949%) | 5,182,012 / 5,188,313 (99.879%) |
| Six-day union | 3,907,587 / 3,920,402 (99.673%) | 6,095,617 / 6,108,975 (99.781%) | 1,957,020 / 1,959,612 (99.868%) | 11,960,224 / 11,988,989 (99.760%) |

The join recovered authors for 379,655 of 385,868 distinct referenced posts (98.390%). Among 838,438 distinct sharers, 836,351 (99.751%) had at least one resolved repost. Recovery was consistently lower for targets shared just once across the six days. Discovery and holdout recovered 97.971% and 97.656% of actions referencing these targets, compared with 99.765% and 99.990% for targets referenced at least 100 times. This difference matters for analyses that give each post equal weight. The [aggregate output](m2-repost-coverage.json) supplies the counts for each day, query membership, target-reuse band and sharer-activity band, including the separate failure categories. The denominator for distinct historical author coverage is unknown because the missing posts do not reveal how many authors are absent.

### How far does the evidence reach?

Unresolved authors account for 0.330% of recorded discovery actions and 0.121% of recorded holdout actions. In any fixed population of verified actions, allocating all unresolved authors first outside and then inside the sharer's group yields a raw internal-share interval whose width equals the unresolved fraction. Using the whole holdout ledger as the denominator, that width is 0.121 percentage points. Its largest day-by-query width is 0.241 points in the holdout and 0.654 points across all six days. These are small relative to the provisional +5-point practical screen. The relevant denominator for the pilot will be actions from sharers assigned to frozen groups. Calculate its bounds after assignment and recompute the expected share under the same missing-endpoint scenarios. Discovery partitions can also change if missing edges cluster around a few accounts. [Statistical decision rules](reflexive-report-5.md#decision-rules-power-and-uncertainty)

Observed counts cover the two acquisition contexts. The collection's documented API limits, query changes and later cutoff do not supply a completeness denominator for the six October days. The audit reconciles recorded actions and measures endpoint recovery conditional on collection. It measures neither uncollected reposts nor any party's overall reach. Folder membership is collection provenance. A repost documents sharing. Political alignment, endorsement, exposure and trust each require additional evidence. [Collection and acquisition limits](reflexive-report-7.md#what-the-evidence-establishes)

### Decision and handoff · 2026-11-26

**Proceed with the six-day pilot for observed actions.** Both windows retain millions of resolved actions. Linkage loss is small in every day-and-query stratum, with greater loss among rarely shared originals. Keep the Lula-only, Bolsonaro-only and shared-query strata and preserve unresolved references for sensitivity checks. There is no coverage basis for dropping a day or a query context.

The next task is to freeze the discovery-only graph specification, activity and source-popularity reference, and prior-tie comparison before evaluating holdout outcomes. An account is a node. Each eligible repost contributes one directed unit from the sharing account to the historical original author. Repeated actions determine edge weight. Recompute missingness among assigned sharers and test sensitivity to target popularity, query membership and discovery partition changes. No frozen-group performance or internal-share outcome was evaluated in M2. [First-pilot design](m1-advisor-synthesis.md#proposed-first-pilot)

### Reproduce the reconciliation

The rechecked November 26 host footer fingerprint matches the [archived manifest](m2-host-inventory.json). It covers paths, sizes, footer row counts and schemas. The run uses Python 3.10.12, DuckDB 1.5.6 and the system IANA time-zone database (2026f). The analysis is deterministic and uses no seed. The final run took 204 seconds and peaked at approximately 7.9 GiB of resident memory on the research host. This invocation writes only aggregate JSON and uses the specified local directory for database spill files.

```sh
mkdir -p runs/local
python3 -m pip install --target /tmp/m2-duckdb duckdb==1.5.6
PYTHONPATH=/tmp/m2-duckdb python3 scripts/m2_repost_coverage.py \
  /data/dados/twitter/corpus runs/local/m2-coverage-spill \
  > runs/local/m2-repost-coverage.json
```
