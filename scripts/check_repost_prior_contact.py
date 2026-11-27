"""Run the prior-contact query on fictional, already reconciled events."""
import sqlite3
from pathlib import Path


def check_fixture():
    db = sqlite3.connect(":memory:")
    db.executescript("""
        CREATE TABLE focal_reposts (
            repost_id TEXT PRIMARY KEY, sharer_id TEXT, item_id TEXT, author_id TEXT,
            item_sec INTEGER, repost_sec INTEGER, history_seconds INTEGER
        );
        CREATE TABLE quote_posts (
            quote_id TEXT PRIMARY KEY, quoter_id TEXT, item_id TEXT, quote_sec INTEGER
        );
        CREATE TABLE direct_replies (
            reply_id TEXT PRIMARY KEY, respondent_id TEXT, target_id TEXT, reply_sec INTEGER
        );
        CREATE TABLE frozen_groups (account_id TEXT PRIMARY KEY, group_id INTEGER);
        CREATE TABLE contact_window (seconds INTEGER);
        INSERT INTO contact_window VALUES (60);
    """)
    db.executemany("INSERT INTO frozen_groups VALUES (?, ?)", [
        ("A", 1), ("B", 2), ("C", 1), ("D", 1), ("E", 2),
    ])
    db.executemany("INSERT INTO quote_posts VALUES (?, ?, ?, ?)", [
        ("qb", "B", "p", 10), ("qb2", "B", "p", 11), ("qd", "D", "p", 12),
        ("qu", "U", "p", 13), ("qa", "A", "p", 14), ("qc", "C", "p", 15),
        ("other-item", "E", "other", 5), ("tie-quote-reply", "E", "p", 81),
        ("tie-item-quote", "E", "p", 0),
    ])
    db.executemany("INSERT INTO direct_replies VALUES (?, ?, ?, ?)", [
        ("h1", "C", "qb", 40), ("h2", "C", "qb2", 60), ("h3", "C", "qd", 65),
        ("h4", "C", "qu", 70), ("self", "C", "qc", 75), ("author", "C", "qa", 75),
        ("wrong-item", "C", "other-item", 80), ("tq", "C", "tie-quote-reply", 81),
        ("tp", "C", "tie-item-quote", 82), ("tr", "C", "qb", 100),
        ("future", "C", "qb", 101), ("wrong-target", "C", "thread-root", 80),
    ])
    db.executemany("INSERT INTO focal_reposts VALUES (?, ?, ?, ?, ?, ?, ?)", [
        ("mixed", "C", "p", "A", 0, 100, 200),
        ("clipped", "C", "p", "A", 0, 49, 20),
        ("time-tie", "C", "p", "A", 0, 40, 11),
        ("no-reply", "D", "p", "A", 0, 100, 200),
        ("late", "C", "p", "A", 0, 200, 200),
        ("repost-of-quote", "C", "qb", "B", 10, 100, 200),
        ("unknown-author", "C", "p", None, 0, 100, 200),
        ("no-item-clock", "C", "p", "A", None, 100, 200),
        ("self", "A", "p", "A", 0, 100, 200),
        ("unassigned", "U", "p", "A", 0, 100, 200),
    ])
    query = Path(__file__).with_name("repost_prior_contact.sql").read_text()

    def result():
        return {row[0]: row[1:] for row in db.execute(query)}

    # Relation, full lookback, distinct contacts, inside, outside, unclassified.
    expected = {
        "mixed": ("within", 1, 3, 1, 1, 1),
        "clipped": ("within", 0, 1, 0, 1, 0),
        "time-tie": ("within", 0, 0, 0, 0, 0),
        "no-reply": ("within", 1, 0, 0, 0, 0),
        "late": ("within", 1, 0, 0, 0, 0),
        "repost-of-quote": ("between", 1, 0, 0, 0, 0),
        "unknown-author": ("unresolved endpoint", 1, 0, 0, 0, 0),
        "no-item-clock": ("within", 1, 0, 0, 0, 0),
        "self": ("self", 1, 0, 0, 0, 0),
        "unassigned": ("unassigned endpoint", 1, 0, 0, 0, 0),
    }
    rows = result()
    assert rows == expected
    eligible = [row for row in rows.values() if row[:2] == ("within", 1)]
    assert len(eligible) == 4
    assert sum(row[3] + row[4] > 0 for row in eligible) == 1
    assert sum(row[4] > 0 for row in eligible) == 1
    db.execute("UPDATE contact_window SET seconds = 30")
    assert result()["mixed"] == ("within", 1, 1, 0, 0, 1)
    db.execute("UPDATE contact_window SET seconds = 29")
    assert result()["mixed"] == ("within", 1, 0, 0, 0, 0)
    db.execute("UPDATE contact_window SET seconds = 60")
    db.execute("DELETE FROM frozen_groups")
    without_groups = result()
    for name, row in expected.items():
        assert without_groups[name][2:] == (row[2], 0, 0, row[2])
    db.close()
    print("Verified ten fictional reposts, the lookback boundary and group-blind matching.")


if __name__ == "__main__":
    check_fixture()
