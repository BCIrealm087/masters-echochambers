"""Build the pre-outcome executable freeze from verified evaluation margins."""
import argparse
from importlib.metadata import version
import json
from pathlib import Path
import platform

from m3_holdout import REPORTS, compare_m2
from m3_reference_score import HOLDOUT_DAYS, atomic_json, digest

SOURCES = (
    "m2_host_inventory.py", "m2_repost_coverage.py", "m3_holdout.py",
    "m3_holdout_completions.py", "m3_complete_endpoints.py", "m3_calibrate.py",
    "m3_reference_score.py", "m3_reference_score.cpp", "m3_distinct_dyads.py",
    "m3_freeze_evaluation.py",
)


def read(path):
    return json.loads(path.read_text())


def check(path, expected):
    if digest(path) != expected:
        raise ValueError(f"Evaluation artifact fingerprint differs: {path}")


def build(holdout, completions, binary):
    discovery_freeze = REPORTS / "m3-discovery-freeze.json"
    frozen = read(discovery_freeze)
    primary_path = holdout / "margins.json"
    primary = read(primary_path)
    compare_m2(primary["counts"])
    check(holdout / "holdout.parquet", primary["ledger_sha256"])
    if (primary["source_footer_inventory_sha256"] != frozen["source_footer_inventory_sha256"]
            or any(row["illegal_time_or_reference"] for row in primary["counts"])):
        raise ValueError("Primary input snapshot or pairing legality changed")
    comparison = read(completions / "review.json")
    scenario_inputs = read(holdout / "endpoint-completions" / "margins.json")
    if (scenario_inputs["primary_ledger_sha256"] != primary["ledger_sha256"] or
            scenario_inputs["scenarios"].keys() != comparison.keys()):
        raise ValueError("Scenario inputs differ from the reviewed refits")
    scenarios = {}
    for name, result in comparison.items():
        grid, completion = result["grid"], scenario_inputs["scenarios"][name]
        chosen = grid["selected"]
        filename = f"{chosen['resolution']}-{chosen['seed']}.npy"
        check(completions / name / "accounts.npy", grid["accounts_sha256"])
        check(completions / name / filename, grid["partition_sha256"])
        check(holdout / "endpoint-completions" / f"{name}.parquet", completion["ledger_sha256"])
        if (sum(row["actions"] for row in primary["counts"]) !=
                sum(row["actions"] for row in completion["margins"]) or
                any(row["illegal_time_or_reference"] for row in completion["margins"])):
            raise ValueError(f"Scenario population changed unexpectedly: {name}")
        scenarios[name] = {
            "partition_file": filename, "accounts_sha256": grid["accounts_sha256"],
            "partition_sha256": grid["partition_sha256"],
            "graph_sha256": grid["graph_sha256"],
            "holdout_ledger_sha256": completion["ledger_sha256"],
            "holdout_eligible_actions": sum(row["eligible"] for row in completion["margins"]),
            **{key: completion[key] for key in (
                "posts_imputed", "actions_imputed", "inherited_actions",
                "blocked_overlap_actions", "still_unresolved_actions",
            )},
        }
    scripts = Path(__file__).resolve().parent
    return {
        "date_utc": "2026-11-27", "holdout_outcomes": "unopened",
        "protocol": "m3-repost-pilot-specification.md",
        "discovery_freeze_sha256": digest(discovery_freeze),
        "holdout_dates": list(map(str, HOLDOUT_DAYS)), "action_timezone": "America/Sao_Paulo",
        "holdout_ledger_sha256": primary["ledger_sha256"],
        "primary_margins_sha256": digest(primary_path), "primary_margins": primary["counts"],
        "group_margin_dispositions": {
            "total": len(primary["group_margins"]),
            "eligible": sum(row["holm_eligible"] for row in primary["group_margins"]),
        },
        "endpoint_scenarios": scenarios,
        "implementation_sha256": {name: digest(scripts / name) for name in SOURCES},
        "reference_binary_sha256": digest(binary),
        "reference_compile_flags": ["-O3", "-std=c++17", "-Wall", "-Wextra"],
        "software": {"python": platform.python_version(), **{
            name: version(name) for name in ("duckdb", "numpy")
        }},
        "prediction_calibration": frozen["prediction_calibration"],
        "reference_settings": {
            "draws": 9999, "batch_size": 64, "seed": 20261127,
            "proposals_per_draw": 10000, "default_workers": 8,
            "sampler": "exact time-ordered assignment, rejecting any self-repost",
            "primary_strata": ["day", "context"], "secondary_group_adjustment": "Holm",
            "group_minimum_actions": 100, "group_minimum_sharers": 20,
            "one_sided_alpha": .05, "primary_practical_screen_pp": 5,
            "practical_screens_pp": [2.5, 5, 10, 20],
            "proposal_budget_failure": "record feasibility limit and withhold affected p-value",
        },
        "registered_runs": {
            "primary": {"stratify": "day-context", "secondary": True},
            "alternative_strata": ["day", "pooled"],
            "frequency_exclusions": {field: ["1", "5", "1%"] for field in ("author", "target")},
            "endpoint_cases": list(scenarios),
            "additional_stages": ["distinct-dyads", "endpoint-bounds",
                                  "circulation-diagnostics", "prediction"],
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("holdout", "completions", "binary", "output"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    result = build(args.holdout, args.completions, args.binary)
    atomic_json(args.output, result)
