"""Reconcile the October ITED-Br repost sample and print aggregate coverage."""
import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import duckdb

WINDOW_START = "2022-10-16"
WINDOW_END = "2022-10-22"
HOLDOUT_START = "2022-10-19"


def rows(db, query):
    result = db.execute(query)
    keys = [column[0] for column in result.description]
    return [dict(zip(keys, row)) for row in result.fetchall()]


def audit(db, root):
    db.read_parquet(str(root / "tweets" / "*" / "*.parquet"), filename=True).create_view(
        "corpus"
    )
    # The fixed offset is valid throughout this window. Dates outside it only
    # indicate whether a row could belong to the audit.
    zone = ZoneInfo("America/Sao_Paulo")
    for boundary in (WINDOW_START, WINDOW_END):
        assert datetime.fromisoformat(boundary).replace(tzinfo=zone).utcoffset() == timedelta(hours=-3)
    db.execute(f"""
        CREATE MACRO usable_id(value) AS
            CASE WHEN regexp_full_match(value, '[1-9][0-9]{{0,19}}')
                 THEN try_cast(value AS UBIGINT) END;
        CREATE MACRO local_day(stamp) AS
            cast(make_timestamp(epoch_us(stamp)) - INTERVAL '3 hours' AS DATE);
        CREATE VIEW candidate_copies AS
        WITH parsed AS (
            SELECT usable_id(id) AS post_id, type, usable_id(author_id) AS sharer,
                   usable_id(referenced_tweet_id) AS target,
                   try_cast(CASE WHEN regexp_full_match(created_at,
                       '[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}[ T][0-9]{{2}}:[0-9]{{2}}:[0-9]{{2}}([.][0-9]+)?')
                       THEN created_at || '+00:00' ELSE created_at END AS TIMESTAMPTZ) AS action_time,
                   regexp_extract(filename, '/([^/]+)/[^/]+$', 1) AS context,
                   regexp_extract(filename, '([0-9]{{4}}_[0-9]{{2}}_[0-9]{{2}})[.]parquet$', 1)
                       AS partition
            FROM corpus
            WHERE regexp_matches(filename, '/(retweets_)?query_(lula|bolsonaro)/[^/]+$')
        ), timed AS (
            SELECT *, to_timestamp(((post_id >> 22) + 1288834974657) // 1000)
                AS id_time
            FROM parsed
        )
        SELECT *, local_day(action_time) AS action_day, local_day(id_time) AS id_day
        FROM timed;
        CREATE MACRO in_window(day_value) AS
            coalesce(day_value >= DATE '{WINDOW_START}' AND day_value < DATE '{WINDOW_END}', false);
        CREATE TEMP TABLE candidate_ids AS
            SELECT DISTINCT post_id FROM candidate_copies
            WHERE post_id IS NOT NULL AND (in_window(action_day) OR in_window(id_day));
    """)
    # Revisit all four contexts so an out-of-window copy can flag a conflict.
    db.execute("""
        CREATE TEMP TABLE event_copies AS
            SELECT * FROM candidate_copies SEMI JOIN candidate_ids USING (post_id);
        CREATE TEMP TABLE ledger AS
        WITH grouped AS (
            SELECT post_id, count(*) AS copies,
                   bool_or(ends_with(context, '_lula')) AS lula,
                   bool_or(ends_with(context, '_bolsonaro')) AS bolsonaro,
                   count(DISTINCT type) AS types,
                   count(DISTINCT action_time) AS times,
                   count(DISTINCT sharer) AS sharers,
                   count(DISTINCT target) AS targets,
                   count(*) FILTER (WHERE type = 'retweeted') AS repost_copies,
                   count(*) FILTER (WHERE action_time = id_time) AS verified_times,
                   min(type) AS kind, min(id_day) AS day,
                   min(sharer) AS known_sharer, min(target) AS known_target,
                   count(*) FILTER (WHERE type IS NULL) AS missing_types,
                   count(*) FILTER (WHERE action_time IS NULL) AS missing_times,
                   count(*) FILTER (WHERE sharer IS NULL) AS missing_sharers,
                   count(*) FILTER (WHERE target IS NULL) AS missing_targets
            FROM event_copies GROUP BY post_id
        )
        SELECT post_id, copies, day, repost_copies, missing_types, missing_times,
               missing_sharers, missing_targets, times > 1 AS conflicting_times,
               sharers > 1 AS conflicting_sharers, targets > 1 AS conflicting_targets,
               CASE WHEN lula AND bolsonaro THEN 'both'
                    WHEN lula THEN 'Lula only' WHEN bolsonaro THEN 'Bolsonaro only'
                    ELSE 'unknown' END AS membership,
               CASE WHEN types > 1 THEN 'conflicting type'
                    WHEN types = 0 OR kind NOT IN
                         ('retweeted', 'tweeted', 'quoted', 'replied_to', 'quoted, replied_to')
                         THEN 'unknown type'
                    WHEN kind = 'retweeted' THEN 'confirmed repost'
                    ELSE kind END AS action_type,
               CASE WHEN times = 1 AND verified_times > 0 THEN
                        CASE WHEN in_window(day) THEN 'in window' ELSE 'out of window' END
                    ELSE 'unresolved' END AS action_date,
               CASE WHEN sharers = 1 THEN known_sharer END AS sharer,
               CASE WHEN targets = 1 THEN known_target END AS target
        FROM grouped;
        CREATE TEMP TABLE reposts AS SELECT * FROM ledger
            WHERE action_type = 'confirmed repost' AND action_date = 'in window';
        CREATE TEMP TABLE targets AS
            SELECT target, count(*) AS action_count
            FROM reposts WHERE target IS NOT NULL GROUP BY target;
    """)
    print("Reconciled candidate actions. Scanning historical tweet rows.", file=sys.stderr)
    db.execute(f"""
        CREATE TEMP TABLE historical AS
        SELECT target, count(*) AS matches,
               count(author) AS usable_matches, min(author) AS first_author,
               max(author) AS last_author,
               count(*) FILTER (WHERE type = 'retweeted') AS repost_matches
        FROM (
            SELECT usable_id(id) AS target, usable_id(author_id) AS author, type
            FROM corpus
        ) SEMI JOIN targets USING (target)
        GROUP BY target;
        CREATE TEMP TABLE coverage AS
        SELECT reposts.*,
               CASE WHEN targets.action_count = 1 THEN '1'
                    WHEN targets.action_count <= 9 THEN '2–9'
                    WHEN targets.action_count <= 99 THEN '10–99'
                    WHEN targets.action_count >= 100 THEN '100+' END AS target_reuse,
               CASE WHEN reposts.target IS NULL THEN 'reference unavailable'
                    WHEN historical.matches IS NULL THEN 'original absent'
                    WHEN historical.usable_matches = 0 THEN 'author missing'
                    WHEN historical.first_author <> historical.last_author THEN 'conflicting authors'
                    WHEN historical.repost_matches > 0 THEN 'target recorded as repost'
                    ELSE 'unique author' END AS resolution,
               CASE WHEN day < DATE '{HOLDOUT_START}' THEN 'discovery'
                    ELSE 'holdout' END AS interval
        FROM reposts LEFT JOIN targets USING (target) LEFT JOIN historical USING (target);
        CREATE TEMP TABLE sharer_activity AS
            SELECT interval, sharer, count(*) AS action_count
            FROM coverage WHERE sharer IS NOT NULL GROUP BY interval, sharer;
    """)
    metrics = """
        count(*) AS reposts, count(sharer) AS usable_sharers, count(target) AS usable_references,
        count(*) FILTER (WHERE resolution = 'reference unavailable') AS reference_unavailable,
        count(*) FILTER (WHERE resolution = 'original absent') AS original_absent,
        count(*) FILTER (WHERE resolution = 'author missing') AS author_missing,
        count(*) FILTER (WHERE resolution = 'conflicting authors') AS conflicting_authors,
        count(*) FILTER (WHERE resolution = 'target recorded as repost') AS target_is_repost,
        count(*) FILTER (WHERE resolution = 'unique author') AS unique_author,
        count(*) FILTER (WHERE resolution = 'unique author' AND sharer IS NOT NULL) AS edges,
        count(DISTINCT target) AS distinct_targets,
        count(DISTINCT target) FILTER (WHERE resolution = 'unique author') AS resolved_targets,
        count(DISTINCT sharer) AS distinct_sharers,
        count(DISTINCT sharer) FILTER (WHERE resolution = 'unique author') AS sharers_with_edge
    """
    source_scan = rows(db, """
        SELECT context, partition, count(*) AS stored_rows,
               count(*) FILTER (WHERE type = 'retweeted') AS repost_rows,
               count(*) FILTER (WHERE starts_with(context, 'retweets_') AND
                   type IS DISTINCT FROM 'retweeted') AS other_rows_in_repost_folder,
               count(*) FILTER (WHERE NOT starts_with(context, 'retweets_') AND
                   type = 'retweeted') AS repost_rows_in_ordinary_folder,
               count(*) FILTER (WHERE in_window(action_day) OR in_window(id_day)) AS window_seed_rows,
               count(*) FILTER (WHERE post_id IS NULL) AS missing_ids,
               count(*) FILTER (WHERE post_id IS NULL AND in_window(action_day)) AS missing_ids_in_window,
               count(*) FILTER (WHERE action_day IS NULL AND id_day IS NULL) AS both_dates_unavailable,
               count(*) FILTER (WHERE type = 'retweeted' AND
                   (action_time IS NULL OR id_time IS NULL OR action_time <> id_time))
                   AS repost_rows_without_date_agreement,
               count(*) FILTER (WHERE type = 'retweeted' AND action_time = id_time
                   AND NOT in_window(action_day)) AS verified_repost_rows_outside_window
        FROM candidate_copies GROUP BY GROUPING SETS ((context, partition), (context))
        ORDER BY context, partition
    """)
    output = {
        "duckdb": duckdb.__version__,
        "window_inclusive_start_exclusive_end": [WINDOW_START, WINDOW_END],
        "scan_by_source": [row for row in source_scan if row["partition"] is None],
        "scanned_partitions_with_window_seeds": [
            row for row in source_scan if row["partition"] and row["window_seed_rows"]
        ],
        "seeded_copies_by_source_partition": rows(db, """
            SELECT context, partition, count(*) AS copies
            FROM event_copies GROUP BY context, partition ORDER BY context, partition
        """),
        "reconciliation": rows(db, """
            SELECT membership, action_type, action_date, count(*) AS actions,
                   sum(copies)::BIGINT AS copies, sum(copies - 1)::BIGINT AS duplicate_copies,
                   count(*) FILTER (WHERE conflicting_times) AS conflicting_times,
                   count(*) FILTER (WHERE conflicting_sharers) AS conflicting_sharers,
                   count(*) FILTER (WHERE conflicting_targets) AS conflicting_targets,
                   count(*) FILTER (WHERE missing_types > 0) AS with_missing_type,
                   count(*) FILTER (WHERE missing_times > 0) AS with_missing_time,
                   count(*) FILTER (WHERE missing_sharers > 0) AS with_missing_sharer,
                   count(*) FILTER (WHERE repost_copies > 0 AND missing_targets > 0)
                     AS repost_candidates_with_missing_reference
            FROM ledger GROUP BY ALL ORDER BY ALL
        """),
        "coverage": rows(db, f"""
            SELECT cast(day AS VARCHAR) AS day, interval, membership, {metrics}
            FROM coverage GROUP BY GROUPING SETS
                ((day, interval, membership), (day, interval), (interval, membership), (interval),
                 (membership), ()) ORDER BY day, interval, membership
        """),
        "coverage_by_target_reuse": rows(db, f"""
            SELECT interval, target_reuse, {metrics}
            FROM coverage GROUP BY interval, target_reuse ORDER BY interval, target_reuse
        """),
        "coverage_by_sharer_activity": rows(db, f"""
            SELECT interval, membership,
                   CASE WHEN action_count = 1 THEN '1'
                        WHEN action_count <= 9 THEN '2–9'
                        WHEN action_count <= 99 THEN '10–99'
                        WHEN action_count >= 100 THEN '100+' END AS sharer_activity,
                   {metrics}
            FROM coverage LEFT JOIN sharer_activity USING (interval, sharer)
            GROUP BY ALL ORDER BY interval, membership, sharer_activity
        """),
    }
    total = output["coverage"][-1]
    assert total["reposts"] == sum(
        total[key] for key in ("reference_unavailable", "original_absent", "author_missing",
                               "conflicting_authors", "target_is_repost", "unique_author")
    )
    assert sum(row["window_seed_rows"] - row["missing_ids_in_window"]
               for row in output["scan_by_source"]) <= sum(
        row["copies"] for row in output["reconciliation"]
    )
    assert sum(row["copies"] for row in output["seeded_copies_by_source_partition"]) == sum(
        row["copies"] for row in output["reconciliation"]
    )
    assert total["reposts"] == sum(
        row["reposts"] for row in output["coverage"] if row["day"] is not None and row["membership"] is None
    )
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("work_dir", type=Path, help="local directory for spill files")
    args = parser.parse_args()
    args.work_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    with duckdb.connect(config={
        "threads": 4, "memory_limit": "8GB", "preserve_insertion_order": False,
        "temp_directory": str(args.work_dir.resolve()),
    }) as db:
        print(json.dumps(audit(db, args.root.resolve()), indent=2))


if __name__ == "__main__":
    main()
