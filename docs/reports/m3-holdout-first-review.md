# First review of the frozen repost holdout

**M3 · Within-corpus repost pilot · 2026-11-28**

Did frozen account groups identify persistent internal sharing and improve author prediction beyond prior ties? In the 19–21 October 2022 holdout, **96.27%** of 4,770,214 eligible reposts went to an original author in the sharer’s frozen group, against **50.74%** under the registered reference. Group membership improved prediction by **0.406 nats per action** over the history model. Both results support keeping frozen groups in the thesis’s structural baseline. The outstanding sensitivities will test how much that conclusion depends on weighting, highly reposted destinations, missing authors and the reference strata.

## What did we compare?

An account is a node and a directed arc runs from the sharer to the original author. The weighted Leiden partition was fitted on 16–18 October and kept fixed. The holdout covers verified non-self reposts with known query provenance, assigned sharers and resolved original authors. Resolved authors outside the partition count as external. The reference used 9,999 independent draws, reallocating original-post slots within São Paulo day and disjoint collection query while preserving sharer activity, original-post popularity, publication time eligibility and the exclusion of self-reposts. The [evaluation freeze](m3-evaluation-freeze.json) specifies the inputs and code. The [aggregate output](m3-holdout-first-review.json) records the reviewed results. Output fingerprints match the completed run markers.

## What did we learn?

| Structural comparison | Observed | Reference mean | Excess |
| --- | ---: | ---: | ---: |
| Event-weighted primary | 96.27% | 50.74% | +45.54 pp |
| Equal weight per sharer | 91.31% | 49.89% | +41.42 pp |

The central 95% reference range for the primary statistic was 50.69–50.78%. It describes variation under the matched reference. No draw reached the observed share, giving a one-sided Monte Carlo p-value of 0.0001 with the plus-one correction, the smallest reportable value with 9,999 draws. The excess exceeded all registered practical thresholds. Per-query excess ranged from +45.10 to +45.61 points, and leave-one-day-out excess ranged from +45.27 to +45.91 points.

Five groups met the secondary margin thresholds, and all five had Holm-adjusted p-values of 0.0005. Four exceeded the global five-point benchmark when used as a descriptive comparison. The fifth had +3.52 points of excess and an observed internal share of 3.52%. The two largest groups supplied 99.43% of eligible actions, so the event-weighted result chiefly describes those groups. The other 4,056 groups fell below the secondary testing margins.

| Prediction model on the conditional author support | Mean log score, nats per action |
| --- | ---: |
| Discovery author popularity | −7.8854 |
| Context popularity | −8.5633 |
| Context plus prior ties | −8.2389 |
| Context, prior ties and group membership | −7.8333 |

The paired group increment over prior ties was +0.4057 nats per action (sharer-clustered 95% interval +0.4033 to +0.4081). The group model also beat discovery author popularity by +0.0521 nats per action in the mean. The intermediate context and history models both scored below popularity alone. The gain over history was +0.3960 on previously unseen dyads and +0.4191 on seen dyads. It was +0.3673 with discovery-only support, where unseen authors share one external category. Those support definitions score different author outcomes, so the gains are interpreted within each support. Excluding actions to the top 1% of original authors reduced the conditional group increment to +0.2464 nats. The increment remained positive after the completed prediction exclusions, which use the fitted probabilities on the retained actions.

## How far does the evidence reach?

This is evidence of persistent internal repost circulation within the corpus window and incremental predictive information relative to the specified history model. The conditional prediction support uses the set of resolved destinations appearing in each evaluation stratum. That makes it a retrospective prediction exercise. The findings concern observed sharing, while exposure, endorsement, trust and political coherence require independent evidence. Query provenance identifies collection context and does not assign stance.

Assigning all 5,545 unresolved destinations from otherwise eligible assigned sharers first outside and then inside their groups bounds the **raw internal share** at 96.16–96.28%. Endpoint refits can also change the grouping and matched expectation. Those comparisons are still running.

## Runtime and second review

The completed primary reference used eight workers on the 16-core corpus host and finished 1,413 batches in about 4 hours 14 minutes. The separate day-only sensitivity spends much more time finding legal allocations on October 20. The aggregate record preserves a performance checkpoint with accepted draws, proposals and median batch duration. This gives future runs a benchmark for the broader reference as well as the primary one. Distinct-dyad, concentration, endpoint and alternative-reference comparisons will be reviewed together when their outputs or feasibility dispositions are available. The workflow continues under the frozen configuration.
