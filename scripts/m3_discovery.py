"""Fit and compare registered directed account partitions using discovery actions."""
import argparse
import hashlib
import json
from pathlib import Path

import duckdb
import igraph as ig
import leidenalg
import networkx as nx
import numpy as np
from scipy.sparse import coo_matrix
from scipy.stats import hypergeom
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics.cluster import entropy, mutual_info_score

RESOLUTIONS = (0.5, 0.75, 1.0, 1.25, 1.5, 2.0)
SEEDS = range(20)
TOLERANCE = 1e-6


def verify_optimizers():
    arcs = [(0, 1), (1, 0), (2, 0), (1, 2)]
    weights = [3, 1, 2, 1]
    graph = ig.Graph(3, arcs, directed=True)
    graph.es["weight"] = weights
    expected = -4 / 49
    assert graph.get_edgelist() == arcs
    assert graph.strength(weights="weight", mode="out") == [3, 2, 2]
    assert graph.strength(weights="weight", mode="in") == [3, 3, 1]
    leiden = leidenalg.RBConfigurationVertexPartition(
        graph, initial_membership=[0, 0, 1], weights="weight",
    )
    directed = directed_louvain_graph(graph)
    assert list(directed.out_degree(weight="weight")) == [(0, 3), (1, 2), (2, 2)]
    assert list(directed.in_degree(weight="weight")) == [(0, 3), (1, 3), (2, 1)]
    assert np.isclose(leiden.quality() / 7, expected)
    louvain_quality = nx.community.modularity(directed, [{0, 1}, {2}])
    assert np.isclose(louvain_quality, expected)
    for method, source in (("leiden", graph), ("louvain", directed)):
        labels = fit(method, source, 1, 0)
        assert len(labels) == 3
        assert graph.modularity(labels, weights="weight", directed=True) >= -1e-12
    return {"expected": expected, "leiden": leiden.quality() / 7, "louvain": louvain_quality}


def directed_louvain_graph(graph):
    directed = nx.DiGraph()
    directed.add_nodes_from(range(graph.vcount()))
    directed.add_weighted_edges_from(
        (source, target, weight)
        for (source, target), weight in zip(graph.get_edgelist(), graph.es["weight"])
    )
    return directed


def fit(method, graph, resolution, seed):
    if method == "leiden":
        labels = leidenalg.find_partition(
            graph, leidenalg.RBConfigurationVertexPartition, weights="weight",
            n_iterations=-1, resolution_parameter=resolution, seed=seed,
        ).membership
    else:
        groups = nx.community.louvain_communities(graph, resolution=resolution, seed=seed)
        labels = np.empty(len(graph), dtype=np.int32)
        for index, group in enumerate(groups):
            labels[list(group)] = index
    # Canonical labels use the first account in each group.
    _, first, inverse = np.unique(labels, return_index=True, return_inverse=True)
    return first.argsort().argsort()[inverse].astype(np.int32)


def graph_from_ledger(ledger, *, before=None, omit_day=None, drop=(), binary=False):
    with duckdb.connect(config={"threads": 4}) as db:
        cols = db.execute("""
            SELECT sharer, author, count(*) AS actions FROM read_parquet(?)
            WHERE sharer <> author AND membership <> 'unknown'
              AND (? IS NULL OR day < cast(? AS DATE))
              AND (? IS NULL OR day <> cast(? AS DATE))
            GROUP BY sharer, author ORDER BY sharer, author
        """, [str(ledger), before, before, omit_day, omit_day]).fetchnumpy()
    source, target, actions = (cols[key] for key in ("sharer", "author", "actions"))
    keep = ~np.isin(source, np.asarray(drop, dtype=np.uint64))
    keep &= ~np.isin(target, np.asarray(drop, dtype=np.uint64))
    source, target, actions = source[keep], target[keep], actions[keep]
    accounts = np.union1d(source, target)
    arcs = np.column_stack((accounts.searchsorted(source), accounts.searchsorted(target)))
    graph = ig.Graph(len(accounts), arcs, directed=True)
    graph.es["weight"] = np.ones(len(actions), dtype=np.int64) if binary else actions
    out_actions = np.zeros(len(accounts), dtype=np.int64)
    np.add.at(out_actions, arcs[:, 0], actions)
    return accounts, arcs, graph, out_actions


def diagnostics(arcs, labels, out_actions):
    internal = arcs[labels[arcs[:, 0]] == labels[arcs[:, 1]]]
    weak = ig.Graph(len(labels), internal, directed=False).connected_components()
    sizes = np.bincount(labels)
    sharers = np.bincount(labels, weights=out_actions > 0)
    actions = np.bincount(labels, weights=out_actions)
    eligible = (sharers >= 20) & (actions >= 100)
    return {
        "connected": len(weak) == len(sizes),
        "groups": len(sizes),
        "eligible_groups": int(eligible.sum()),
        "largest_group_accounts": int(sizes.max()),
        "eligible_group_sharers": int(sharers[eligible].sum()),
        "eligible_group_actions": int(actions[eligible].sum()),
    }


def compare(first_accounts, first, second_accounts, second):
    _, ai, bi = np.intersect1d(first_accounts, second_accounts, return_indices=True)
    if not len(ai):
        return {"common_accounts": 0}
    a, b = first[ai], second[bi]
    overlap = coo_matrix((np.ones(len(a), dtype=np.int64), (a, b))).tocsr().tocoo()
    jaccard = overlap.data / (
        np.bincount(a)[overlap.row] + np.bincount(b)[overlap.col] - overlap.data
    )
    information = mutual_info_score(a, b)
    a_entropy, b_entropy = entropy(a), entropy(b)
    expected = expected_information(np.bincount(a), np.bincount(b), len(a))
    normalizer = (a_entropy + b_entropy) / 2 - expected
    epsilon = np.finfo(float).eps
    normalizer = min(normalizer, -epsilon) if normalizer < 0 else max(normalizer, epsilon)
    ari = adjusted_rand_score(a, b)
    return {
        "common_accounts": len(ai),
        "ari": ari,
        "ami": 1.0 if ari == 1 else (information - expected) / normalizer,
        "vi_nats": max(0.0, a_entropy + b_entropy - 2 * information),
        "mean_best_jaccard_primary_groups": float(
            coo_matrix((jaccard, (overlap.row, overlap.col))).tocsr().max(axis=1)
            .toarray().ravel()[np.unique(a)].mean()
        ),
    }


def expected_information(first_sizes, second_sizes, total):
    """Compute the permutation expectation once per distinct pair of group sizes."""
    first, first_counts = np.unique(first_sizes[first_sizes > 0], return_counts=True)
    second, second_counts = np.unique(second_sizes[second_sizes > 0], return_counts=True)
    result = 0.0
    for a, multiplicity in zip(first, first_counts):
        for b, count in zip(second, second_counts):
            overlap = np.arange(max(1, int(a + b - total)), min(a, b) + 1, dtype=float)
            probability = hypergeom.pmf(overlap, total, a, b)
            result += multiplicity * count * np.dot(
                probability, (overlap / total) * np.log(overlap * total / (a * float(b)))
            )
    return result


def grid(method, graph, arcs, out_actions, directory):
    optimizer_graph = graph if method == "leiden" else directed_louvain_graph(graph)
    directory.mkdir(parents=True, exist_ok=True)
    results = []
    representatives = []
    for resolution in RESOLUTIONS:
        passed = []
        for seed in SEEDS:
            labels = fit(method, optimizer_graph, resolution, seed)
            summary = diagnostics(arcs, labels, out_actions)
            summary.update(seed=seed, resolution=resolution, modularity=graph.modularity(
                labels, weights="weight", resolution=resolution, directed=True,
            ))
            results.append(summary)
            np.save(directory / f"{resolution}-{seed}.npy", labels)
            if summary["connected"] and summary["eligible_groups"] >= 2:
                passed.append((seed, labels))
        if len(passed) < 10:
            continue
        stability = np.eye(len(passed))
        for i, (_, a) in enumerate(passed):
            for j in range(i):
                stability[i, j] = stability[j, i] = adjusted_rand_score(a, passed[j][1])
        median = float(np.median(stability[np.triu_indices(len(passed), k=1)]))
        means = (stability.sum(axis=1) - 1) / (len(passed) - 1)
        index = next(i for i, score in enumerate(means) if score >= means.max() - TOLERANCE)
        representatives.append(dict(resolution=resolution, seed=passed[index][0],
                                    median_ari=median, eligible_runs=len(passed),
                                    representative_mean_ari=float(means[index])))
    if not representatives:
        return {"runs": results, "resolutions": [], "selected": None}
    maximum = max(rep["median_ari"] for rep in representatives)
    selected = min(
        (rep for rep in representatives if rep["median_ari"] >= maximum - TOLERANCE),
        key=lambda rep: (abs(rep["resolution"] - 1), rep["resolution"]),
    )
    return {"runs": results, "resolutions": representatives, "selected": selected}


def write_graph_grid(ledger, directory, method, binary=False, before=None):
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    accounts, arcs, graph, out_actions = graph_from_ledger(ledger, binary=binary, before=before)
    np.save(directory / "accounts.npy", accounts)
    graph_hash = hashlib.sha256()
    for values in (accounts, arcs, graph.es["weight"]):
        graph_hash.update(np.asarray(values, dtype="<u8").tobytes())
    result = grid(method, graph, arcs, out_actions, directory)
    result.update(method=method, binary=binary, before=before, vertices=len(accounts),
                  arcs=len(arcs), actions=int(out_actions.sum()),
                  graph_sha256=graph_hash.hexdigest(), optimizer_fixture=verify_optimizers())
    if result["selected"]:
        selected = result["selected"]
        partition = directory / f"{selected['resolution']}-{selected['seed']}.npy"
        result["partition_sha256"] = hashlib.sha256(partition.read_bytes()).hexdigest()
    (directory / "grid.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", action="store_true")
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--method", choices=("leiden", "louvain"), default="leiden")
    parser.add_argument("--binary", action="store_true")
    parser.add_argument("--before")
    args = parser.parse_args()
    print(json.dumps(verify_optimizers()))
    if not args.fixture:
        if args.ledger is None or args.output is None:
            parser.error("--ledger and --output are required unless running --fixture")
        write_graph_grid(args.ledger, args.output, args.method, args.binary, args.before)
