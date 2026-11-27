"""Prepare holdout sensitivity ledgers without scoring account agreement."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

import duckdb
import numpy as np

from m3_complete_endpoints import SCENARIOS, choose
from m3_holdout import margins, verify_frozen
from m3_reference_score import HOLDOUT_DAYS, atomic_json, digest


def prepare(discovery, accounts_path, labels_path, completions, holdout):
    verify_frozen(discovery, accounts_path, labels_path)
    primary = json.loads((holdout / "margins.json").read_text())
    ledger = holdout / "holdout.parquet"
    if digest(ledger) != primary["ledger_sha256"]:
        raise ValueError("Prepared holdout ledger fingerprint mismatch")
    recorded = json.loads((completions / "completion.json").read_text())["scenarios"]
    accounts, labels = np.load(accounts_path), np.load(labels_path)
    group_of = dict(zip(map(int, accounts), map(int, labels)))
    output = holdout / "endpoint-completions"
    output.mkdir(mode=0o700, parents=True, exist_ok=True)
    summaries = {}
    with duckdb.connect(config={"threads": 4, "memory_limit": "8GB",
                                "temp_directory": str(output.resolve())}) as db:
        db.read_parquet(str(ledger)).create_view("events")
        db.read_parquet(str(discovery)).create_view("training")
        if {day for day, in db.execute("SELECT DISTINCT day FROM events").fetchall()} != set(
                HOLDOUT_DAYS):
            raise ValueError("Unexpected evaluation dates")
        db.register("primary_groups", {"account": accounts, "group_id": labels})
        authors = db.execute("""
            SELECT a.author, g.group_id, count(*) AS actions
            FROM training a JOIN primary_groups g ON a.author = g.account
            WHERE a.sharer <> a.author AND a.membership <> 'unknown'
            GROUP BY 1, 2 ORDER BY actions DESC, a.author
        """).fetchall()
        all_missing = db.execute("SELECT count(*) FROM events WHERE author IS NULL").fetchone()[0]
        profiles = db.execute("""
            SELECT target, list(sharer) AS sharers, count(*) AS actions,
                   bool_and(author IS NULL AND resolution IN ('original absent', 'author missing')
                            AND original_second IS NOT NULL AND action_second IS NOT NULL
                            AND original_second <= action_second) AS admissible
            FROM events WHERE target IN (
                SELECT target FROM events WHERE author IS NULL AND target IS NOT NULL
            )
            GROUP BY target ORDER BY target
        """).fetchall()
        ranked = {
            "frequent": [(a, g) for a, g, _ in authors],
            "rare": [(a, g) for a, g, _ in sorted(authors, key=lambda x: (x[2], x[0]))],
        }
        rankings = {}
        for name, candidates in ranked.items():
            groups = defaultdict(list)
            for index, (account, group) in enumerate(candidates):
                groups[group].append((index, account))
            rankings[name] = groups
        for direction, rank in SCENARIOS:
            name = f"{direction}-{rank}"
            prior = completions / f"{name}.parquet"
            if digest(prior) != recorded[name]["sha256"]:
                raise ValueError(f"Discovery completion fingerprint mismatch: {name}")
            inherited = dict(db.execute("""
                SELECT DISTINCT target, author FROM read_parquet(?)
                WHERE resolution = 'scenario imputation'
            """, [str(prior)]).fetchall())
            chosen = []
            reused = blocked_overlap = 0
            for target, sharers, actions, admissible in profiles:
                blocked = set(sharers)
                if target in inherited:
                    author = inherited[target]
                    if not admissible or author in blocked:
                        blocked_overlap += actions
                        continue
                    reused += actions
                elif admissible:
                    shares = Counter(group_of[s] for s in sharers if s in group_of)
                    author, _ = choose(blocked, shares, ranked[rank], rankings[rank], direction)
                else:
                    continue
                if author is not None:
                    chosen.append((target, author, actions))
            db.register("replacement", {
                "post": np.array([row[0] for row in chosen], dtype=np.uint64),
                "imputed_author": np.array([row[1] for row in chosen], dtype=np.uint64),
            })
            db.execute("""
                CREATE OR REPLACE TEMP VIEW evaluation_ledger AS
                SELECT e.* REPLACE (coalesce(e.author, r.imputed_author) AS author,
                    CASE WHEN r.post IS NULL THEN e.resolution ELSE 'scenario imputation'
                         END AS resolution)
                FROM events e LEFT JOIN replacement r ON e.target = r.post
            """)
            illegal = db.execute("""
                SELECT count(*) FROM evaluation_ledger
                WHERE resolution = 'scenario imputation' AND
                      (author IS NULL OR author = sharer OR original_second > action_second)
            """).fetchone()[0]
            if illegal:
                raise ValueError(f"Illegal scenario assignment: {name}")
            grid = json.loads((completions / name / "grid.json").read_text())
            if grid["selected"] is None:
                raise ValueError(f"No eligible refit for scenario {name}")
            accounts_file = completions / name / "accounts.npy"
            scenario_margins = margins(db, np.load(accounts_file))
            db.unregister("assigned_accounts")
            if any(row["illegal_time_or_reference"] for row in scenario_margins):
                raise ValueError(f"Illegal reference margins for scenario {name}")
            path = output / f"{name}.parquet"
            temp = path.with_suffix(".tmp")
            db.execute("""
                COPY (SELECT * FROM evaluation_ledger ORDER BY post_id)
                TO ? (FORMAT PARQUET, COMPRESSION ZSTD)
            """, [str(temp)])
            temp.replace(path)
            db.unregister("replacement")
            completed_actions = sum(row[2] for row in chosen)
            summaries[name] = dict(ledger_sha256=digest(path), posts_imputed=len(chosen),
                                   actions_imputed=completed_actions, inherited_actions=reused,
                                   blocked_overlap_actions=blocked_overlap,
                                   still_unresolved_actions=all_missing-completed_actions,
                                   margins=scenario_margins)
    result = dict(primary_ledger_sha256=primary["ledger_sha256"], scenarios=summaries)
    atomic_json(output / "margins.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("discovery", "accounts", "labels", "completions", "holdout"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    print(json.dumps(prepare(args.discovery, args.accounts, args.labels,
                             args.completions, args.holdout), indent=2))
