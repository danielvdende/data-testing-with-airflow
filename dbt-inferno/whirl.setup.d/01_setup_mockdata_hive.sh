#!/usr/bin/env bash

echo "=========================="
echo "== Setup Mockdata       =="
echo "=========================="
spark-submit --name spark-data-generate \
             /opt/airflow/dags/dbt-inferno/spark/generate_data.py