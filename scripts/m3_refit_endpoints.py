"""Fit resumable registered Leiden grids on missing-author scenarios."""
import argparse
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import fcntl
from importlib.metadata import version
import json
import multiprocessing as mp
from pathlib import Path

import numpy as np

from m3_discovery import RESOLUTIONS, SEEDS, fit, write_graph_grid
from m3_reference_score import atomic_json, digest

_GRAPH = None


def stored_labels(path):
    return np.load(path, allow_pickle=False)


def fit_one(task):
    resolution, seed, directory = task
    path = directory / f"{resolution}-{seed}.npy"
    if path.exists():
        labels = stored_labels(path)
        if labels.shape != (_GRAPH.vcount(),) or labels.dtype != np.int32:
            raise ValueError(f"Invalid membership checkpoint: {path}")
    else:
        labels = fit("leiden", _GRAPH, resolution, seed)
        temporary = path.with_suffix(".tmp")
        with temporary.open("wb") as stream:
            np.save(stream, labels, allow_pickle=False)
        temporary.replace(path)
    return resolution, seed


def prepare_labels(graph, graph_hash, directory, *, workers):
    global _GRAPH
    _GRAPH = graph
    config = {
        "graph_sha256": graph_hash, "resolutions": RESOLUTIONS, "seeds": list(SEEDS),
        "method": "directed weighted RB Leiden until convergence",
        "software": {package: version(package) for package in ("igraph", "leidenalg", "numpy")},
        "fit_source_sha256": digest(Path(__file__).with_name("m3_discovery.py")),
        "refit_driver_sha256": digest(Path(__file__)),
    }
    config_path = directory / "fit-config.json"
    if config_path.exists():
        if json.loads(config_path.read_text()) != json.loads(json.dumps(config)):
            raise ValueError(f"Refit checkpoint belongs to different inputs: {directory}")
    else:
        atomic_json(config_path, config)
    tasks = [(res, seed, directory) for res in RESOLUTIONS for seed in SEEDS]
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("fork")) as pool:
        for resolution, seed in pool.map(fit_one, tasks):
            print(f"Completed resolution {resolution}, seed {seed}", flush=True)
    _GRAPH = None
    return stored_labels


def refit(ledger, directory, workers):
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    with (directory / "lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return write_graph_grid(ledger, directory, "leiden",
                                prepare_labels=partial(prepare_labels, workers=workers))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be positive")
    result = refit(args.ledger, args.directory, args.workers)
    print(json.dumps(result["selected"], indent=2))
