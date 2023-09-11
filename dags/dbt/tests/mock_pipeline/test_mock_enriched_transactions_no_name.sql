-- Neither of these accounts should appear
SELECT *
FROM bank.enriched_transactions
WHERE payer_account='NL00XXXX0000000000' OR beneficiary_account='NL00XXXX0000000000'
