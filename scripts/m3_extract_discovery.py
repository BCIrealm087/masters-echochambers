"""Reconcile and export only discovery actions from the registered M2 snapshot."""
import argparse
import hashlib
import json
from pathlib import Path

import duckdb

from m2_repost_coverage import HOLDOUT_START, reconcile, rows


def export(root, work):
    work.mkdir(mode=0o700, parents=True, exist_ok=True)
    with duckdb.connect(config={
        "threads": 4, "memory_limit": "8GB", "preserve_insertion_order": False,
        "temp_directory": str(work.resolve()),
    }) as db:
        reconcile(db, root.resolve(), window_end=HOLDOUT_START)
        db.execute("""
            CREATE TEMP VIEW discovery AS
            SELECT post_id, day, membership, sharer, target, resolution,
                   CASE WHEN resolution = 'unique author' THEN first_author END AS author,
                   ((post_id >> 22) + 1288834974657) // 1000 AS action_second,
                   ((target >> 22) + 1288834974657) // 1000 AS original_second
            FROM coverage LEFT JOIN historical USING (target)
        """)
        ledger = work / "discovery.parquet"
        db.execute("""
            COPY (SELECT * FROM discovery ORDER BY post_id)
            TO ? (FORMAT PARQUET, COMPRESSION ZSTD)
        """, [str(ledger)])
        counts = rows(db, """
            SELECT cast(day AS VARCHAR) AS day, membership, count(*) AS actions,
                   count(*) FILTER (WHERE author IS NULL) AS unresolved_authors,
                   count(*) FILTER (WHERE sharer IS NULL) AS unresolved_sharers,
                   count(*) FILTER (WHERE sharer = author) AS self_reposts,
                   count(*) FILTER (WHERE sharer <> author) AS eligible_actions,
                   count(*) FILTER (
                       WHERE sharer <> author AND original_second > action_second
                   ) AS publication_after_action
            FROM discovery GROUP BY day, membership ORDER BY day, membership
        """)
    digest = hashlib.sha256()
    with ledger.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return {"duckdb": duckdb.__version__, "discovery_ledger_sha256": digest.hexdigest(),
            "counts": counts}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    print(json.dumps(export(args.root, args.work), indent=2))
