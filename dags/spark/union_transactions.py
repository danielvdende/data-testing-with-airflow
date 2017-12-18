import argparse

from pyspark.sql import SparkSession

APP_NAME = 'union-transactions'


def union_transactions(spark, environment):
    spark.sql("USE {0}_app".format(environment)).collect()

    # Merge all the transactions from the different data sources
    spark.sql("""
        SELECT * FROM transaction_a.transactions
        UNION ALL
        SELECT * FROM transaction_b.transactions
        """).write \
        .saveAsTable('transactions_union', format='parquet', mode='overwrite')


if __name__ == "__main__":
    # parse the parameters
    parser = argparse.ArgumentParser(description='Union Transactions')
    parser.add_argument('-e', dest='environment', action='store')
    arguments = parser.parse_args()
    # Init
    spark = SparkSession.builder \
        .appName(APP_NAME) \
        .config('spark.sql.warehouse.dir', '/usr/local/airflow/spark-warehouse')\
        .enableHiveSupport() \
        .getOrCreate()
    union_transactions(spark, arguments.environment)
