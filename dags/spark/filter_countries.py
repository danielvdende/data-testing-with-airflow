import argparse

from pyspark.sql import SparkSession

APP_NAME = 'filter-countries'


def filter_countries(spark, environment):
    spark.sql("USE {0}_app".format(environment)).collect()

    # Filter out countries we don't want to analyse, if either side is not allowed, we filter the line out
    spark.sql("""
        SELECT
        t.*
        FROM enrich_transactions t
        LEFT JOIN countries pc ON t.payer_country = pa.country
        LEFT JOIN countries bc ON t.beneficiary_country = ba.country
        WHERE 
        pc.allowed AND bc.allowed
        """).format(environment).write \
        .saveAsTable('filter_countries', format='parquet', mode='overwrite')


if __name__ == "__main__":
    # parse the parameters
    parser = argparse.ArgumentParser(description='Filter Countries')
    parser.add_argument('-e', dest='environment', action='store')
    arguments = parser.parse_args()
    # Init
    spark = SparkSession.builder \
        .appName(APP_NAME) \
        .enableHiveSupport() \
        .getOrCreate()
    filter_countries(spark, arguments.environment)