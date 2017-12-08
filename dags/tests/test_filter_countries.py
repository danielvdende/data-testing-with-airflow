def test_absence_known_pi(spark, environment):
    spark.sql("USE {0}_app".format(environment)).collect()

    # Make sure no North Koreans slipped through the DMZ
    assert spark.sql("""
    SELECT
    SUM(IF(payer_country = 'NK' OR beneficiary_country='NK' = TRUE,1,0)) nk_count
    FROM filter_countries
    """).first().nk_count == 0
