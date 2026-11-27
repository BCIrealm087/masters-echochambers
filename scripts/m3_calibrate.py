"""Calibrate nested author models on rolling discovery folds."""
import argparse
import json
from pathlib import Path

import duckdb
import numpy as np

MASSES = (100, 10, 1)
HALF_LIVES = (None, 3, 1)
BETAS = (0, -0.5, 0.5, -1, 1, -2, 2)
FOLD_DAYS = ("2022-10-17", "2022-10-18")


def load_fold(ledger, day, partition=None, *, evaluation=None,
              training_end=None, discovery_support=False):
    with duckdb.connect(config={"threads": 4}) as db:
        db.execute("""
            CREATE TEMP TABLE events AS SELECT * FROM read_parquet(?)
            WHERE sharer <> author AND membership <> 'unknown' AND day <= cast(? AS DATE)
        """, [[str(ledger)] if evaluation is None else [str(ledger), str(evaluation)], day])
        if partition:
            accounts, groups = partition
            db.register("account_groups", {"account": accounts, "label": groups})
        else:
            db.execute("CREATE TEMP TABLE account_groups (account UBIGINT, label INTEGER)")
        # Anchor recency at local midnight to keep exponent magnitudes small.
        db.execute("CREATE TEMP TABLE boundary AS SELECT cast(? AS DATE) AS day, "
                   "epoch(cast(? AS DATE)) + 10800 AS anchor, cast(? AS DATE) AS training_end",
                   [day, day, training_end or day])
        db.execute("""
            CREATE TEMP TABLE train AS SELECT e.*,
                s.label AS sharer_group, a.label AS author_group,
                pow(2, (action_second - anchor) / 259200.0) AS recent3,
                pow(2, (action_second - anchor) / 86400.0) AS recent1
            FROM events e CROSS JOIN boundary b
            LEFT JOIN account_groups s ON e.sharer = s.account
            LEFT JOIN account_groups a ON e.author = a.account
            WHERE e.day < b.training_end;
            CREATE TEMP TABLE validation AS SELECT e.*, anchor,
                s.label AS sharer_group, a.label AS author_group
            FROM events e CROSS JOIN boundary b
            LEFT JOIN account_groups s ON e.sharer = s.account
            LEFT JOIN account_groups a ON e.author = a.account
            WHERE e.day = b.day;
            CREATE TEMP TABLE popularity AS SELECT author, count(*) AS total
                FROM train GROUP BY author;
            CREATE TEMP TABLE context_popularity AS SELECT membership, author, count(*) AS total
                FROM train GROUP BY membership, author;
        """)
        if discovery_support:
            # Zero is reserved because the corpus reconciliation accepts positive IDs.
            db.execute("""
                UPDATE validation SET author = 0, author_group = NULL
                WHERE author NOT IN (SELECT author FROM popularity)
            """)
        support = ("SELECT membership, 0 AS author FROM contexts" if discovery_support
                   else "SELECT membership, author FROM validation")
        db.execute(f"""
            CREATE TEMP TABLE risk AS
                WITH contexts AS (SELECT DISTINCT membership FROM validation),
                support AS (
                    SELECT membership, author FROM contexts CROSS JOIN popularity
                    UNION {support}
                )
                SELECT s.*, g.label, coalesce(p.total, 0) AS popularity,
                       coalesce(c.total, 0) AS context_popularity
                FROM support s LEFT JOIN popularity p USING (author)
                LEFT JOIN context_popularity c USING (membership, author)
                LEFT JOIN account_groups g ON s.author = g.account;
            CREATE TEMP TABLE risk_totals AS
                SELECT membership, count(*) AS size,
                       sum(popularity)::BIGINT AS global_total,
                       sum(context_popularity)::BIGINT AS context_total
                FROM risk GROUP BY membership;
            CREATE TEMP TABLE group_totals AS
                SELECT membership, label, count(*) AS size,
                       sum(popularity)::BIGINT AS global_total,
                       sum(context_popularity)::BIGINT AS context_total
                FROM risk WHERE label IS NOT NULL GROUP BY membership, label;
            CREATE TEMP TABLE dyad AS
                SELECT sharer, author, count(*) AS total, sum(recent3) AS recent3,
                       sum(recent1) AS recent1 FROM train GROUP BY sharer, author;
            CREATE TEMP TABLE history AS
                SELECT sharer, count(*) AS total, sum(recent3) AS recent3,
                       sum(recent1) AS recent1,
                       count(*) FILTER (WHERE sharer_group = author_group) AS within_total,
                       sum(recent3) FILTER (WHERE sharer_group = author_group) AS within3,
                       sum(recent1) FILTER (WHERE sharer_group = author_group) AS within1
                FROM train GROUP BY sharer;
        """)
        metadata = "v.sharer, v.author, v.target, v.membership," if evaluation is not None else ""
        assigned_only = "WHERE v.sharer_group IS NOT NULL" if evaluation is not None else ""
        return db.execute(f"""
            SELECT
                {metadata}
                t.size - (s.author IS NOT NULL)::INT AS risk_size,
                t.global_total - coalesce(s.popularity, 0) AS global_total,
                t.context_total - coalesce(s.context_popularity, 0) AS context_total,
                p.popularity AS observed_global, p.context_popularity AS observed_context,
                coalesce(g.size, 0) - coalesce((s.label = v.sharer_group)::INT, 0) AS group_size,
                coalesce(g.global_total, 0) - coalesce(
                    CASE WHEN s.label = v.sharer_group THEN s.popularity END, 0) AS group_global,
                coalesce(g.context_total, 0) - coalesce(
                    CASE WHEN s.label = v.sharer_group THEN s.context_popularity END, 0) AS group_context,
                coalesce(v.sharer_group = v.author_group, false) AS internal,
                v.action_second - v.anchor AS elapsed,
                coalesce(h.total, 0) AS history_total, coalesce(d.total, 0) AS dyad_total,
                coalesce(h.within_total, 0) AS within_total,
                coalesce(h.recent3, 0) AS history3, coalesce(d.recent3, 0) AS dyad3,
                coalesce(h.within3, 0) AS within3,
                coalesce(h.recent1, 0) AS history1, coalesce(d.recent1, 0) AS dyad1,
                coalesce(h.within1, 0) AS within1
            FROM validation v JOIN risk_totals t USING (membership)
            JOIN risk p USING (membership, author)
            LEFT JOIN risk s ON s.membership = v.membership AND s.author = v.sharer
            LEFT JOIN group_totals g ON g.membership = v.membership AND g.label = v.sharer_group
            LEFT JOIN dyad d USING (sharer, author)
            LEFT JOIN history h USING (sharer)
            {assigned_only}
            ORDER BY v.post_id
        """).fetchnumpy()


def context_scores(data, mass):
    uniform = 1 / data["risk_size"]
    global_denominator = data["global_total"] + 1
    context_denominator = data["context_total"] + mass
    global_probability = (data["observed_global"] + uniform) / global_denominator
    global_group = (data["group_global"] + data["group_size"] * uniform) / global_denominator
    return (
        (data["observed_context"] + mass * global_probability) / context_denominator,
        (data["group_context"] + mass * global_group) / context_denominator,
    )


def history_scores(data, context, mass, half_life):
    suffix = "_total" if half_life is None else str(half_life)
    scale = 1 if half_life is None else np.exp2(-data["elapsed"] / (86400 * half_life))
    denominator = data["history" + suffix] * scale + mass
    return (
        (data["dyad" + suffix] * scale + mass * context[0]) / denominator,
        (data["within" + suffix] * scale + mass * context[1]) / denominator,
    )


def calibrate(folds):
    def context_score(mass):
        return float(sum(np.log(context_scores(data, mass)[0]).sum() for data, _ in folds))

    context_results = [(mass, context_score(mass)) for mass in MASSES]
    context_mass = max(context_results, key=lambda item: item[1])[0]
    contexts = [context_scores(data, context_mass) for data, _ in folds]
    history_results = [
        (mass, half_life, float(sum(
            np.log(history_scores(data, context, mass, half_life)[0]).sum()
            for (data, _), context in zip(folds, contexts)
        )))
        for mass in MASSES for half_life in HALF_LIVES
    ]
    dyad_mass, half_life, _ = max(history_results, key=lambda item: item[2])
    selected_data = [
        (data, history_scores(data, context, dyad_mass, half_life))
        for (data, eligible), context in zip(folds, contexts) if eligible
    ]
    beta_results = [
        (beta, float(sum(
            (beta * data["internal"] - np.log1p(np.expm1(beta) * group)).sum()
            for data, (_, group) in selected_data
        ))) for beta in BETAS
    ]
    beta = max(beta_results, key=lambda item: item[1])[0]
    return dict(context_mass=context_mass, dyad_mass=dyad_mass, half_life_days=half_life,
                beta=beta, membership_calibrated=bool(selected_data),
                context_log_scores=context_results, history_log_scores=history_results,
                beta_log_score_gains=beta_results,
                fold_actions=[len(data["risk_size"]) for data, _ in folds])


def selected_partition(directory):
    selected = json.loads((directory / "grid.json").read_text())["selected"]
    if selected is None:
        return None
    return (np.load(directory / "accounts.npy"),
            np.load(directory / f"{selected['resolution']}-{selected['seed']}.npy"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("fold_grids", type=Path, nargs=2)
    args = parser.parse_args()
    folds = []
    for day, directory in zip(FOLD_DAYS, args.fold_grids):
        partition = selected_partition(directory)
        folds.append((load_fold(args.ledger, day, partition), partition is not None))
    print(json.dumps(calibrate(folds), indent=2))
