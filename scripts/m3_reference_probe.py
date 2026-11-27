"""Probe exact rejection feasibility using the discovery ledger only."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import json
from itertools import permutations
from pathlib import Path
import subprocess
from time import perf_counter

import duckdb
import numpy as np


def verify_probe(binary):
    fixtures = [
        # The two legal derangements cannot be joined by a legal pair swap.
        ([1, 2, 3], [1, 1, 1], [2, 3, 1], [1, 1, 1]),
        ([1, 2, 3], [1, 2, 3], [2, 3, 1], [1, 2, 3]),
        ([1, 2, 2], [2, 3, 3], [2, 1, 1], [1, 2, 2]),
    ]
    checked = []
    for sharers, actions, authors, originals in fixtures:
        orders = [
            order for order in permutations(range(len(actions)))
            if all(originals[j] <= action for j, action in zip(order, actions))
        ]
        legal = sum(all(authors[j] != sharer for j, sharer in zip(order, sharers))
                    for order in orders)
        expected = legal / len(orders)
        data = dict(sharer=np.array(sharers), action_second=np.array(actions),
                    author=np.array(authors), original_second=np.array(originals))
        for early in (False, True):
            result = probe(binary, 100000, 314159, "fixture", "fixture", data, early)
            observed = result["accepted"] / result["draws"]
            if abs(observed - expected) > 0.01:
                raise ValueError("Compiled rejection rate disagrees with enumeration")
            checked.append(dict(time_feasible=len(orders), legal=legal, early_reject=early,
                                draws=result["draws"], accepted=result["accepted"]))
    return checked


def probe(binary, draws, seed, day, context, data, early_reject=False):
    actions = data["action_second"]
    order = np.argsort(data["original_second"], kind="stable")
    fields = (len(actions), data["sharer"], actions,
              data["author"][order], data["original_second"][order])
    payload = b"".join(np.asarray(field, dtype="<u8").tobytes() for field in fields)
    start = perf_counter()
    command = [str(binary.resolve()), str(draws), str(seed)]
    if early_reject:
        command.append("--early-reject")
    result = subprocess.run(command, input=payload, capture_output=True, check=True)
    accepted, total, minimum, maximum = map(int, result.stdout.split())
    summary = dict(day=str(day), context=context, slots=len(actions), draws=draws, seed=seed,
                   accepted=accepted, seconds=perf_counter() - start,
                   zero_acceptance_upper_95=1 - 0.05 ** (1 / draws) if accepted == 0 else None)
    if not early_reject:
        summary.update(self_min=minimum, self_max=maximum, self_mean=total / draws)
    return summary


def run(ledger, binary, draws, workers, seed, early_reject):
    jobs = []
    started = perf_counter()
    with duckdb.connect(config={"threads": 2}) as db, ThreadPoolExecutor(workers) as pool:
        scope = db.execute("SELECT DISTINCT day FROM read_parquet(?)",
                           [str(ledger)]).fetchall()
        expected = {(date(2022, 10, day),) for day in (16, 17, 18)}
        if set(scope) != expected:
            raise ValueError("Expected only the three discovery days")
        rows = db.execute("""
            SELECT day, membership, count(*) AS actions, count(target) AS references,
                   count(*) - count(DISTINCT (sharer, target)) AS repeat_sharer_post_actions,
                   count(*) FILTER (WHERE original_second = action_second) AS same_second,
                   count(*) FILTER (WHERE original_second > action_second) AS after_action
            FROM read_parquet(?) WHERE sharer <> author AND membership <> 'unknown'
            GROUP BY ALL ORDER BY day, membership
        """, [str(ledger)]).fetchall()
        semantics = []
        for day, context, actions, references, repeats, simultaneous, after in rows:
            if actions != references or after:
                raise ValueError(f"Observed pairing failed legality check in {day} {context}")
            semantics.append(dict(day=str(day), context=context, slots=actions,
                                  repeat_sharer_post_actions=repeats, same_second=simultaneous))
            data = db.execute("""
                SELECT sharer, author, action_second, original_second FROM read_parquet(?)
                WHERE day = ? AND membership = ? AND sharer <> author
                ORDER BY action_second, post_id
            """, [str(ledger), day, context]).fetchnumpy()
            jobs.append(pool.submit(probe, binary, draws, seed + len(jobs), day, context, data,
                                    early_reject))
        results = [job.result() for job in jobs]
    return dict(workers=workers, seconds=perf_counter() - started, early_reject=early_reject,
                strata=results, slot_semantics=semantics, compiled_fixtures=verify_probe(binary))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("binary", type=Path)
    parser.add_argument("--draws", type=int, default=256)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20261126)
    parser.add_argument("--early-reject", action="store_true")
    args = parser.parse_args()
    if args.draws < 1:
        parser.error("--draws must be positive")
    print(json.dumps(run(args.ledger, args.binary, args.draws, args.workers, args.seed,
                         args.early_reject), indent=2))
