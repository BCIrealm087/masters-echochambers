# Sensitivity checks for the frozen repost evaluation

**M3 · Within-corpus repost pilot · 2026-11-27**

How sensitive is the matched-post comparison to group size, active sharers, repeated ties and unresolved authors? The group and weighting checks now run on the frozen discovery ledger. A 64-draw rehearsal produced the same primary result with the group and equal-sharer statistics enabled, and a separate whole-window rehearsal validated distinct-dyad deduplication. Raw missing-author bounds and circulation diagnostics also ran on discovery data. Holdout outcomes remain unopened.

## Group and weighting checks

The [reference scorer](../../scripts/m3_reference_score.py) calculates every group’s test eligibility from its action and distinct-sharer margins. It tests groups with at least 100 eligible actions and 20 distinct eligible sharers and applies Holm to the resulting one-sided p-values. Groups below either threshold receive an explicit disposition. Eight of 4,061 frozen groups qualified in the discovery rehearsal.

The equal-sharer statistic gives each eligible action weight equal to the inverse of its sharer’s action count across the evaluation interval. Because the reference fixes those margins, a sharer receives the same total weight in every draw. A compiled fixture matched exhaustive joint scores for the primary count, weighted count and group counts. A separate check reproduced hand-calculated Holm adjustments. On 6,764,928 discovery actions, 64 draws with eight workers took approximately 54 seconds after saving the configuration, versus about 49 seconds in the [earlier primary benchmark](m3-reference-validation.md). These runs were timed separately and give an approximate comparison of overhead.

The [distinct-dyad scorer](../../scripts/m3_distinct_dyads.py) streams accepted author allocations for each stratum, then combines and deduplicates ordered sharer–author pairs across the full interval for each draw. The denominator is recomputed for every allocation. A duplicate-pair fixture verified the deduplication rule. The observed discovery ledger reproduced the frozen graph’s 4,484,125 distinct dyads, and eight reference draws took about 13 seconds with four workers, including loading and encoding the ledger. The scorer checkpoints only the two aggregate counts for each draw. The full 9,999-draw runtime remains unmeasured.

## Endpoint coverage and circulation

The [evaluation driver](../../scripts/m3_holdout.py) reports raw internal-share bounds among assigned sharers overall and by day and query, group, sharer activity and target reuse. It excludes verified self-reposts and counts resolved authors outside the partition as external. The lower and upper bounds assign all otherwise eligible unresolved endpoints to external and internal destinations, respectively. All four breakdowns reconciled to 6,764,928 resolved and 20,599 unresolved discovery actions among assigned sharers. These are bounds on the raw share. The matched reference would need to be recomputed after each post-level completion to bound the contrast.

The driver also reports maximum action shares and inverse squared-share sums for sharers, authors, posts and dyads. It distinguishes actions involving new dyads, originals unseen in discovery and originals published since the evaluation start. The October 18 rehearsal used October 16–17 as history for these checks.

## Remaining work

Implement a coherent assignment of missing authors once per original, with internal, external, frequent-source and rare-source scenarios. Verify eligibility after imputation and refit discovery partitions under corresponding completions, or document which scenarios cannot be completed. Then freeze the executable evaluation configuration and verify holdout margins before opening outcomes.

For the discovery benchmark, build [the scorer](../../scripts/m3_reference_score.cpp) with GCC 11.4.0 and `-O3 -std=c++17 -Wall -Wextra`. Use the [discovery benchmark inputs](m3-reference-validation.md#reproduction-and-handoff) with a fresh work directory and add `--secondary` to the 64-draw reference command. The same frozen artifacts and binary can be passed to the distinct-dyad script with `--draws 8 --workers 4`. The seed for both rehearsals was 20261127.
