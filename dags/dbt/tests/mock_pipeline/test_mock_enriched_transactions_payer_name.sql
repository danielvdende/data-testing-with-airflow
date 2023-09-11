SELECT payer_name
FROM bank.enriched_transactions
WHERE payer_account='BE31199386628955' AND NOT payer_name='Vlaamse Patat'
