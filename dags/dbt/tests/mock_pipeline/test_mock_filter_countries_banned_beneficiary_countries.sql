SELECT *
FROM bank.filter_countries
WHERE beneficiary_country IN (
  SELECT country
  FROM bank.countries
  WHERE allowed = false
)