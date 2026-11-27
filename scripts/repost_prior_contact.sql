-- Inputs and eligibility are defined in docs/reports/repost-intermediaries.md.
-- Each input action has already been reconciled. Times are whole UTC seconds.
WITH quote_contacts AS (
    SELECT r.respondent_id, r.reply_sec, q.quoter_id, q.item_id, q.quote_sec
    FROM direct_replies AS r
    JOIN quote_posts AS q ON q.quote_id = r.target_id
    WHERE q.quote_sec < r.reply_sec
),
witnesses AS (
    SELECT DISTINCT f.repost_id, c.quoter_id
    FROM focal_reposts AS f
    JOIN quote_contacts AS c
      ON c.respondent_id = f.sharer_id AND c.item_id = f.item_id
    CROSS JOIN contact_window AS w
    WHERE f.item_sec < c.quote_sec
      AND c.reply_sec < f.repost_sec
      AND f.repost_sec - c.reply_sec <= w.seconds
      AND f.sharer_id <> f.author_id
      AND c.quoter_id <> f.author_id AND c.quoter_id <> f.sharer_id
)
SELECT f.repost_id,
       CASE WHEN f.sharer_id IS NULL OR f.author_id IS NULL THEN 'unresolved endpoint'
            WHEN f.sharer_id = f.author_id THEN 'self'
            WHEN gs.group_id IS NULL OR ga.group_id IS NULL THEN 'unassigned endpoint'
            WHEN gs.group_id = ga.group_id THEN 'within'
            ELSE 'between' END AS endpoint_relation,
       CASE WHEN f.history_seconds >= w.seconds THEN 1 ELSE 0 END AS full_lookback,
       COUNT(b.quoter_id) AS contacts,
       COUNT(CASE WHEN gb.group_id = gs.group_id THEN 1 END) AS inside_contacts,
       COUNT(CASE WHEN gb.group_id <> gs.group_id THEN 1 END) AS outside_contacts,
       COUNT(CASE WHEN b.quoter_id IS NOT NULL
                   AND (gb.group_id IS NULL OR gs.group_id IS NULL) THEN 1 END)
           AS unclassified_contacts
FROM focal_reposts AS f
CROSS JOIN contact_window AS w
LEFT JOIN witnesses AS b ON b.repost_id = f.repost_id
LEFT JOIN frozen_groups AS gs ON gs.account_id = f.sharer_id
LEFT JOIN frozen_groups AS ga ON ga.account_id = f.author_id
LEFT JOIN frozen_groups AS gb ON gb.account_id = b.quoter_id
GROUP BY f.repost_id, f.sharer_id, f.author_id, f.history_seconds, w.seconds,
         gs.group_id, ga.group_id;
