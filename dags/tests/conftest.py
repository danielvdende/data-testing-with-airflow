"""
    py.test fixture for creating a pyspark context for all tests
"""

import pytest
import os
from pyspark.sql import SparkSession

# Name of the Spark application for running the tests
APP_NAME = 'App: Data test {0}'.format(os.environ['ENVIRONMENT'])


@pytest.fixture(scope="session")
def spark(request):
    """
    Fixture to create the SparkSession.
    """
    spark = SparkSession.builder \
        .appName(APP_NAME) \
        .config('spark.sql.warehouse.dir', '/usr/local/airflow/daniel_spark_warehouse') \
        .config('spark.hadoop.javax.jdo.option.ConnectionURL', 'jdbc:derby:;databaseName=/usr/local/airflow/daniel_metastore_db;create=true') \
        .enableHiveSupport() \
        .getOrCreate()

    request.addfinalizer(spark.stop)

    return spark


@pytest.fixture(scope="session")
def environment(request):
    """
    Fixture to pass the environment of the DTAP.
    """
    return os.environ['ENVIRONMENT']
