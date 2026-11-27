"""Prepare M3 holdout inputs and explicitly invoke frozen primary evaluations."""
import argparse
from datetime import date
import json
from pathlib import Path
from types import SimpleNamespace

import duckdb
import numpy as np

from m2_repost_coverage import HOLDOUT_START, reconcile
from m3_calibrate import context_scores, history_scores, load_fold
from m3_reference_score import HOLDOUT_DAYS, atomic_json, digest, run

REPOSITORY = Path(__file__).resolve().parent.parent
REPORTS = REPOSITORY / "docs" / "reports"


def verify_frozen(discovery, accounts, membership):
    freeze = json.loads((REPORTS / "m3-discovery-freeze.json").read_text())
    primary = freeze["grids"]["leiden-weighted"]
    for path, expected in (
        (discovery, freeze["ledger"]["discovery_ledger_sha256"]),
        (accounts, primary["accounts_sha256"]),
        (membership, primary["partition_sha256"]),
    ):
        if digest(path) != expected:
            raise ValueError(f"Frozen input fingerprint mismatch: {path}")
    return freeze["prediction_calibration"]


def margins(db, accounts):
    """Compute eligibility and legality without using any agreement between labels."""
    db.register("assigned_accounts", {"account": accounts})
    return [
        dict(zip(("day", "context", "actions", "resolved_authors", "known_sharers",
                  "assigned_sharers", "unassigned_sharers", "self_reposts",
                  "eligible", "external_authors", "missing_authors_assigned",
                  "illegal_time_or_reference", "same_second", "repeat_sharer_post_actions"), row))
        for row in db.execute("""
            WITH exact AS (
                SELECT e.*, s.account IS NOT NULL AS assigned,
                       a.account IS NULL AS external,
                       s.account IS NOT NULL AND e.sharer <> e.author
                           AND membership <> 'unknown' AS eligible
                FROM evaluation_ledger e
                LEFT JOIN assigned_accounts s ON e.sharer = s.account
                LEFT JOIN assigned_accounts a ON e.author = a.account
            )
            SELECT cast(day AS VARCHAR), membership, count(*), count(author), count(sharer),
                   count(*) FILTER (WHERE assigned),
                   count(*) FILTER (WHERE sharer IS NOT NULL AND NOT assigned),
                   count(*) FILTER (WHERE sharer = author),
                   count(*) FILTER (WHERE eligible),
                   count(*) FILTER (WHERE eligible AND external),
                   count(*) FILTER (WHERE assigned AND author IS NULL
                                           AND membership <> 'unknown'),
                   count(*) FILTER (WHERE eligible AND (target IS NULL OR
                           original_second IS NULL OR action_second IS NULL OR
                           original_second > action_second)),
                   count(*) FILTER (WHERE eligible AND original_second = action_second),
                   count(*) FILTER (WHERE eligible)
                       - count(DISTINCT (sharer, target)) FILTER (WHERE eligible)
            FROM exact GROUP BY 1, 2 ORDER BY 1, 2
        """).fetchall()
    ]


def compare_m2(counts):
    source = json.loads((REPORTS / "m2-repost-coverage.json").read_text())
    expected = {(row["day"], row["membership"]): row for row in source["coverage"]
                if row["interval"] == "holdout" and row["day"] and row["membership"]}
    if {(row["day"], row["context"]) for row in counts} != expected.keys():
        raise ValueError("Holdout strata differ from the archived M2 audit")
    for row in counts:
        prior = expected[row["day"], row["context"]]
        if (row["actions"], row["resolved_authors"], row["known_sharers"]) != (
                prior["reposts"], prior["unique_author"], prior["usable_sharers"]):
            raise ValueError("Holdout action or endpoint totals differ from M2")


def group_margins(db, accounts, membership):
    db.register("frozen_groups", {"account": accounts, "group_id": membership})
    return [
        dict(group=group, eligible_actions=actions, distinct_sharers=sharers,
             holm_eligible=actions >= 100 and sharers >= 20)
        for group, actions, sharers in db.execute("""
            WITH eligible AS (
                SELECT g.group_id, count(*) AS actions, count(DISTINCT e.sharer) AS sharers
                FROM evaluation_ledger e JOIN frozen_groups g ON e.sharer = g.account
                WHERE e.sharer <> e.author AND e.membership <> 'unknown'
                GROUP BY g.group_id
            )
            SELECT m.group_id, coalesce(e.actions, 0), coalesce(e.sharers, 0)
            FROM (SELECT DISTINCT group_id FROM frozen_groups) m
            LEFT JOIN eligible e USING (group_id) ORDER BY m.group_id
        """).fetchall()
    ]


def prepare(root, snapshot, output, accounts, membership):
    frozen_footer = json.loads((REPORTS / "m3-discovery-freeze.json").read_text())[
        "source_footer_inventory_sha256"]
    if json.loads(snapshot.read_text())["footer_inventory_sha256"] != frozen_footer:
        raise ValueError("Corpus footer fingerprint differs from the discovery freeze")
    output.mkdir(mode=0o700, parents=True, exist_ok=True)
    ledger = output / "holdout.parquet"
    temp = output / "holdout.tmp"
    with duckdb.connect(config={
        "threads": 4, "memory_limit": "8GB", "preserve_insertion_order": False,
        "temp_directory": str(output.resolve()),
    }) as db:
        reconcile(db, root.resolve())
        db.execute("""
            CREATE TEMP VIEW evaluation_ledger AS
            SELECT post_id, day, membership, sharer, target, resolution,
                   CASE WHEN resolution = 'unique author' THEN first_author END AS author,
                   ((post_id >> 22) + 1288834974657) // 1000 AS action_second,
                   ((target >> 22) + 1288834974657) // 1000 AS original_second
            FROM coverage LEFT JOIN historical USING (target)
            WHERE interval = 'holdout'
        """)
        counts = margins(db, accounts)
        compare_m2(counts)
        if any(row["illegal_time_or_reference"] for row in counts):
            raise ValueError("Ineligible observed original-post pairing in holdout")
        groups = group_margins(db, accounts, membership)
        if sum(group["eligible_actions"] for group in groups) != sum(
                row["eligible"] for row in counts):
            raise ValueError("Group margins do not reconcile with the primary population")
        db.execute("""
            COPY (SELECT * FROM evaluation_ledger ORDER BY post_id)
            TO ? (FORMAT PARQUET, COMPRESSION ZSTD)
        """, [str(temp)])
    temp.replace(ledger)
    return dict(ledger_sha256=digest(ledger), source_footer_inventory_sha256=frozen_footer,
                counts=counts, group_margins=groups, software={"duckdb": duckdb.__version__})


def score_prediction(data, settings):
    mass = settings["context_mass"]
    context = context_scores(data, mass)
    history, within = history_scores(data, context, settings["dyad_mass"],
                                     settings["half_life_days"])
    beta = settings["beta"]
    gain = beta * data["internal"] - np.log1p(np.expm1(beta) * within)
    popularity = ((data["observed_global"] + 1/data["risk_size"]) /
                  (data["global_total"] + 1))
    scores = np.stack((np.log(popularity), np.log(context[0]), np.log(history),
                       np.log(history) + gain))
    return scores, gain


def summarize_prediction(scores, gain, sharers, selected):
    n = int(selected.sum())
    if not n:
        return {"actions": 0}
    values = gain[selected]
    unique, inverse = np.unique(sharers[selected], return_inverse=True)
    center = values.mean()
    residual_sums = np.bincount(inverse, weights=values-center)
    clusters = len(unique)
    error = (float(np.sqrt(np.sum(residual_sums**2) * clusters/(clusters-1))/n)
             if clusters > 1 else None)
    return {
        "actions": n, "sharers": clusters,
        "mean_log_scores": dict(zip(("popularity", "context", "history", "group"),
                                    scores[:, selected].mean(axis=1).tolist())),
        "paired_gain_nats": float(center),
        "sharer_clustered_standard_error": error,
        "normal_95_interval": [float(center-1.96*error), float(center+1.96*error)]
            if error is not None else None,
    }


def prediction(discovery, evaluation, membership, settings, days=HOLDOUT_DAYS,
               training_end=HOLDOUT_START):
    result = {}
    for mode in ("conditional", "discovery-support"):
        buffers = []
        for day in days:
            data = load_fold(discovery, str(day), membership, evaluation=evaluation,
                             training_end=training_end, discovery_support=mode != "conditional")
            scores, gain = score_prediction(data, settings)
            n = len(gain)
            buffers.append({
                "day": np.full(n, day.day, dtype=np.uint8),
                "scores": scores, "gain": gain, "sharer": data["sharer"],
                "seen_dyad": data["dyad_total"] > 0,
                "author": data["author"], "target": data["target"],
                "context": data["membership"],
            })
        joined = {key: np.concatenate([buffer[key] for buffer in buffers],
                                     axis=1 if key == "scores" else 0)
                  for key in buffers[0]}
        def summarize(mask):
            return summarize_prediction(joined["scores"], joined["gain"], joined["sharer"], mask)

        strata = {"all": summarize(np.ones(len(joined["gain"]), dtype=bool))}
        for key in ("day", "context", "seen_dyad"):
            strata[key] = {str(value): summarize(joined[key] == value)
                           for value in np.unique(joined[key])}
        if mode == "conditional":
            for dimension in ("author", "target"):
                ids, counts = np.unique(joined[dimension], return_counts=True)
                order = np.lexsort((ids, -counts))
                strata[dimension + "_concentration"] = {
                    name: summarize(~np.isin(joined[dimension], ids[order[:cutoff]]))
                    for name, cutoff in (("top-1", 1), ("top-5", 5),
                                         ("top-1pct", (len(ids)+99)//100))
                }
        result[mode] = strata
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("prepare-margins", "primary-reference", "prediction"))
    for name in ("discovery", "accounts", "membership", "work"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--binary", type=Path)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--stratify", choices=("day-context", "day", "pooled"),
                        default="day-context")
    parser.add_argument("--exclude", nargs=2, metavar=("FIELD", "TOP"))
    args = parser.parse_args()
    settings = verify_frozen(args.discovery, args.accounts, args.membership)
    if args.stage == "prepare-margins":
        if args.root is None or args.snapshot is None:
            parser.error("prepare-margins requires --root and --snapshot")
        result = prepare(args.root, args.snapshot, args.work, np.load(args.accounts),
                         np.load(args.membership))
        atomic_json(args.work / "margins.json", result)
    else:
        ledger = args.work / "holdout.parquet"
        marker = json.loads((args.work / "margins.json").read_text())
        if digest(ledger) != marker["ledger_sha256"]:
            raise ValueError("Prepared holdout ledger fingerprint mismatch")
        if args.stage == "prediction":
            result = prediction(args.discovery, ledger, (np.load(args.accounts),
                                np.load(args.membership)), settings)
        else:
            if args.binary is None or args.workers < 1:
                parser.error("primary-reference requires --binary and a positive worker count")
            if args.exclude and (args.exclude[0] not in ("author", "target")
                                 or args.exclude[1] not in ("1", "5", "1%")):
                parser.error("--exclude takes author or target followed by 1, 5, or 1%")
            suffix = "-".join(args.exclude or ())
            result = run(SimpleNamespace(ledger=ledger, accounts=args.accounts,
                         membership=args.membership, binary=args.binary,
                         output=args.work / f"reference-{args.stratify}-{suffix}",
                         days=HOLDOUT_DAYS, stratify=args.stratify, exclude=args.exclude,
                         draws=9999, batch_size=64, workers=args.workers, seed=20261127,
                         proposals_per_draw=10000))
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
