"""Run the frozen M3 jobs with local logs and restartable stage outputs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import fcntl
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

from m3_holdout import verify_evaluation, verify_frozen
from m3_reference_score import atomic_json, digest


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def jobs(plan, refits):
    runs = plan["registered_runs"]
    structural = [
        ("primary-reference", "primary-reference", ["--secondary"]),
        *((f"reference-{mode}", "primary-reference", ["--stratify", mode])
          for mode in runs["alternative_strata"]),
        ("distinct-dyads", "distinct-dyads", []),
        *((f"exclude-{field}-{level.replace('%', 'pct')}", "primary-reference",
           ["--exclude", field, level]) for field, levels in runs["frequency_exclusions"].items()
          for level in levels),
        *((f"endpoint-{name}", "primary-reference", ["--scenario", name, "--refits", str(refits)])
          for name in runs["endpoint_cases"]),
    ]
    light = [(stage, stage, []) for stage in ("prediction", "endpoint-bounds",
                                             "circulation-diagnostics")]
    return structural, light


def execute(item, base, directory, fingerprint):
    name, stage, extra = item
    result = directory / f"{name}.json"
    status = directory / f"{name}.status.json"
    log = directory / f"{name}.log"
    saved = json.loads(status.read_text()) if status.exists() else {}
    if (saved.get("state") == "complete" and saved.get("freeze_sha256") == fingerprint
            and result.exists() and digest(result) == saved["result_sha256"]):
        return name, "complete"
    metadata = dict(freeze_sha256=fingerprint, started_utc=stamp(), log=log.name)
    atomic_json(status, dict(metadata, state="running"))
    temp = result.with_suffix(".tmp")
    with temp.open("w") as out, log.open("a") as err:
        rc = subprocess.run([base[0], base[1], stage, *base[2:], *extra],
                            stdout=out, stderr=err, check=False).returncode
    state = "failed"
    if rc == 0:
        try:
            if not isinstance(json.loads(temp.read_text()), dict) and stage != "endpoint-bounds":
                raise ValueError("Expected a structured result")
        except ValueError as error:
            with log.open("a") as err:
                print(f"Result verification failed: {error}", file=err)
        else:
            temp.replace(result)
            metadata["result_sha256"] = digest(result)
            state = "complete"
    atomic_json(status, dict(metadata, state=state, exit_code=rc, finished_utc=stamp()))
    print(f"{stamp()} {name}: {state}", flush=True)
    return name, state


def run(args):
    plan = verify_evaluation(args.work, args.binary)
    verify_frozen(args.discovery, args.accounts, args.membership)
    freeze = Path(__file__).resolve().parent.parent / "docs/reports/m3-evaluation-freeze.json"
    fingerprint = digest(freeze)
    directory = args.work / "evaluation"
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    with (directory / "lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        status = directory / "workflow-status.json"
        lanes = jobs(plan, args.refits)
        atomic_json(status, dict(state="running", freeze_sha256=fingerprint, started_utc=stamp(),
                                 jobs=[name for lane in lanes for name, _, _ in lane]))
        driver = Path(__file__).with_name("m3_holdout.py")
        base = [sys.executable, str(driver), str(args.discovery), str(args.accounts),
                str(args.membership), str(args.work), "--binary", str(args.binary),
                "--workers", str(args.workers)]

        def run_lane(lane):
            return dict(execute(item, base, directory, fingerprint) for item in lane)

        with ThreadPoolExecutor(max_workers=2) as executor:
            long = executor.submit(run_lane, lanes[0])
            short = executor.submit(run_lane, lanes[1])
            states = {**long.result(), **short.result()}
        state = "complete" if all(s == "complete" for s in states.values()) else "completed_with_failures"
        atomic_json(status, dict(state=state, freeze_sha256=fingerprint,
                                 finished_utc=stamp(), jobs=states))
        print(f"{stamp()} {state}\a", flush=True)
        return int(state != "complete")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("discovery", "accounts", "membership", "work", "binary", "refits"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--workers", type=int, default=8)
    arguments = parser.parse_args()
    if arguments.workers < 1:
        parser.error("--workers must be positive")
    sys.exit(run(arguments))
