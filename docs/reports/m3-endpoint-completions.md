# Missing-author completions for the discovery sensitivity

**M3 · Within-corpus repost pilot · 2026-11-27**

How sensitive are the discovered account groups to unknown original authors? Four deterministic scenarios each complete 3,435 originals referenced by 22,464 reposts on the discovery dates. The refits are in progress. All scenario choices and checks used the 16–18 October discovery window. Holdout outcomes remain unopened.

## Scenario construction

The [completion script](../../scripts/m3_complete_endpoints.py) uses the frozen account groups and 77,817 original authors with resolved incoming discovery actions. For each missing original, it assigns one source to all copies, choosing the feasible candidate whose group matches the largest or smallest number of assigned sharer actions. Within that constraint it prefers either frequently or rarely reposted discovery authors, measured by action counts. Numeric author ID breaks frequency ties. These are deliberately concentrated stress tests. They provide no evidence about the identities of the missing authors.

A candidate is infeasible if it would introduce a self-repost on any recorded copy. Eligible missing originals must retain a usable target ID and publication second and have either absent historical records or no historical author. The procedure leaves conflicting historical evidence intact. In this discovery slice all unresolved actions met the post-level eligibility rule. An independent join confirmed that the four scenarios preserve all 6,800,676 action IDs and already resolved authors, assign one author per completed original, and introduce no self-reposts or after-action publication times. The [aggregate record](m3-endpoint-completions.json) archives counts and ledger hashes.

| Scenario | Newly internal under original groups | Assigned scenario authors | Most added actions to one author |
| --- | ---: | ---: | ---: |
| Internal, frequent | 20,294 | 23 | 13,367 |
| Internal, rare | 20,294 | 23 | 13,367 |
| External, frequent | 0 | 4 | 13,737 |
| External, rare | 0 | 2 | 13,737 |

The internal scenarios cannot make every repost internal because actions sharing an original can originate in different groups. Choosing a rare source uses its frequency in observed discovery. The resulting completed ledger can still concentrate imputed actions on that same author.

## Refit execution and recovery

Each scenario reruns the registered weighted Leiden grid of six resolutions and 20 seeds, with the existing connectivity, coverage and stability selection. A small graph fixture gave identical memberships under serial and parallel fitting and confirmed that a restart reuses saved seed files. The [refit driver](../../scripts/m3_refit_endpoints.py) atomically saves each membership and checks the graph fingerprint, fit code, software versions, resolutions and seeds on restart. The [workflow](../../scripts/m3_run_endpoint_refits.py) then runs an eight-draw discovery-only reference rehearsal under each available refitted partition. A proposal-budget failure is recorded for review.

The host has 16 logical cores and 62 GiB of RAM. Four scenario processes each use three fit workers, leaving CPU capacity for the host and other tasks. The 480 fit checkpoints require about 1.2 GiB of membership storage, with separate local logs and ledgers. The prior serial-per-grid timings give a rough estimate of a few hours with this worker allocation. Runtime depends on convergence and resource contention. Read the atomic workflow status at `runs/local/m3-discovery/endpoint-completions/workflow-status.json` on completion and the per-scenario `status.json` files during execution. The detached `endpoint-refits` tmux session on socket `m3-endpoints` survives disconnection and emits a terminal bell when the workflow exits. Status files are available after the session ends.

Before finalizing the evaluator, review partition stability and reference feasibility for all four cases. Pair each usable refit with its corresponding holdout sensitivity. If an original occurs in both periods, reuse the discovery scenario assignment when it is legal for the corresponding holdout copies and report unresolved exceptions. Freeze the executable configuration and check holdout eligibility and timing before scoring.
