SELECT null_count
FROM (
    SELECT COUNT(*) AS null_count
    FROM bank.enriched_transactions
    WHERE payer_country IS NULL OR beneficiary_country IS NULL
)
WHERE null_count >0
