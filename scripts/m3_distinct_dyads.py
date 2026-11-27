"""Stream accepted assignments into a whole-window distinct-dyad statistic."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import fcntl
from hashlib import sha256
import json
from pathlib import Path
import subprocess

import numpy as np

from m3_reference_score import (DISCOVERY_DAYS, atomic_json, digest, load_strata, pack)


def distinct_counts(sources, destinations, groups):
    width = len(groups)
    edges = np.unique(sources * np.uint64(width) + destinations)
    sharer_group = groups[edges // width]
    author_group = groups[edges % width]
    return len(edges), int(np.count_nonzero((sharer_group != 0) & (sharer_group == author_group)))


def sample(binary, payload, seed, slots, cap):
    result = subprocess.run([str(binary.resolve()), "1", str(seed), str(cap), "--assignments"],
                            input=payload, capture_output=True)
    if result.returncode == 4:
        raise RuntimeError(f"Distinct-dyad draw exhausted the proposal cap at seed {seed}")
    result.check_returncode()
    values = np.frombuffer(result.stdout, dtype="<u8")
    if len(values) != slots:
        raise ValueError("Assignment length differs from the action margins")
    return values


def score(binary, ledger, accounts_path, labels_path, output, *, draws, workers, seed,
          days=DISCOVERY_DAYS, cap=10000):
    output.mkdir(mode=0o700, parents=True, exist_ok=True)
    with (output / "lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        config = dict(ledger=digest(ledger), accounts=digest(accounts_path), labels=digest(labels_path),
                      binary=digest(binary), driver=digest(Path(__file__)),
                      seed=seed, cap=cap, days=list(map(str, days)))
        path = output / "config.json"
        if path.exists() and json.loads(path.read_text()) != config:
            raise ValueError("Saved draws use a different input or RNG configuration")
        atomic_json(path, config)
        accounts, labels = np.load(accounts_path), np.load(labels_path)
        strata = list(load_strata(ledger, accounts, labels, days=days))
        if not strata:
            raise ValueError("No eligible slots")
        universe = np.unique(np.concatenate([accounts, *[d["author"] for _, _, d in strata]]))
        groups = np.zeros(len(universe), dtype=np.uint64)
        groups[universe.searchsorted(accounts)] = labels.astype(np.uint64) + 1
        if len(universe) ** 2 > np.iinfo(np.uint64).max:
            raise ValueError("Too many accounts for exact dense pair encoding")
        sizes, payloads, sources, destinations = [], [], [], []
        for _, _, data in strata:
            s = universe.searchsorted(data["sharer"]).astype(np.uint64)
            a = universe.searchsorted(data["author"]).astype(np.uint64)
            sizes.append(len(s))
            sources.append(s)
            destinations.append(a)
            payloads.append(pack(s, data["action_second"], a, data["original_second"],
                                 groups[s], groups[a]))
        source = np.concatenate(sources)
        observed_total, observed_internal = distinct_counts(source, np.concatenate(destinations),
                                                             groups)

        def one(index):
            checkpoint = output / f"draw-{index:05d}.json"
            if checkpoint.exists():
                total, internal = json.loads(checkpoint.read_text())
                if not 0 <= internal <= total <= len(source) or not total:
                    raise ValueError(f"Invalid saved draw {checkpoint}")
            else:
                values = []
                for stratum, (payload, slots) in enumerate(zip(payloads, sizes)):
                    key = sha256(f"dyad:{seed}:{index}:{stratum}".encode()).digest()
                    values.append(sample(binary, payload, int.from_bytes(key[:8], "little"),
                                         slots, cap))
                total, internal = distinct_counts(source, np.concatenate(values), groups)
                atomic_json(checkpoint, [total, internal])
            return internal / total

        with ThreadPoolExecutor(max_workers=workers) as pool:
            reference = np.array(list(pool.map(one, range(draws))))
    observed = observed_internal / observed_total
    return dict(draws=draws, observed_distinct_dyads=observed_total, observed_share=observed,
                expected_share=float(reference.mean()),
                excess_percentage_points=float(100*(observed-reference.mean())),
                central_95_reference_share=np.quantile(reference, [.025, .975]).tolist(),
                plus_one_upper_p=float((1+np.count_nonzero(reference >= observed))/(draws+1)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("ledger", "accounts", "membership", "binary", "output"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--draws", type=int, default=64)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20261127)
    args = parser.parse_args()
    if min(args.draws, args.workers) < 1:
        parser.error("Draw and worker counts must be positive")
    print(json.dumps(score(args.binary, args.ledger, args.accounts, args.membership, args.output,
                           draws=args.draws, workers=args.workers, seed=args.seed), indent=2))
