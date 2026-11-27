"""Run discovery completion grids and small reference rehearsals on the data host."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import fcntl
import json
from pathlib import Path
import subprocess
import sys

from m3_complete_endpoints import SCENARIOS
from m3_reference_score import atomic_json, digest

SCRIPTS = Path(__file__).resolve().parent


def run_case(work, binary, name, workers, draws, fingerprint):
    ledger = work / f"{name}.parquet"
    output = work / name
    output.mkdir(mode=0o700, exist_ok=True)
    with (output / "workflow.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        status = output / "status.json"
        if digest(ledger) != fingerprint:
            raise ValueError(f"Completion ledger fingerprint differs: {name}")
        step = "discovery grid"
        try:
            atomic_json(status, dict(state="running", step=step))
            with (output / "refit.log").open("a", buffering=1) as log:
                subprocess.run([sys.executable, "-u", str(SCRIPTS / "m3_refit_endpoints.py"),
                                str(ledger), str(output), "--workers", str(workers)],
                               stdout=log, stderr=subprocess.STDOUT, check=True)
            result = json.loads((output / "grid.json").read_text())["selected"]
            if result is None:
                atomic_json(status, dict(state="no eligible partition", step=step))
                return
            step = "discovery reference rehearsal"
            atomic_json(status, dict(state="running", step=step))
            partition = output / f"{result['resolution']}-{result['seed']}.npy"
            temporary = output / "reference.tmp"
            with temporary.open("w") as result_file, (output / "refit.log").open("a") as log:
                subprocess.run([sys.executable, str(SCRIPTS / "m3_reference_score.py"), str(ledger),
                                str(output / "accounts.npy"), str(partition), str(binary),
                                str(output / "reference-batches"), "--workers", str(workers),
                                "--draws", str(draws), "--batch-size", "1",
                                "--proposals-per-draw", "2048"],
                               stdout=result_file, stderr=log, check=True)
            temporary.replace(output / "reference.json")
            atomic_json(status, dict(state="complete", step=step))
        except Exception as error:
            atomic_json(status, dict(state="failed", step=step, error=str(error)))
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path)
    parser.add_argument("binary", type=Path)
    parser.add_argument("--workers-per-scenario", type=int, default=3)
    parser.add_argument("--rehearsal-draws", type=int, default=8)
    args = parser.parse_args()
    if min(args.workers_per_scenario, args.rehearsal_draws) < 1:
        parser.error("Worker and draw counts must be positive")
    manifest = json.loads((args.work / "completion.json").read_text())
    failures = []
    with ThreadPoolExecutor(max_workers=len(SCENARIOS)) as pool:
        jobs = {}
        for direction, rank in SCENARIOS:
            name = f"{direction}-{rank}"
            jobs[name] = pool.submit(
                run_case, args.work, args.binary, name, args.workers_per_scenario,
                args.rehearsal_draws, manifest["scenarios"][name]["sha256"],
            )
        for name, result in jobs.items():
            try:
                result.result()
            except Exception as error:
                failures.append(name)
                print(f"{name}: {error}", file=sys.stderr, flush=True)
    atomic_json(args.work / "workflow-status.json",
                dict(state="failed" if failures else "complete", failed_scenarios=failures))
    print("\a", end="", flush=True)
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
