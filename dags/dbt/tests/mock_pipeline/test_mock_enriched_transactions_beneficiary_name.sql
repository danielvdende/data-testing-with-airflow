SELECT payer_name
FROM bank.enriched_transactions
WHERE beneficiary_account='NL29ABNA5612457383' AND NOT beneficiary_name='Super mooie laptops BV'
