"""Score the exact matched-post reference on discovery-only inputs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import fcntl
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from time import perf_counter

import duckdb
import numpy as np

SCORE_COLUMNS = ("sharer", "action_second", "author", "original_second",
                 "sharer_group", "author_group")
DISCOVERY_DAYS = tuple(date(2022, 10, day) for day in (16, 17, 18))
HOLDOUT_DAYS = tuple(date(2022, 10, day) for day in (19, 20, 21))


def digest(path):
    result = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def pack(sharers, actions, authors, originals, sharer_groups, author_groups):
    order = np.argsort(originals, kind="stable")
    values = (len(actions), sharers, actions, authors[order], originals[order],
              sharer_groups, author_groups[order])
    return b"".join(np.asarray(value, dtype="<u8").tobytes() for value in values)


def draw(binary, payload, count, seed, proposal_limit, group_count=None):
    command = [str(binary.resolve()), str(count), str(seed), str(proposal_limit)]
    if group_count is not None:
        command.append(str(group_count))
    proc = subprocess.run(command,
                          input=payload, capture_output=True)
    if proc.returncode == 4:
        raise RuntimeError(f"Proposal budget exhausted at seed {seed} after "
                           f"{proc.stderr.decode().strip()} proposals")
    proc.check_returncode()
    scores = ([int(line) for line in proc.stdout.splitlines()] if group_count is None
              else [[int(fields[0]), float(fields[1]), *map(int, fields[2:])]
                    for line in proc.stdout.splitlines() if (fields := line.split())])
    proposals = int(proc.stderr)
    if len(scores) != count or not count <= proposals <= proposal_limit:
        raise ValueError("Invalid scorer output")
    return scores, proposals


def atomic_json(path, value):
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temp.replace(path)


def score_batch(binary, output, key, payload, slots, batch, count, seed, limit, group_count):
    path = output / f"{key}-{batch:04d}.json"
    if path.exists():
        prior = json.loads(path.read_text())
        scores, proposals = prior["scores"], prior["proposals"]
        if (prior["seed"] != seed or len(scores) != count or
                not count <= proposals <= limit or
                not all(valid_score(score, slots, group_count) for score in scores)):
            raise ValueError(f"Invalid saved batch {path}")
        return prior
    start = perf_counter()
    scores, proposals = draw(binary, payload, count, seed, limit, group_count)
    if not all(valid_score(score, slots, group_count) for score in scores):
        raise ValueError("Invalid score values from compiled scorer")
    result = dict(seed=seed, scores=scores, proposals=proposals, seconds=perf_counter()-start)
    atomic_json(path, result)
    return result


def valid_score(score, slots, group_count):
    if group_count is None:
        return isinstance(score, int) and 0 <= score <= slots
    return (isinstance(score, list) and len(score) == group_count + 2
            and isinstance(score[0], int) and 0 <= score[0] <= slots
            and 0 <= score[1] <= score[0] and all(
                isinstance(value, int) and 0 <= value <= score[0] for value in score[2:]
            ) and sum(score[2:]) <= score[0])


def secondary_margins(inputs, accounts, labels):
    activity = np.zeros(len(accounts), dtype=np.int64)
    for _, _, data in inputs:
        indices = accounts.searchsorted(data["sharer"])
        activity += np.bincount(indices, minlength=len(accounts))
    action_counts = np.bincount(labels, weights=activity).astype(np.int64)
    sharer_counts = np.bincount(labels, weights=activity > 0).astype(np.int64)
    codes = np.flatnonzero((action_counts >= 100) & (sharer_counts >= 20))
    mapping = np.zeros(len(action_counts) + 1, dtype=np.uint64)
    mapping[codes + 1] = np.arange(1, len(codes) + 1)
    return activity, action_counts, sharer_counts, codes, mapping


def holm(p_values):
    order = np.argsort(p_values, kind="stable")
    adjusted = np.empty(len(order))
    adjusted[order] = np.minimum(1, np.maximum.accumulate(
        np.asarray(p_values)[order] * np.arange(len(order), 0, -1)
    ))
    return adjusted


def load_strata(ledger, accounts, labels, *, days=DISCOVERY_DAYS, stratify="day-context",
                exclude=None):
    with duckdb.connect(config={"threads": 4}) as db:
        scope = db.execute("SELECT DISTINCT day FROM read_parquet(?)", [str(ledger)]).fetchall()
        if set(scope) != {(day,) for day in days}:
            raise ValueError("Ledger dates differ from the requested evaluation interval")
        db.register("groups", {"account": accounts, "label": labels.astype(np.uint64) + 1})
        db.execute("""
            CREATE TEMP TABLE eligible AS
            SELECT e.day, e.membership, e.post_id, e.target, e.sharer, e.author,
                   e.action_second, e.original_second, g.label AS sharer_group,
                   coalesce(a.label, 0) AS author_group
            FROM read_parquet(?) e JOIN groups g ON e.sharer = g.account
            LEFT JOIN groups a ON e.author = a.account
            WHERE e.sharer <> e.author AND e.membership <> 'unknown'
        """, [str(ledger)])
        bad = db.execute("""
            SELECT count(*) FROM eligible
            WHERE target IS NULL OR action_second IS NULL OR original_second IS NULL
               OR original_second > action_second
        """).fetchone()[0]
        if bad:
            raise ValueError(f"{bad} observed pairings lack a valid post time")
        if exclude is not None:
            field, top = exclude
            if field not in ("author", "target") or top not in ("1", "5", "1%"):
                raise ValueError("Invalid concentration exclusion")
            cutoff = "ceil(count(*) OVER () / 100.0)" if top == "1%" else top
            db.execute(f"""
                DELETE FROM eligible WHERE {field} IN (
                    SELECT {field} FROM eligible GROUP BY {field}
                    QUALIFY row_number() OVER (ORDER BY count(*) DESC, {field}) <= {cutoff}
                )
            """)
        if stratify not in ("day-context", "day", "pooled"):
            raise ValueError("Unknown reference strata")
        date_expr = "cast(day AS VARCHAR)" if stratify != "pooled" else "'all'"
        context_expr = "membership" if stratify == "day-context" else "'all'"
        for day, context in db.execute(f"""
            SELECT DISTINCT {date_expr}, {context_expr} FROM eligible ORDER BY 1, 2
        """).fetchall():
            data = db.execute(f"""
                SELECT sharer, action_second, author, original_second, sharer_group, author_group,
                       target
                FROM eligible WHERE {date_expr} = ? AND {context_expr} = ?
                ORDER BY action_second, post_id
            """, [day, context]).fetchnumpy()
            yield str(day), context, data


def run(args):
    args.output.mkdir(mode=0o700, parents=True, exist_ok=True)
    with (args.output / "lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return score(args)


def score(args):
    days = getattr(args, "days", DISCOVERY_DAYS)
    stratify = getattr(args, "stratify", "day-context")
    exclude = getattr(args, "exclude", None)
    secondary = getattr(args, "secondary", False)
    config = dict(ledger_sha256=digest(args.ledger), accounts_sha256=digest(args.accounts),
                  membership_sha256=digest(args.membership), binary_sha256=digest(args.binary),
                  driver_sha256=digest(Path(__file__)), draws=args.draws, batch_size=args.batch_size,
                  seed=args.seed, proposals_per_draw=args.proposals_per_draw)
    config.update(days=[str(day) for day in days], stratify=stratify,
                  exclude=list(exclude) if exclude else None, secondary=secondary)
    state = args.output / "config.json"
    if state.exists():
        if json.loads(state.read_text()) != config:
            raise ValueError("Saved batches belong to different inputs or scoring settings")
    else:
        atomic_json(state, config)
    accounts, labels = np.load(args.accounts), np.load(args.membership)
    jobs = {}
    strata = []
    stratum_scores = []
    secondary_scores = []
    source = load_strata(args.ledger, accounts, labels, days=days, stratify=stratify,
                         exclude=exclude)
    group_count = None
    if secondary:
        source = list(source)
        activity, action_counts, sharer_counts, codes, mapping = secondary_margins(
            source, accounts, labels)
        group_count = len(codes)
        observed_group = np.zeros(group_count + 1, dtype=np.int64)
        observed_weight = 0.0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for index, (day, context, data) in enumerate(source):
            shards = jobs[index] = []
            payload = pack(*(data[column] for column in SCORE_COLUMNS))
            slots = len(data["sharer"])
            internal = data["sharer_group"] == data["author_group"]
            observed = int(np.count_nonzero(internal))
            if secondary:
                weights = 1.0 / activity[accounts.searchsorted(data["sharer"])]
                indices = mapping[data["sharer_group"]]
                payload += weights.astype("<f8").tobytes() + indices.astype("<u8").tobytes()
                observed_weight += weights[internal].sum()
                observed_group += np.bincount(
                    indices[internal].astype(np.int64), minlength=group_count + 1)
            strata.append(dict(day=day, context=context, slots=slots, observed_internal=observed))
            for batch, offset in enumerate(range(0, args.draws, args.batch_size)):
                count = min(args.batch_size, args.draws - offset)
                seed = int.from_bytes(sha256(f"{args.seed}:{index}:{batch}".encode()).digest()[:8],
                                      "little")
                shards.append(pool.submit(score_batch, args.binary, args.output, str(index),
                                          payload, slots, batch, count, seed,
                                          count * args.proposals_per_draw, group_count))
        for index, stratum in enumerate(strata):
            batches = [job.result() for job in jobs[index]]
            scores = np.concatenate([batch["scores"] for batch in batches])
            if secondary:
                secondary_scores.append(scores[:, 1:])
                scores = scores[:, 0].astype(np.int64)
            stratum_scores.append(scores)
            stratum.update(reference_mean_internal=float(scores.mean()),
                           proposals=sum(batch["proposals"] for batch in batches))
    if not strata:
        raise ValueError("No eligible actions")
    def contrast(indices):
        selected = [strata[index] for index in indices]
        return summarize(selected, np.sum([stratum_scores[index] for index in indices], axis=0))

    result = dict(draws=args.draws, strata=strata, **contrast(list(range(len(strata)))))
    if secondary:
        combined = np.sum(secondary_scores, axis=0)
        result["equal_sharer"] = summarize(
            [{"slots": int(np.count_nonzero(activity)), "observed_internal": observed_weight}],
            combined[:, 0], tie_tolerance=1e-9)
        comparisons = [
            summarize([{"slots": int(action_counts[code]), "observed_internal": observed_group[i+1]}],
                      combined[:, i+1])
            for i, code in enumerate(codes)
        ]
        adjusted = holm([row["plus_one_upper_p"] for row in comparisons])
        lookup = dict(zip(codes, comparisons))
        for row, value in zip(comparisons, adjusted):
            row["holm_adjusted_p"] = float(value)
        result["groups"] = [
            dict(group=code, eligible_actions=int(actions), distinct_sharers=int(sharer_counts[code]),
                 disposition="tested" if code in lookup else "below_margins",
                 **lookup.get(code, {}))
            for code, actions in enumerate(action_counts)
        ]
    if stratify == "day-context":
        result["per_context"] = {
            context: contrast([i for i, row in enumerate(strata) if row["context"] == context])
            for context in sorted({row["context"] for row in strata})
        }
        if len({row["day"] for row in strata}) > 1:
            result["leave_one_day_out"] = {
                day: contrast([i for i, row in enumerate(strata) if row["day"] != day])
                for day in sorted({row["day"] for row in strata})
            }
    return result


def summarize(strata, combined, tie_tolerance=0):
    total = sum(row["slots"] for row in strata)
    observed = sum(row["observed_internal"] for row in strata)
    excess = float(100*(observed-combined.mean())/total)
    return dict(slots=total, observed_share=observed/total,
                expected_share=float(combined.mean()/total),
                excess_percentage_points=excess,
                practical_screens={str(threshold): excess >= threshold
                                   for threshold in (2.5, 5, 10, 20)},
                central_95_reference_share=(np.quantile(combined, [.025, .975])/total).tolist(),
                plus_one_upper_p=float(
                    (1+np.count_nonzero(combined >= observed-tie_tolerance))/(len(combined)+1)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("ledger", "accounts", "membership", "binary", "output"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--draws", type=int, default=9999)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20261127)
    parser.add_argument("--proposals-per-draw", type=int, default=10000)
    parser.add_argument("--secondary", action="store_true")
    args = parser.parse_args()
    if min(args.draws, args.batch_size, args.workers, args.proposals_per_draw) < 1:
        parser.error("Draws, batch size, workers and proposal budget must be positive")
    result = run(args)
    print(json.dumps(result, indent=2, allow_nan=False))
