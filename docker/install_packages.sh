#!/usr/bin/env bash
sudo apt-get install -y libsasl2-dev build-essential vim
pip install dbt-spark[PyHive]==1.7.0b1 dbt-core==1.7.0b1 pytest

# agate==1.6.1 dbt-core airflow-dbt