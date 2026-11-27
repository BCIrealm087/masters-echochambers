# Pre-outcome freeze for the within-corpus repost evaluation

**M3 · Within-corpus repost pilot · 2026-11-27**

Do the frozen account groups explain 19–21 October sharing after accounting for original-post popularity, timing and known ties? The four missing-author discovery refits completed all 480 registered runs and produced eligible partitions. The frequent-source completions broadly retained the original groups. The rare-source completions selected finer partitions and substantially changed account memberships. Holdout group agreement and prediction outcomes remain unopened.

## Discovery refit results

| Missing-author scenario | Resolution | Seed | Median ARI across eligible runs at selected resolution | ARI against original |
| --- | ---: | ---: | ---: | ---: |
| Internal, frequent | 0.5 | 19 | 0.9940 | 0.9933 |
| External, frequent | 0.5 | 5 | 0.9938 | 0.9880 |
| Internal, rare | 1.0 | 15 | 0.9959 | 0.5183 |
| External, rare | 1.0 | 8 | 0.9954 | 0.5179 |

The [refit record](m3-endpoint-refit-review.json) verifies the selected memberships and records alignment metrics across 660,089 common accounts. All four eight-draw reference rehearsals completed on the discovery margins. The scenario refits used the full registered selection procedure, so the membership differences combine endpoint completion with resolution selection. The small rehearsals establish that the reference can produce legal draws on the completed discovery inputs. They provide no estimate of holdout excess or holdout runtime. The host timestamps span about 2 hours 38 minutes from the first saved fit configuration to the workflow completion marker.

## Evaluation choices

The evaluator fixes the primary matched reference by São Paulo day and disjoint collection provenance. It uses 9,999 accepted draws per reference, exact release-time and self-repost constraints, Holm correction for eligible groups, and an event-weighted +5 percentage-point practical screen. Day-only, pooled, weighting, frequency exclusions and endpoint completions are sensitivity analyses. Proposal-budget failures leave the affected p-value unavailable. Prediction uses the frozen discovery calibration and compares the conditional and discovery-only author supports.

In endpoint scenarios, use the corresponding refitted membership. When a target overlaps discovery, retain its assigned source if it satisfies the constraints for every holdout copy. Otherwise keep the post unresolved and record the exclusion. For missing originals absent from the discovery completion, the [projection code](../../scripts/m3_holdout_completions.py) uses the same primary group and discovery frequency rankings as the discovery completion. A synthetic fixture verified that the rule leaves all holdout copies unresolved when an inherited assignment would introduce a self-repost on any copy. Preparation uses counts and feasibility constraints. The refit choices and primary predictions depend only on discovery data.

## Verified holdout margins

The refreshed host footer fingerprint matched the discovery snapshot and the holdout action and endpoint counts reconciled to M2 in all nine day-by-query strata. Of 5,188,313 distinct verified reposts, 4,770,214 meet the primary eligibility rule. The eligible records include 81,605 reposts of authors outside the primary partition, 325 repeated sharer–post actions within strata, and one same-second publication. No eligible observed pairing violates the publication-time or original-reference rule. There are 5,545 otherwise eligible actions by assigned sharers with unresolved authors. Five of 4,061 groups qualify for the secondary family by their margins.

Each endpoint scenario completes 2,890 holdout originals referenced in 6,301 actions. Of those actions, 326 inherit their original’s discovery scenario assignment and none violate the carryover constraints. Each scenario has 4,776,150 eligible actions under its refitted membership. Scenario eligibility can include sharers who gain a group in the refit.

## Reproduction

The [evaluation manifest](m3-evaluation-freeze.json) pins input, code, binary and margin fingerprints. Local working data stays under `runs/local/`. Compile the reference with the flags in the manifest and use the recorded Python, NumPy and DuckDB versions. The evaluator checks these fingerprints before any scoring. The primary command uses the group and equal-sharer outputs from the same accepted draws.

```bash
discovery=runs/local/m3-discovery
holdout=runs/local/m3-holdout
python3 scripts/m3_holdout.py primary-reference "$discovery/discovery.parquet" \
  "$discovery/leiden-weighted/accounts.npy" "$discovery/leiden-weighted/0.5-3.npy" \
  "$holdout" --binary "$discovery/reference-score-evaluation" --secondary
```

The next step is to run the frozen evaluation on the research host in a persistent terminal session and record the primary result, sensitivities and any resource limits. The command above has yet to be run.
