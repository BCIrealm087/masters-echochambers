# Preparing the frozen holdout evaluation

**M3 · Within-corpus repost pilot · 2026-11-27**

Do the frozen account groups explain 19–21 October reposting after accounting for post popularity, timing and prior ties? The primary reference and prediction entry points are implemented and rehearsed on discovery data. The research host has not run the holdout preparation or scoring commands. The registered secondary inference and missing-endpoint checks remain in preparation.

## Population and reference

The [evaluation driver](../../scripts/m3_holdout.py) checks the discovery ledger and primary membership hashes against the [freeze](m3-discovery-freeze.json). The preparation command uses M2 reconciliation and compares archived and regenerated action and endpoint counts in each holdout date and query stratum. It verifies observed post-time legality, counts repeated sharer–post pairs and same-second pairings, and distinguishes assigned sharers, external authors and unresolved authors. Group test eligibility uses action and distinct-sharer counts alone. The preparation command saves its ledger and margins locally and generates no outcome statistics.

The [primary scorer](../../scripts/m3_reference_score.py) supports separate references by day and collection query, by day alone, and pooled. It summarizes per-query and leave-one-day-out results from the day-by-query draws. It also supports rebuilding the action and post margins after excluding the top one, top five or top 1% of authors or posts by eligible action frequency. The evaluator pins 9,999 draws and the registered practical screens. The discovery rehearsal checked nine base strata and verified that day-only and pooled modes covered the identical eligible action total across three days. Small runs also exercised the exclusion and scoring paths.

## Prediction

The [prediction implementation](../../scripts/m3_calibrate.py) uses only discovery actions for popularity and tie history. In conditional mode, it includes eligible resolved authors observed in the evaluation day and query, including destinations from unassigned sharers. Only assigned sharers' actions are scored. The discovery-support comparison uses a pooled external category for unseen authors. Both modes report paired log-score gain with sharer-clustered uncertainty, overall and by day, query and prior dyad status. Removing the most frequent authors or posts from the score summaries assesses dependence while holding each action's scoring support fixed.

A scalar comparison fixture verified both prediction supports, including exclusion of an unassigned sharer. Rerunning both original rolling folds reproduced the frozen settings and log scores. The discovery rehearsal split October 16–17 training from October 18 validation and scored all 1,641,194 eligible actions through both support definitions. The exercise checks the code path. The primary partition uses all three discovery days, so this rehearsal provides no independent estimate of predictive gain.

## Work remaining before opening outcomes

Implement and verify the group-level reference scores and Holm correction, equal-sharer and distinct-dyad reference statistics, concentration and historical-item diagnostics, and the missing-endpoint bounds and imputation analyses. Freeze the executable evaluation configuration and record dispositions for any sensitivity that exceeds available resources. The primary preparation, reference and prediction commands are separate stages so margin checks can be performed before group agreement or prediction outcomes are evaluated.
