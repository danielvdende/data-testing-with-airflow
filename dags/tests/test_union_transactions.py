def test_union_transactions(spark, environment):
    spark.sql("USE {0}_app".format(environment)).collect()

    # Check that we have all our transactions
    row_count_a = spark.sql("""
        SELECT
            COUNT(*) count_transaction_a
        FROM
            transaction_a.transactions
    """).format(environment).first().count_transaction_a

    row_count_b = spark.sql("""
        SELECT
            COUNT(*) count_transaction_b
        FROM
            transaction_b.transactions
    """).format(environment).first().count_transaction_b

    row_count_union = spark.sql("""
        SELECT
            COUNT(*) count_union
        FROM
            union_transactions
    """).format(environment).first().count_union

    assert row_count_a + row_count_b == row_count_union
