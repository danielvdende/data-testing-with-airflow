def test_enrich_transactions(spark, environment):
    spark.sql("USE {0}_app".format(environment)).collect()

    # Make sure no North Koreans slipped through the DMZ
    assert spark.sql("""
    SELECT
    SUM(IF(payer_country IS NULL OR beneficiary_country IS NULL,1,0)) null_count
    FROM enrich_transactions
    """).first().null_count == 0
