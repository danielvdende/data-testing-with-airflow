import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope='session')
def spark(request):
    spark = SparkSession.builder \
        .master('local[*]') \
        .enableHiveSupport() \
        .getOrCreate()

    # Now populate some tables
    for database_name in ['application', 'source_a', 'source_b', 'source_c']:
        spark.sql('DROP DATABASE IF EXISTS {0} CASCADE'.format(database_name)).collect()
        spark.sql('CREATE DATABASE {0}'.format(database_name))

    return spark