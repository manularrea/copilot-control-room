-- Executable SQLite legacy fragment. Events were ingested before this query.
-- Business calendar is contractual UTC-05:00, not the database server's date.
-- Preserve refunds, currency partitioning and settled-only behavior.
SELECT currency,
       SUM(CASE WHEN kind = 'refund' THEN -amount_minor ELSE amount_minor END) AS total_minor
FROM ledger
WHERE status = 'settled'
  AND date(occurred_at, '-5 hours') = :business_day
GROUP BY currency
ORDER BY currency;
