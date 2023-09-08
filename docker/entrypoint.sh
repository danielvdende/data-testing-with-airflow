#!/usr/bin/env bash
# Might be empty
AIRFLOW_COMMAND="singlemachine"

if [[ ${AIRFLOW_COMMAND} == "scheduler" || ${AIRFLOW_COMMAND} == "webserver" ]]; then
  echo  "wait a while for the other systems to be started"
  sleep 15
fi

if [[ ${AIRFLOW_COMMAND} == "scheduler" || ${AIRFLOW_COMMAND} == "singlemachine" ]]; then
  echo "========================================="
  echo "== Reset Airflow ========================"
  echo "========================================="
  rm -rf ${AIRFLOW_HOME}/*.pid
  rm -rf ${AIRFLOW_HOME}/*.err
  rm -rf ${AIRFLOW_HOME}/*.log
  rm -rf ${AIRFLOW_HOME}/logs/*
  echo "y" | airflow db reset
  airflow users create --username admin --password admin --firstname Anonymous --lastname Admin --role Admin --email admin@example.org
else
  if [[ ${AIRFLOW_COMMAND} == "webserver" || ${AIRFLOW_COMMAND} == "triggerer" ]]; then
    echo "wait a bit more to let the scheduler do the database reset."
    sleep 30
  fi
fi

. "/add_spark_config.sh"
. "/install_packages.sh"
. "/setup_mockdata.sh"

nohup /entrypoint scheduler -D &
nohup /entrypoint triggerer -D &
/entrypoint webserver -p 5000