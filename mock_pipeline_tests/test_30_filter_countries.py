from dags.spark.union_transactions import union_transactions
from dags.spark.enrich_transactions import enrich_transactions
from dags.spark.filter_countries import filter_countries


def test_filter_countries(spark):
    spark.sql("USE tst_app").collect()
    union_transactions(spark, "tst")
    enrich_transactions(spark, "tst")
    filter_countries(spark, "tst")

    # check that banned countries are gone
    assert spark.sql("""
        SELECT COUNT(*) ct
        FROM filter_countries
        WHERE country IN (
          SELECT country
          FROM countries
          WHERE allowed = false
        )
    """).first().ct == 0

    # check that all transactions with valid countries in them are still in there.
