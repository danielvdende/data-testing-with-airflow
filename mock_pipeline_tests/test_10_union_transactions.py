from dags.spark.union_transactions import union_transactions


def test_union_transactions(spark):
    spark.sql("USE tst_app").collect()

    union_transactions(spark, "tst")

    # assert that all transactions are there
    assert spark.sql("""
        SELECT COUNT(*) ct
        FROM transactions_union
    """).first().ct == 2000
