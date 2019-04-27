import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType, StringType, DateType, BooleanType
from random import uniform, sample, randint
from datetime import date

SCHEMA_TRANSACTIONS = StructType([
    StructField('dt', DateType()),
    StructField('payer_account', StringType()),
    StructField('beneficiary_account', StringType()),
    StructField('amount', DoubleType())
])

SCHEMA_ACCOUNT_INFO = StructType([
    StructField('account', StringType()),
    StructField('name', StringType()),
    StructField('country', StringType())
])

SCHEMA_COUNTRIES = StructType([
    StructField('country', StringType()),
    StructField('allowed', BooleanType())
])

ACCOUNT_INFO_ROWS = [
    ("NL99INGB9999999999", "John Muller BV", "NL"),
    ("NL88RABO8888888888", "Kris Geusebroek NV", "NL"),
    ("NL29ABNA5612457383", "Super mooie laptops BV", "NL"),
    ("BE59587979732526", "Ahmet Erdem Belgian Investment", "BE"),
    ("BE31199386628955", "Vlaamse Patat", "BE"),
    ("BE29587431928864", "Gauffre Belgique", "BE"),
    ("PL84109024029551596171791699", "Polski Beat", "PL"),
    ("PL75109024026862879594797792", "Zywiec", "PL"),
    ("NK1", "Kim Jong Un Industries", "NK"),
    ("NK2", "Kim Jong Un Investment", "NK")
]


def generate_transactions(number):
    transactions = []
    for x in range(0, number):
        parties = sample(ACCOUNT_INFO_ROWS, 2)
        transactions.append((date(2017, 1, randint(1, 31)), parties[0][0], parties[1][0], round(uniform(0, 1000), 2)))
    return transactions


def populate_transaction_a(spark):
    transaction_rows = generate_transactions(1000)
    spark.createDataFrame(transaction_rows, SCHEMA_TRANSACTIONS) \
        .write.saveAsTable('transaction_a.transactions', format='parquet', mode='overwrite')


def populate_transaction_b(spark):
    transaction_rows = generate_transactions(1000)
    spark.createDataFrame(transaction_rows, SCHEMA_TRANSACTIONS) \
        .write.saveAsTable('transaction_b.transactions', format='parquet', mode='overwrite')


def populate_account_info(spark):
    account_info_rows = spark.sparkContext.parallelize(ACCOUNT_INFO_ROWS)
    spark.createDataFrame(account_info_rows, SCHEMA_ACCOUNT_INFO) \
        .write.saveAsTable('tst_app.account_info', format='parquet', mode='overwrite')


def populate_countries(spark):
    countries_rows = spark.sparkContext.parallelize([
        ("NK", False),  # North Korea
        ("PL", False),  # Poland (bank secrecy)
        ("NL", True),   # Netherlands
        ("BE", True)    # Belgium
    ])
    spark.createDataFrame(countries_rows, SCHEMA_COUNTRIES) \
        .write.saveAsTable('tst_app.countries', format='parquet', mode='overwrite')


@pytest.fixture(scope='session')
def spark(request):
    spark = SparkSession.builder \
        .master('local[*]') \
        .enableHiveSupport() \
        .getOrCreate()

    # Now populate some tables
    for database_name in ['tst_app', 'transaction_a', 'transaction_b']:
        spark.sql('DROP DATABASE IF EXISTS {0} CASCADE'.format(database_name)).collect()
        spark.sql('CREATE DATABASE {0}'.format(database_name))

    populate_transaction_a(spark)
    populate_transaction_b(spark)
    populate_account_info(spark)
    populate_countries(spark)

    return spark
