"""Validate primary reference behavior on small discovery-derived margins."""
import argparse
from collections import Counter
from functools import lru_cache
import json
from math import exp
from pathlib import Path

import duckdb
import numpy as np

from m3_reference import exact_distribution, legal_targets
from m3_reference_score import SCORE_COLUMNS, draw, load_strata, pack

REPLICATES = 1000
SEED = 20261127


def masks(sharers, actions, authors, originals, sharer_groups, author_groups):
    allowed = legal_targets(sharers, actions, authors, originals)
    internal = tuple(sum(1 << j for j, group in enumerate(author_groups)
                         if group and group == own) for own in sharer_groups)
    return allowed, internal


def fixture(binary):
    fixtures = [
        ([1, 2, 3], [1, 1, 1], [2, 3, 1], [1, 1, 1], [1, 2, 3], [1, 2, 3]),
        ([1, 2, 3], [1, 2, 3], [2, 3, 1], [1, 2, 3], [1, 2, 3], [1, 2, 3]),
        ([1, 2, 2], [2, 3, 3], [2, 1, 1], [1, 2, 2], [1, 2, 2], [2, 1, 1]),
        ([1, 2, 3], [1, 1, 1], [2, 3, 1], [1, 1, 1], [0, 0, 1], [0, 1, 0]),
    ]
    results = []
    for columns in fixtures:
        allowed, internal = masks(*columns)
        expected = np.asarray(exact_distribution(allowed, internal), dtype=float)
        scores, tried = draw(binary, pack(*map(np.asarray, columns)), 10000, SEED, 100000)
        observed = np.bincount(scores, minlength=len(expected)) / len(scores)
        np.testing.assert_allclose(observed, expected, atol=.02, rtol=0)
        results.append(dict(expected=expected.tolist(), sampled=observed.tolist(), proposals=tried))
    return results


def select_profiles(ledger, accounts, labels):
    with duckdb.connect(config={"threads": 4}) as db:
        counts = db.execute("""
            SELECT cast(day AS VARCHAR), membership, max(post_reposts), max(sharer_reposts)
            FROM (
                SELECT day, membership,
                  count(*) OVER (PARTITION BY day, membership, target) AS post_reposts,
                  count(*) OVER (PARTITION BY day, membership, sharer) AS sharer_reposts
                FROM read_parquet(?) WHERE sharer <> author
            ) GROUP BY 1, 2 ORDER BY 1, 2
        """, [str(ledger)]).fetchall()
    profiles = []
    for (day, context, data), summary in zip(load_strata(ledger, accounts, labels), counts, strict=True):
        if (day, context) != tuple(summary[:2]):
            raise ValueError("Mismatched discovery profiles")
        sharer_group, author_group = data["sharer_group"], data["author_group"]
        # Take a mixture of internal and cross-group actions and then retain their
        # observed clocks and endpoints. The top observed margins set stress weights.
        primary = Counter(sharer_group).most_common(1)[0][0]
        rng = np.random.default_rng(SEED + len(profiles))
        pools = [np.flatnonzero((sharer_group == primary) == s)
                 for s in (False, True)]
        chosen = [rng.choice(index, 5, replace=False) for index in pools]
        selected = np.sort(np.concatenate(chosen))
        profile = np.stack([
            np.asarray(data[column][selected], dtype=np.uint64)
            for column in (*SCORE_COLUMNS, "target")
        ])
        profiles.append((profile, dict(day=day, context=context, max_post_actions=summary[2],
                                       max_sharer_actions=summary[3])))
    return profiles


def concentrated(profile):
    # Repeat two observed actions from the dominant groups as distinct slots.
    # Duplicate original slots model a burst of amplification and repeated ties.
    return profile[:, np.r_[np.arange(10), 2, 2, 7, 7]]


def generator(profile, beta):
    allowed, internal = masks(*profile[:6])
    n = len(allowed)

    @lru_cache(maxsize=None)
    def weight(remaining):
        if not remaining:
            return 1.0
        row = n - remaining.bit_count()
        return sum(weight(remaining ^ flag) * exp(beta * bool(internal[row] & flag))
                   for flag in choices(remaining & allowed[row]))

    def sample(rng):
        remaining = (1 << n) - 1
        order = []
        while remaining:
            row = len(order)
            options = list(choices(remaining & allowed[row]))
            mass = np.array([weight(remaining ^ flag) * exp(beta * bool(internal[row] & flag))
                             for flag in options])
            flag = options[rng.choice(len(options), p=mass / mass.sum())]
            order.append(flag.bit_length() - 1)
            remaining ^= flag
        return order
    return sample


def choices(bits):
    while bits:
        flag = bits & -bits
        yield flag
        bits ^= flag


def distribution(profile):
    return np.asarray(exact_distribution(*masks(*profile[:6])), dtype=float)


def score_summary(profile, null):
    size = profile.shape[1]
    if not size:
        return 1.0, 0.0
    observed = np.count_nonzero((profile[4] != 0) & (profile[4] == profile[5]))
    return float(null[observed:].sum()), float(100*(observed - null @ np.arange(size+1))/size)


def simulate(profiles, beta, stress, loss):
    full = [concentrated(p) if stress else p for p, _ in profiles]
    samplers = [generator(p, beta) for p in full]
    distributions = [distribution(p) for p in full]
    rng = np.random.default_rng(SEED)
    rejected = practical = full_rejected = 0
    deltas, removals = [], []
    for replicate in range(REPLICATES):
        index = replicate % len(full)
        profile = full[index]
        order = samplers[index](rng)
        ledger = profile.copy()
        original_fields = [2, 3, 5, 6]
        ledger[original_fields, :] = profile[original_fields, :][:, order]
        # Drop copies together by original slot provenance. Repeated profile
        # slots retain the same provenance key through the allocation.
        full_p, full_excess = score_summary(ledger, distributions[index])
        full_rejected += full_p <= .05
        if loss:
            _, inverse = np.unique(ledger[6], return_inverse=True)
            group = Counter(ledger[4]).most_common(1)[0][0]
            missing = rng.random(inverse.max()+1)[inverse] < np.where(ledger[5] == group, .35, .03)
            ledger = ledger[:, ~missing]
            removals.append(int(missing.sum()))
        p, excess = score_summary(ledger, distribution(ledger)) if loss else (full_p, full_excess)
        rejected += p <= .05
        practical += p <= .05 and excess >= 5
        deltas.append(excess)
    return dict(replicates=REPLICATES, beta=beta, concentrated_slots=stress,
                group_selective_loss=loss, rejection_rate=rejected/REPLICATES,
                full_data_rejection_rate=full_rejected/REPLICATES,
                significance_and_five_point_rate=practical/REPLICATES,
                mean_excess_percentage_points=float(np.mean(deltas)),
                mean_removed_slots=float(np.mean(removals)) if removals else 0.0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("ledger", "accounts", "membership", "binary"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    checks = fixture(args.binary)
    profiles = select_profiles(args.ledger, np.load(args.accounts), np.load(args.membership))
    results = [simulate(profiles, beta, stress, loss)
               for stress, loss in [(False, False), (True, False), (True, True)]
               for beta in (0, 1.5)]
    print(json.dumps(dict(seed=SEED, fixtures=checks, inputs=[p[1] for p in profiles],
                          scenarios=results), indent=2, allow_nan=False))
