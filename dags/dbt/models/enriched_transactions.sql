{{ config(materialized='table') }}
SELECT
    t.dt                                dt,
    t.amount                            amount,
    t.payer_account                     payer_account,
    pa.name                             payer_name,
    pa.country                          payer_country,
    t.beneficiary_account               beneficiary_account,
    ba.name                             beneficiary_name,
    ba.country                          beneficiary_country
FROM bank.transactions_union t
LEFT JOIN bank.account_info pa ON t.payer_account = pa.account
LEFT JOIN bank.account_info ba ON t.beneficiary_account = ba.account

