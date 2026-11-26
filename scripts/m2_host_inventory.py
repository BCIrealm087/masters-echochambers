"""Inventory ITED-Br without exporting record-level data."""
import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pyarrow
import pyarrow.compute as pc
import pyarrow.parquet as pq

WINDOW = {f"2022_10_{day}" for day in range(16, 22)}
CONTEXTS = {"query_lula", "query_bolsonaro",
            "retweets_query_lula", "retweets_query_bolsonaro"}
FIELDS = ["id", "type", "created_at", "referenced_tweet_id", "author_id"]
SAO_PAULO = ZoneInfo("America/Sao_Paulo")
TYPES = {"retweeted", "tweeted", "quoted", "replied_to", "quoted, replied_to"}


def numeric(value):
    return bool(value and re.fullmatch(r"[1-9][0-9]{0,19}", value))


def inspect_rows(file, partition):
    counts = Counter()
    for batch in file.iter_batches(columns=FIELDS):
        for post, kind, created, reference, author in zip(
            *(column.to_pylist() for column in batch.columns)
        ):
            counts["rows"] += 1
            counts[f"type {kind}" if kind in TYPES else "type other or missing"] += 1
            counts["usable post ID"] += numeric(post)
            counts["usable row author"] += numeric(author)
            if kind == "retweeted":
                counts["reposts with single numeric reference"] += numeric(reference)
            try:
                stamp = datetime.fromisoformat(created)
                counts["timestamp parsed"] += 1
                counts["timestamp with explicit offset"] += stamp.tzinfo is not None
                if not numeric(post):
                    continue
                id_time = datetime.fromtimestamp(
                    ((int(post) >> 22) + 1288834974657) // 1000, timezone.utc
                )
                if stamp.replace(tzinfo=stamp.tzinfo or timezone.utc) != id_time:
                    continue
                counts["timestamp agrees with ID at UTC second"] += 1
                local_date = id_time.astimezone(SAO_PAULO).strftime("%Y_%m_%d")
                counts["São Paulo day agrees with partition"] += local_date == partition
                counts["São Paulo day in audit window"] += local_date in WINDOW
            except (TypeError, ValueError, OverflowError, OSError):
                continue
    return counts


def inspect_partition_offsets(root):
    """Count São Paulo date offsets, assuming the diagnosed UTC clock."""
    offsets = {}
    for context in sorted(CONTEXTS):
        for partition in sorted(WINDOW | {"2022_10_22"}):
            file = root / "tweets" / context / f"tweets-{context}-{partition}.parquet"
            if not file.is_file():
                continue
            timestamps = pq.read_table(file, columns=["created_at"])[0]
            utc = pc.strptime(timestamps, "%Y-%m-%d %H:%M:%S", unit="s",
                              error_is_null=True)
            # São Paulo was UTC−03:00 on every date examined here.
            local = pc.subtract(utc, pyarrow.scalar(10800, type=pyarrow.duration("s")))
            days = pc.cast(pc.floor_temporal(local, unit="day"), pyarrow.date32())
            partition_day = datetime.strptime(partition, "%Y_%m_%d").date()
            counts = Counter()
            for item in pc.value_counts(days).to_pylist():
                day = item["values"]
                offset = (day - partition_day).days if day else None
                key = str(offset) if offset in {-2, -1, 0} else "other"
                if offset is None:
                    key = "unparsed"
                counts[key] += item["counts"]
            offsets[f"{context}/{partition}"] = counts
    return offsets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--partition-offsets", action="store_true",
                        help="count action-date offsets through the October 22 partitions")
    args = parser.parse_args()
    if args.partition_offsets:
        print(json.dumps(inspect_partition_offsets(args.root), indent=2, sort_keys=True))
        return
    inventory = defaultdict(Counter)
    schemas = defaultdict(Counter)
    coverage = {}
    fingerprint = hashlib.sha256()
    for path in sorted(args.root.rglob("*.parquet")):
        family, context, filename = path.relative_to(args.root).parts
        partition = filename.removesuffix(".parquet").rsplit("-", 1)[-1]
        size = path.stat().st_size
        file = pq.ParquetFile(path)
        rows = file.metadata.num_rows
        schema = ", ".join(f"{field.name}:{field.type}" for field in file.schema_arrow)
        fingerprint.update(f"{family}/{context}/{filename}\t{size}\t{rows}\t{schema}\n".encode())
        summary = inventory[f"{family}/{context}"]
        summary.update(files=1, rows=rows, bytes=size, empty_files=int(rows == 0))
        schemas[family][schema] += 1
        if family == "tweets" and context in CONTEXTS and partition in WINDOW:
            coverage[f"{context}/{partition}"] = inspect_rows(file, partition)
    print(json.dumps(dict(pyarrow=pyarrow.__version__, footer_inventory_sha256=fingerprint.hexdigest(),
                          inventory=inventory, schemas=schemas, coverage=coverage),
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
