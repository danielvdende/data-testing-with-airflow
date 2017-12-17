from dags.spark.union_transactions import union_transactions
from dags.spark.enrich_transactions import enrich_transactions


def test_enrich_transactions(spark):
    spark.sql("USE tst_app").collect()

    union_transactions(spark, "tst")
    enrich_transactions(spark, "tst")

    # check that account name is now available for specific accounts (payer side)
    assert spark.sql("""
        SELECT payer_name
        FROM enrich_transactions
        WHERE payer_account='BE31199386628955'
    """).first().payer_name == "Vlaamse Patat"

    # check that account name is now available for specific accounts (beneficiary side)
    assert spark.sql("""
        SELECT beneficiary
        FROM enrich_transactions
        WHERE payer_account='NL29ABNA5612457383'
    """).first().payer_name == "Super mooie laptops BV"

    # check that 'non-existent' accounts are not in enriched_transactions
    assert spark.sql("""
        SELECT COUNT(*) ct
        FROM enrich_transactions
        WHERE payer_account='NL00XXXX0000000000'
    """).first().ct == 0
