"""Construct deterministic, post-consistent missing-author discovery scenarios."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

import duckdb
import numpy as np

from m3_holdout import verify_frozen
from m3_reference_score import DISCOVERY_DAYS, atomic_json, digest

SCENARIOS = [(direction, rank) for direction in ("internal", "external")
             for rank in ("frequent", "rare")]


def choose(blocked, shares, candidates, by_group, direction):
    """Return one historical source and the assigned sharer actions it matches."""
    if direction == "internal":
        best = []
        for group, count in shares.items():
            for rank, account in by_group.get(group, ()):
                if account not in blocked:
                    best.append((-count, rank, account))
                    break
        if best:
            negative, _, account = min(best)
            return account, -negative
    best = None
    for account, group in candidates:
        if account in blocked:
            continue
        count = shares.get(group, 0)
        if best is None or count < best[1]:
            best = account, count
        if count == 0:
            break
    return best or (None, 0)


def complete(ledger, accounts_path, labels_path, output):
    verify_frozen(ledger, accounts_path, labels_path)
    accounts, labels = np.load(accounts_path), np.load(labels_path)
    output.mkdir(mode=0o700, parents=True, exist_ok=True)
    with duckdb.connect(config={"threads": 4, "memory_limit": "8GB",
                                "temp_directory": str(output.resolve())}) as db:
        dates = db.execute("SELECT DISTINCT day FROM read_parquet(?)", [str(ledger)]).fetchall()
        if {day for day, in dates} != set(DISCOVERY_DAYS):
            raise ValueError("Expected only the discovery days")
        db.read_parquet(str(ledger)).create_view("events")
        db.register("frozen_groups", {"account": accounts, "group_id": labels})
        authors = db.execute("""
            SELECT e.author, g.group_id, count(*) AS actions
            FROM events e JOIN frozen_groups g ON e.author = g.account
            WHERE e.sharer <> e.author AND e.membership <> 'unknown'
            GROUP BY 1, 2 ORDER BY actions DESC, e.author
        """).fetchall()
        # Missing references and sources with contradictory historical evidence
        # have no admissible synthetic replacement under these scenarios.
        missing = db.execute("""
            SELECT target, list(sharer) AS sharers, count(*) AS actions,
                   bool_and(author IS NULL AND resolution IN ('original absent', 'author missing')
                            AND action_second IS NOT NULL AND original_second IS NOT NULL
                            AND original_second <= action_second) AS admissible
            FROM events WHERE target IN (
                SELECT target FROM events WHERE author IS NULL AND target IS NOT NULL
            )
            GROUP BY target ORDER BY target
        """).fetchall()
        counts = db.execute("""
            SELECT count(*) FILTER (WHERE author IS NULL),
                   count(*) FILTER (WHERE author IS NULL AND target IS NULL)
            FROM events
        """).fetchone()
        group_of = dict(zip(map(int, accounts), map(int, labels)))
        profiles = []
        blocked_actions = 0
        for target, sharers, actions, admissible in missing:
            if not admissible:
                blocked_actions += actions
                continue
            profiles.append((target, set(sharers), actions,
                             Counter(group_of[s] for s in sharers if s in group_of)))
        ranked = {
            "frequent": [(a, g) for a, g, _ in authors],
            "rare": [(a, g) for a, g, _ in sorted(authors, key=lambda x: (x[2], x[0]))],
        }
        summaries = {}
        for direction, rank in SCENARIOS:
            name = f"{direction}-{rank}"
            candidates = ranked[rank]
            by_group = defaultdict(list)
            for slot, (account, group) in enumerate(candidates):
                by_group[group].append((slot, account))
            chosen, known, matches = [], [], 0
            for target, blocked, actions, shares in profiles:
                account, inside = choose(blocked, shares, candidates, by_group, direction)
                if account is not None:
                    chosen.append((target, account))
                    known.append(actions)
                    matches += inside
            path = output / f"{name}.parquet"
            temp = path.with_suffix(".tmp")
            db.register("replacement", {
                "post": np.array([target for target, _ in chosen], dtype=np.uint64),
                "imputed_author": np.array([account for _, account in chosen], dtype=np.uint64),
            })
            bad = db.execute("""
                SELECT count(*) FROM events e JOIN replacement r ON e.target = r.post
                WHERE e.author IS NOT NULL OR e.sharer = r.imputed_author
                   OR e.original_second > e.action_second
            """).fetchone()[0]
            if bad:
                raise ValueError(f"Illegal completion for {name}")
            db.execute("""
                COPY (
                    SELECT e.* REPLACE (coalesce(e.author, r.imputed_author) AS author,
                        CASE WHEN r.post IS NULL THEN e.resolution ELSE 'scenario imputation'
                             END AS resolution)
                    FROM events e LEFT JOIN replacement r ON e.target = r.post
                    ORDER BY e.post_id
                ) TO ? (FORMAT PARQUET, COMPRESSION ZSTD)
            """, [str(temp)])
            db.unregister("replacement")
            temp.replace(path)
            summaries[name] = dict(posts_imputed=len(chosen), actions_imputed=sum(known),
                                   internal_added_under_frozen_groups=matches,
                                   sha256=digest(path))
    result = dict(discovery_sha256=digest(ledger), candidate_authors=len(authors),
                  missing_actions=counts[0], missing_reference_actions=counts[1],
                  actions_on_inadmissible_posts=blocked_actions, scenarios=summaries)
    atomic_json(output / "completion.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("ledger", "accounts", "labels", "output"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    print(json.dumps(complete(args.ledger, args.accounts, args.labels, args.output), indent=2))
