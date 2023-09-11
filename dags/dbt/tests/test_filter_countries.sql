SELECT row_count
FROM (
    SELECT COUNT(*) AS row_count
    FROM bank.filter_countries
    WHERE payer_country = 'NK' OR beneficiary_country = 'NK'
)
WHERE row_count > 0