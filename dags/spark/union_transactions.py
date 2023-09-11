from pyspark.sql import SparkSession

APP_NAME = 'union-transactions'


def union_transactions(spark):
    spark.sql("USE bank").collect()

    # Merge all the transactions from the different data sources
    spark.sql("""
        SELECT * FROM transaction_a.transactions
        UNION ALL
        SELECT * FROM transaction_b.transactions
        """).write \
        .saveAsTable('transactions_union', format='parquet', mode='overwrite')


if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName(APP_NAME) \
        .config('spark.sql.warehouse.dir', '/opt/airflow/spark-warehouse') \
        .config('spark.sql.parquet.compression.codec', 'gzip') \
        .config('spark.hadoop.javax.jdo.option.ConnectionURL',
                'jdbc:derby:;databaseName=/opt/airflow/metastore_db;create=true') \
        .enableHiveSupport() \
        .getOrCreate()
    union_transactions(spark)
