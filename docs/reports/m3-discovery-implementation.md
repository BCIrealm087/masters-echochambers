# Discovery cohort and implementation checks for the repost pilot

**M3 · Within-corpus repost pilot · 2026-11-26**

Can account groups learned from 16–18 October 2022 explain later reposting? The discovery extract reproduced the M2 action and endpoint counts in all nine day-by-query strata. This establishes which actions enter the clustering stage and provides a versioned baseline for checking the eventual partition. Holdout outcomes remain unopened.

## Discovery population

The extract applies the M2 reconciliation to São Paulo action dates 16–18 October, with October 19 as an exclusive cutoff. It deduplicates explicit reposts by verified action ID, preserves disjoint Lula-only, Bolsonaro-only and shared provenance, and resolves the historical author against the corpus. The graph uses accounts as nodes and arcs from sharers to original authors weighted by distinct eligible reposts. The [registered protocol](m3-repost-pilot-specification.md) fixes selection and validation rules.

| Discovery actions | Count |
| --- | ---: |
| Distinct verified reposts | 6,800,676 |
| Missing sharer | 0 |
| Unresolved original author | 22,464 |
| Verified self-reposts | 13,284 |
| Eligible non-self reposts | 6,764,928 |
| Eligible reposts with original-ID publication after action | 0 |

Counts by date and collection provenance and the local ledger hash are in the [aggregate extract](m3-discovery-extract.json). The discovery counts agree with the [M2 aggregate](m2-repost-coverage.json). The ledger and account memberships stay under the ignored local working directory.

## Implementation checks

Directed Leiden and directed Louvain both reproduced the fixture's normalized modularity of −4/49 and its directed in- and out-strengths. A two-component synthetic ledger exercised all six resolutions and 20 seeds for each optimizer. Both selected resolution 1 and seed 0, with median eligible-run adjusted Rand index 1. The matched-post reference matched exhaustive permutation counts on small fixtures, including a legal assignment space disconnected under pair swaps. The prediction fixture checked normalization, recency weighting, exclusion of the sharer from the risk set, positive mass for an unseen author and the group multiplier.

These checks establish behavior on small examples. The small-stratum exact reference has a 16-slot limit, and the reference remains unvalidated at corpus scale. The prediction check covers individual author distributions. Rolling-fold calibration and scale checks remain pending.

## Reproduction and next step

Run from the repository root with Python 3.10.12 and DuckDB 1.5.6. The graph checks used igraph 0.11.9, leidenalg 0.10.2, NetworkX 3.4.2, NumPy 1.26.4, SciPy 1.13.1 and scikit-learn 1.6.1. The extract uses four DuckDB threads. Set `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1` for graph fitting.

```bash
python3 scripts/m3_extract_discovery.py /data/dados/twitter/corpus runs/local/m3-discovery
python3 scripts/m3_discovery.py --fixture
python3 scripts/m3_reference.py
python3 scripts/m3_prediction.py
python3 scripts/m3_discovery.py --ledger runs/local/m3-discovery/discovery.parquet \
  --output runs/local/m3-discovery/leiden-weighted
```

The empirical weighted Leiden grid is the first fitting run. The full grid, sensitivity runs, discovery-only calibration and reference checks must be assessed before the run manifest can be frozen.

## Discovery fitting checkpoint

The host footer fingerprint matches the M2 snapshot. The empirical weighted and binary Leiden grids, both weighted Leiden rolling-fold grids, and the weighted directed Louvain grid have started. Directed Infomap 2.8.0 runs on the weighted, binary and reversed weighted graphs with 20 trials and seed 20. The comparison flattens the finest modules and retains the hierarchy locally. The leave-day-out and hub-removal runs use the selected primary settings after its grid finishes.

The discovery-only prediction code aggregates the risk set by query provenance and subtracts the focal sharer from the author support. A synthetic two-day fixture reproduced the scalar scoring equations, including warm and unseen destinations and the same-group probability mass. The empirical context and dyad stages selected a context prior mass of 100, a dyad prior mass of 100, and a one-day recency half-life over 1,929,561 October 17 actions and 1,641,194 October 18 actions. This is a discovery calibration result. The membership coefficient awaits fold partitions selected by the registered rule.

For the two fold grids, use `--before 2022-10-17` and `--before 2022-10-18` with the same weighted grid invocation and separate output directories. Use `--binary` or `--method louvain` for the corresponding full discovery comparisons. After the grids complete, the calibration and partition-dependent perturbations can run from the discovery ledger.

```bash
python3 scripts/m3_calibrate.py runs/local/m3-discovery/discovery.parquet \
  runs/local/m3-discovery/leiden-fold-17 runs/local/m3-discovery/leiden-fold-18
python3 scripts/m3_sensitivities.py runs/local/m3-discovery/discovery.parquet \
  runs/local/m3-discovery/perturbations --primary runs/local/m3-discovery/leiden-weighted
```

The empirical partition, large-stratum reference validation and run manifest remain pending. The holdout outcomes remain unopened.
