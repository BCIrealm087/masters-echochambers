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


def draw(binary, payload, count, seed, proposal_limit):
    proc = subprocess.run([str(binary.resolve()), str(count), str(seed), str(proposal_limit)],
                          input=payload, capture_output=True)
    if proc.returncode == 4:
        raise RuntimeError(f"Proposal budget exhausted at seed {seed} after "
                           f"{proc.stderr.decode().strip()} proposals")
    proc.check_returncode()
    scores = [int(line) for line in proc.stdout.splitlines()]
    proposals = int(proc.stderr)
    if len(scores) != count or not count <= proposals <= proposal_limit:
        raise ValueError("Invalid scorer output")
    return scores, proposals


def atomic_json(path, value):
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temp.replace(path)


def score_batch(binary, output, key, payload, slots, batch, count, seed, limit):
    path = output / f"{key}-{batch:04d}.json"
    if path.exists():
        prior = json.loads(path.read_text())
        scores, proposals = prior["scores"], prior["proposals"]
        if (prior["seed"] != seed or len(scores) != count or
                not count <= proposals <= limit or
                not all(isinstance(score, int) and 0 <= score <= slots for score in scores)):
            raise ValueError(f"Invalid saved batch {path}")
        return prior
    start = perf_counter()
    scores, proposals = draw(binary, payload, count, seed, limit)
    result = dict(seed=seed, scores=scores, proposals=proposals, seconds=perf_counter()-start)
    atomic_json(path, result)
    return result


def load_strata(ledger, accounts, labels):
    with duckdb.connect(config={"threads": 4}) as db:
        scope = db.execute("SELECT DISTINCT day FROM read_parquet(?)", [str(ledger)]).fetchall()
        if set(scope) != {(date(2022, 10, day),) for day in (16, 17, 18)}:
            raise ValueError("This scorer is restricted to the discovery dates")
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
        for day, context in db.execute(
            "SELECT DISTINCT day, membership FROM eligible ORDER BY 1, 2"
        ).fetchall():
            data = db.execute("""
                SELECT sharer, action_second, author, original_second, sharer_group, author_group,
                       target
                FROM eligible WHERE day = ? AND membership = ? ORDER BY action_second, post_id
            """, [day, context]).fetchnumpy()
            yield str(day), context, data


def run(args):
    args.output.mkdir(mode=0o700, parents=True, exist_ok=True)
    with (args.output / "lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return score(args)


def score(args):
    config = dict(ledger_sha256=digest(args.ledger), accounts_sha256=digest(args.accounts),
                  membership_sha256=digest(args.membership), binary_sha256=digest(args.binary),
                  driver_sha256=digest(Path(__file__)), draws=args.draws, batch_size=args.batch_size,
                  seed=args.seed, proposals_per_draw=args.proposals_per_draw)
    state = args.output / "config.json"
    if state.exists():
        if json.loads(state.read_text()) != config:
            raise ValueError("Saved batches belong to different inputs or scoring settings")
    else:
        atomic_json(state, config)
    accounts, labels = np.load(args.accounts), np.load(args.membership)
    jobs = {}
    strata = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for index, (day, context, data) in enumerate(load_strata(args.ledger, accounts, labels)):
            shards = jobs[index] = []
            payload = pack(*(data[column] for column in SCORE_COLUMNS))
            slots = len(data["sharer"])
            observed = int(np.count_nonzero(data["sharer_group"] == data["author_group"]))
            strata.append(dict(day=day, context=context, slots=slots, observed_internal=observed))
            for batch, offset in enumerate(range(0, args.draws, args.batch_size)):
                count = min(args.batch_size, args.draws - offset)
                seed = int.from_bytes(sha256(f"{args.seed}:{index}:{batch}".encode()).digest()[:8],
                                      "little")
                shards.append(pool.submit(score_batch, args.binary, args.output, str(index),
                                          payload, slots, batch, count, seed,
                                          count * args.proposals_per_draw))
        combined = np.zeros(args.draws, dtype=np.int64)
        for index, stratum in enumerate(strata):
            batches = [job.result() for job in jobs[index]]
            scores = np.concatenate([batch["scores"] for batch in batches])
            combined += scores
            stratum.update(reference_mean_internal=float(scores.mean()),
                           proposals=sum(batch["proposals"] for batch in batches))
    total = sum(row["slots"] for row in strata)
    observed = sum(row["observed_internal"] for row in strata)
    return dict(draws=args.draws, slots=total, strata=strata, observed_share=observed/total,
                expected_share=float(combined.mean()/total),
                excess_percentage_points=float(100*(observed-combined.mean())/total),
                central_95_reference_share=(np.quantile(combined, [.025, .975])/total).tolist(),
                plus_one_upper_p=float((1+np.count_nonzero(combined >= observed))/(args.draws+1)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("ledger", "accounts", "membership", "binary", "output"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--draws", type=int, default=9999)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20261127)
    parser.add_argument("--proposals-per-draw", type=int, default=10000)
    args = parser.parse_args()
    if min(args.draws, args.batch_size, args.workers, args.proposals_per_draw) < 1:
        parser.error("Draws, batch size, workers and proposal budget must be positive")
    result = run(args)
    print(json.dumps(result, indent=2, allow_nan=False))
