"""Run discovery graph perturbations and compare common-account memberships."""
import argparse
import hashlib
import json
from math import ceil
from pathlib import Path

import numpy as np
from infomap import Infomap

from m3_calibrate import selected_partition
from m3_discovery import compare, diagnostics, directed_louvain_graph, fit, graph_from_ledger


def infomap_fit(arcs, weights):
    model = Infomap(silent=True, flow_model="directed", seed=20, num_trials=20,
                    recorded_teleportation=False, teleportation_probability=0.15)
    model.add_links(
        (int(source), int(target), float(weight))
        for (source, target), weight in zip(arcs, weights)
    )
    model.run()
    hierarchy = model.get_multilevel_modules()
    paths = [hierarchy[node] for node in range(len(hierarchy))]
    width = max(map(len, paths))
    levels = np.zeros((len(paths), width), dtype=np.int32)
    for index, path in enumerate(paths):
        levels[index, :len(path)] = path
    labels = np.unique(levels, axis=0, return_inverse=True)[1].astype(np.int32)
    return labels, levels, dict(codelength=model.codelength, depth=width,
                                top_modules=model.num_top_modules,
                                leaf_modules=len(np.unique(labels)))


def save_membership(output, accounts, labels, summary, primary=None, hierarchy=None):
    output.mkdir(mode=0o700, parents=True, exist_ok=True)
    np.save(output / "accounts.npy", accounts)
    labels_path = output / "membership.npy"
    np.save(labels_path, labels)
    summary["partition_sha256"] = hashlib.sha256(labels_path.read_bytes()).hexdigest()
    if hierarchy is not None:
        path = output / "hierarchy.npy"
        np.save(path, hierarchy)
        summary["hierarchy_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    if primary is not None:
        summary.update(compare(*primary, accounts, labels))
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def infomap_run(ledger, output, binary, reverse):
    accounts, arcs, graph, out_actions = graph_from_ledger(ledger, binary=binary)
    if reverse:
        arcs = arcs[:, ::-1]
    labels, hierarchy, summary = infomap_fit(arcs, graph.es["weight"])
    summary.update(binary=binary, reverse=reverse, **diagnostics(arcs, labels, out_actions))
    save_membership(output, accounts, labels, summary, hierarchy=hierarchy)


def perturb(ledger, primary_directory, output):
    grid = json.loads((primary_directory / "grid.json").read_text())
    primary = selected_partition(primary_directory)
    if primary is None:
        raise ValueError("The primary grid contains no eligible partition")
    selected = grid["selected"]
    accounts, _, graph, _ = graph_from_ledger(ledger)
    strengths = np.asarray(graph.strength(weights="weight", mode="in"))
    positive = np.flatnonzero(strengths > 0)
    ranked = positive[np.lexsort((accounts[positive], -strengths[positive]))]
    cases = {
        **{f"omit-{day}": {"omit_day": day}
           for day in ("2022-10-16", "2022-10-17", "2022-10-18")},
        **{f"drop-{share}": {"drop": accounts[ranked[:ceil(share * len(ranked))]]}
           for share in (0.0001, 0.0005, 0.001)},
    }
    for label, settings in cases.items():
        ids, arcs, candidate, out_actions = graph_from_ledger(ledger, **settings)
        method = grid["method"]
        source = candidate if method == "leiden" else directed_louvain_graph(candidate)
        labels = fit(method, source, selected["resolution"], selected["seed"])
        summary = diagnostics(arcs, labels, out_actions)
        summary.update(vertices=len(ids), arcs=len(arcs), actions=int(out_actions.sum()),
                       removed_ranked_accounts=len(settings.get("drop", ())))
        save_membership(output / label, ids, labels, summary, primary)


def compare_partitions(primary_directory, alternatives):
    primary = selected_partition(primary_directory)
    if primary is None:
        raise ValueError("The primary grid contains no eligible partition")
    results = {}
    for directory in alternatives:
        if (directory / "grid.json").exists():
            alternative = selected_partition(directory)
        else:
            alternative = (np.load(directory / "accounts.npy"),
                           np.load(directory / "membership.npy"))
        results[directory.name] = (compare(*primary, *alternative) if alternative is not None
                                   else {"disposition": "no eligible partition"})
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--primary", type=Path)
    parser.add_argument("--binary", action="store_true")
    parser.add_argument("--reverse", action="store_true")
    parser.add_argument("--compare", type=Path, nargs="+")
    args = parser.parse_args()
    if args.compare:
        if not args.primary:
            parser.error("--compare requires --primary")
        args.output.write_text(json.dumps(compare_partitions(args.primary, args.compare),
                                          indent=2) + "\n")
    elif args.primary:
        perturb(args.ledger, args.primary, args.output)
    else:
        infomap_run(args.ledger, args.output, args.binary, args.reverse)
