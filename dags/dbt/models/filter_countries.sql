{{ config(materialized='table') }}
SELECT
    t.*
FROM bank.enriched_transactions t
         LEFT JOIN bank.countries pc ON t.payer_country = pc.country
         LEFT JOIN bank.countries bc ON t.beneficiary_country = bc.country
WHERE
    pc.allowed AND bc.allowed
