# Validating exact matched-post scoring for the repost pilot

**M3 · Within-corpus repost pilot · 2026-11-27**

Can the registered matched-post reference be scored with independent draws at corpus scale? The scorer matched exhaustive reference distributions on four small fixtures and completed a discovery-scale execution across all nine strata. The slowest stratum accepted 64 of 17,078 proposals. A 72-batch replay reused 71 checkpoints, regenerated the missing batch and reproduced identical scores. The holdout remains unopened.

## Scorer and throughput

The [scorer](../../scripts/m3_reference_score.cpp) implements the [registered time-ordered proposal and early self-repost rejection](m3-discovery-implementation.md#matched-post-reference-feasibility). It records internal-action counts only for legal assignments. Distinct original slots preserve post multiplicity. Group code zero is external. The [driver](../../scripts/m3_reference_score.py) sums independent stratum scores draw by draw, reports the event-weighted reference and applies the plus-one upper-tail correction. It retains batch results locally with distinct deterministic seeds, atomic writes and an input and settings fingerprint. A proposal cap fails the affected batch and prevents the driver from emitting a p-value from an incomplete set.

The 64-draw benchmark used GCC 11.4.0 with `-O3 -std=c++17`, Python 3.10.12, DuckDB 1.5.6, NumPy 1.26.4 and eight concurrent batch workers on the 16-core corpus host. It finished in about 49 seconds across 6,764,928 discovery actions, including input preparation after writing the run configuration. A linear extrapolation gives roughly **two hours** for 9,999 draws at that throughput. This estimate applies to the primary statistic on the measured discovery margins. Holdout acceptance, workload contention, and additional sensitivity scoring can change runtime. A long execution should run in a persistent host session with a saved log and status on exit.

## Simulation checks

The [simulation driver](../../scripts/m3_reference_simulation.py) retained observed clocks, endpoints, and group labels in nine discovery-derived 10-slot profiles, one per day and query. It sampled sharers from the largest group in each stratum and from other groups. The concentrated profiles repeated two actions twice each to make 14 slots with unequal sharer activity, repeated ties and highly reused originals. Selective loss removed all slots for each affected original together, with probabilities 0.35 for authors in the largest sampled sharer group and 0.03 otherwise. For every profile, the null was uniform over legal assignments and the alternative tilted that distribution by exp(1.5 × internal actions). The simulations recomputed the exact conditional reference on the surviving slots after loss.

| Scenario | Null rejection at 5% | Injected affinity rejection | Mean excess with injected affinity |
| --- | ---: | ---: | ---: |
| Discovery profiles | 1.0% | 38.9% | +26.3 pp |
| Concentrated slots | 1.4% | 40.9% | +20.8 pp |
| Concentrated slots with group-selective loss | 0.3% | 27.9% | +18.9 pp |

Each row uses 1,000 replicates under each data-generating condition. The discrete reference was conservative on these small profiles. Group-selective loss reduced detection relative to the same scenario's corresponding full data, where 42.3% of injected-affinity replicates rejected. These perturbations validate behavior under known conditions and give no estimate of holdout power. The corpus benchmark checks throughput and execution across empirical strata, where a known-outcome experiment is unavailable.

## Reproduction and handoff

```bash
work=runs/local/m3-discovery
g++ -O3 -std=c++17 -Wall -Wextra scripts/m3_reference_score.cpp -o "$work/reference-score"
python3 scripts/m3_reference_score.py "$work/discovery.parquet" \
  "$work/leiden-weighted/accounts.npy" "$work/leiden-weighted/0.5-3.npy" \
  "$work/reference-score" "$work/scorer-validation-batches" --draws 64 --batch-size 8
python3 scripts/m3_reference_simulation.py "$work/discovery.parquet" \
  "$work/leiden-weighted/accounts.npy" "$work/leiden-weighted/0.5-3.npy" "$work/reference-score"
```

The [aggregate record](m3-reference-validation.json) archives fingerprints, fixture checks, proposal counts, simulation settings and results. The current entry point is restricted to discovery dates. Preparing the holdout entry point, verifying its population and margins, and implementing the registered secondary and sensitivity statistics remain separate work before scoring.
