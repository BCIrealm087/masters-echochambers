"""Verify discovery artifacts and print a shareable manifest with hashes and aggregates."""
import argparse
from collections import Counter
from hashlib import sha256
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform

import numpy as np

from m3_discovery import RESOLUTIONS, SEEDS, diagnostics, graph_from_ledger
from m3_prediction import verify_prediction
from m3_reference import verify_reference
from m3_calibrate import selected_partition

GRID_NAMES = ("leiden-weighted", "leiden-binary", "leiden-fold-17", "leiden-fold-18",
              "louvain-weighted")
INFOMAP_NAMES = ("infomap-weighted", "infomap-binary", "infomap-reversed")
PERTURBATIONS = ("omit-2022-10-16", "omit-2022-10-17", "omit-2022-10-18",
                 "drop-0.0001", "drop-0.0005", "drop-0.001")


def digest(path):
    result = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def read(path):
    return json.loads(path.read_text())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify_grid(directory):
    grid = read(directory / "grid.json")
    attempted = {(entry["resolution"], entry["seed"]) for entry in grid["runs"]}
    require(len(grid["runs"]) == 120 and attempted == {
        (resolution, seed) for resolution in RESOLUTIONS for seed in SEEDS
    }, f"Incomplete grid: {directory}")
    counts = Counter(entry["resolution"] for entry in grid["runs"]
                     if entry["connected"] and entry["eligible_groups"] >= 2)
    eligible = {res for res in RESOLUTIONS if counts[res] >= 10}
    require(eligible == {row["resolution"] for row in grid["resolutions"]},
            f"Resolution eligibility mismatch: {directory}")
    summary = {key: val for key, val in grid.items() if key != "runs"}
    summary["grid_report_sha256"] = digest(directory / "grid.json")
    summary["eligible_run_counts"] = {str(res): counts[res] for res in RESOLUTIONS}
    summary["connected_runs"] = sum(entry["connected"] for entry in grid["runs"])
    summary["accounts_sha256"] = digest(directory / "accounts.npy")
    selected = grid["selected"]
    if selected:
        best = max(row["median_ari"] for row in grid["resolutions"])
        expected = min((row for row in grid["resolutions"] if best - row["median_ari"] <= 1e-6),
                       key=lambda row: (abs(row["resolution"] - 1), row["resolution"]))
        require(selected == expected, f"Resolution selection mismatch: {directory}")
        res, seed = selected["resolution"], selected["seed"]
        require(digest(directory / f"{res}-{seed}.npy") == grid["partition_sha256"],
                f"Partition hash mismatch: {directory}")
        summary["selected_diagnostics"] = next(
            row for row in grid["runs"] if (row["resolution"], row["seed"]) == (res, seed)
        )
    else:
        require(not eligible, f"Missing selected partition: {directory}")
    return summary


def verify_sensitivity(directory):
    summary = read(directory / "summary.json")
    require(digest(directory / "membership.npy") == summary["partition_sha256"],
            f"Sensitivity hash mismatch: {directory}")
    if "hierarchy_sha256" in summary:
        require(digest(directory / "hierarchy.npy") == summary["hierarchy_sha256"],
                f"Hierarchy hash mismatch: {directory}")
    summary["accounts_sha256"] = digest(directory / "accounts.npy")
    return summary


def build(work, reports, snapshot, source_revision):
    ledger = work / "discovery.parquet"
    extract = read(reports / "m3-discovery-extract.json")
    require(digest(ledger) == extract["discovery_ledger_sha256"], "Discovery ledger hash mismatch")
    footer = read(snapshot)["footer_inventory_sha256"]
    require(footer == read(reports / "m2-host-inventory.json")["footer_inventory_sha256"],
            "Corpus footer fingerprint mismatch")
    grids = {name: verify_grid(work / name) for name in GRID_NAMES}
    primary = grids["leiden-weighted"]
    require(primary["graph_sha256"] == grids["louvain-weighted"]["graph_sha256"],
            "Weighted graph differs across optimizers")
    ids, arcs, graph, out = graph_from_ledger(ledger)
    account_ids, labels = selected_partition(work / "leiden-weighted")
    require(np.array_equal(ids, account_ids), "Rebuilt graph vertices differ")
    graph_hash = sha256()
    for values in (ids, arcs, graph.es["weight"]):
        graph_hash.update(np.asarray(values, dtype="<u8").tobytes())
    require(graph_hash.hexdigest() == primary["graph_sha256"], "Rebuilt graph hash mismatch")
    primary_summary = diagnostics(arcs, labels, out)
    require(all(primary["selected_diagnostics"][key] == value
                for key, value in primary_summary.items()), "Primary diagnostics mismatch")
    primary["size_quantiles_accounts"] = dict(zip(
        ("min", "median", "p90", "p99", "max"),
        np.quantile(np.bincount(labels), [0, .5, .9, .99, 1]).tolist(),
    ))
    return {
        "freeze_date_utc": "2026-11-26",
        "protocol": "m3-repost-pilot-specification.md",
        "fitting_source_revision": source_revision,
        "implementation_sha256": {name: digest(Path(__file__).with_name(name)) for name in (
            "m2_repost_coverage.py", "m3_extract_discovery.py", "m3_discovery.py",
            "m3_sensitivities.py", "m3_calibrate.py", "m3_prediction.py", "m3_reference.py",
            "m3_reference_probe.py", "m3_reference_probe.cpp", "m3_freeze_discovery.py",
        )},
        "date_timezone": "America/Sao_Paulo",
        "discovery_dates": ["2022-10-16", "2022-10-18"],
        "holdout_dates": ["2022-10-19", "2022-10-21"],
        "date_bounds_inclusive": True,
        "eligibility": "M2 verified distinct explicit repost, known query stratum, resolved "
                       "sharer and historical author, excluding verified self-reposts",
        "source_footer_inventory_sha256": footer,
        "ledger": extract,
        "software": {"python": platform.python_version(), **{
            package: version(package) for package in (
                "duckdb", "igraph", "leidenalg", "networkx", "numpy", "scipy", "scikit-learn",
                "infomap",
            )
        }},
        "threads": {"duckdb": 4, **{key: os.environ.get(key) for key in (
            "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
        )}},
        "grid_settings": {"resolutions": RESOLUTIONS, "seeds": list(SEEDS),
                          "leiden_iterations": "until convergence", "infomap_trials": 20,
                          "infomap_seed": 20, "infomap_teleportation": 0.15,
                          "infomap_recorded_teleportation": False,
                          "infomap_flat_partition": "finest hierarchy level"},
        "grids": grids,
        "sensitivities": {
            **{name: verify_sensitivity(work / name) for name in INFOMAP_NAMES},
            **{name: verify_sensitivity(work / "perturbations" / name) for name in PERTURBATIONS},
        },
        "comparisons": read(work / "comparisons-fast.json"),
        "prediction_calibration": read(work / "calibration.json"),
        "reference": {"exhaustive_fixtures": verify_reference(),
                      "prediction_scalar_fixture": verify_prediction(),
                      "full_proposal_probe": read(work / "reference-probe.json"),
                      "early_rejection_probe": read(work / "reference-probe-early.json"),
                      "status": "Exact rejection candidate benchmarked on discovery. "
                                "Executable scoring and registered simulations are pending."},
        "holdout_status": "unopened",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path)
    parser.add_argument("reports", type=Path)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("source_revision")
    args = parser.parse_args()
    print(json.dumps(build(args.work, args.reports, args.snapshot, args.source_revision),
                     indent=2, allow_nan=False))
