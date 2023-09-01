"""
    py.test fixture for creating a pyspark context for all tests
"""

import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark(request):
    """
    Fixture to create the SparkSession.
    """
    spark = SparkSession.builder \
        .config('spark.sql.warehouse.dir', '/opt/airflow/spark_warehouse') \
        .config('spark.hadoop.javax.jdo.option.ConnectionURL',
                'jdbc:derby:;databaseName=/opt/airflow/metastore_db;create=true') \
        .enableHiveSupport() \
        .getOrCreate()

    request.addfinalizer(spark.stop)

    return spark

