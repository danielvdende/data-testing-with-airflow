import argparse

from pyspark.sql import SparkSession

APP_NAME = 'enrich-transactions'


def enrich_transactions(spark, environment):
    spark.sql("USE {0}_app".format(environment)).collect()

    # Enrich transactions with account info
    spark.sql("""
        SELECT
            t.dt                                dt,
            t.amount                            amount,
            t.payer_account                     payer_account,
            pa.name                             payer_name,
            pa.country                          payer_country,
            t.beneficiary_account               beneficiary_account,
            ba.name                             beneficiary_name,
            ba.country                          beneficiary_country
        FROM transactions_union t
        LEFT JOIN account_info pa ON t.payer_account = pa.account
        LEFT JOIN account_info ba ON t.beneficiary_account = ba.account
        """).write \
        .saveAsTable('enrich_transactions', format='parquet', mode='overwrite')


if __name__ == "__main__":
    # parse the parameters
    parser = argparse.ArgumentParser(description='Enrich Transactions')
    parser.add_argument('-e', dest='environment', action='store')
    arguments = parser.parse_args()
    # Init
    spark = SparkSession.builder \
        .appName(APP_NAME) \
        .enableHiveSupport() \
        .config('spark.sql.warehouse.dir', '/usr/local/airflow/spark_warehouse') \
        .config('spark.hadoop.javax.jdo.option.ConnectionURL',
                'jdbc:derby:;databaseName=/usr/local/airflow/metastore_db;create=true') \
        .getOrCreate()
    enrich_transactions(spark, arguments.environment)
