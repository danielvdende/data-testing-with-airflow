import os
import pytest
import sqlalchemy as sa
from airflow import configuration, models
from airflow.utils import db

# pylint:disable=redefined-outer-name

TEST_AIRFLOW_HOME = os.path.join(
    os.path.dirname(__file__),
    'test_airflow_home',
)
TEST_ENV_VARS = {
    'AIRFLOW_HOME': TEST_AIRFLOW_HOME
}

APP_NAME = 'pytest-airflow-dag-integrity-sdp-ingestion-tests'


def pytest_configure(config):
    """Configure and init envvars for airflow."""
    # configuration.load_test_config()
    config.old_env = {}
    for key, value in TEST_ENV_VARS.items():
        config.old_env[key] = os.getenv(key)
        os.environ[key] = value
    # define some models to get the tests to pass.
    db.merge_conn(
        models.Connection(
            conn_id='ingestion_server', conn_type='ssh',
            host='http://localhost')
    )


def pytest_unconfigure(config):
    """Restore envvars to old values."""
    for key, value in config.old_env.items():
        if value is None:
            del os.environ[key]
        else:
            os.environ[key] = value
