SELECT *
FROM bank.filter_countries
WHERE payer_country IN (
  SELECT country
  FROM bank.countries
  WHERE allowed = false
)