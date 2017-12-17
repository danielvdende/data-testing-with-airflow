# -*- coding: utf-8 -*-

import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator

# Configuration variables
THIS_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)))
SPARK_DIRECTORY = THIS_DIRECTORY + '/spark/'
TESTS_DIRECTORY = THIS_DIRECTORY + '/tests/'
ENV_CONFIG_PATH = THIS_DIRECTORY + '/environment.conf'
# need to go up to parent dag directory so we can switch to next environment
DAG_LOCATION = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

with open(ENV_CONFIG_PATH, 'r') as environment_file:
    ENVIRONMENT = environment_file.read().lower().strip()


# Send a slack alert on failure
def send_slack_alert(context=None):
    """Send slack alert on failure to alert the team"""
    payload_vars = {
        'url': 'your_slack_hook_url_here',
        'run_id': str(context['run_id']),
        'task': str(context['task']),
        'dag_name': str(context['dag'].dag_id)
    }

    error_message = "{dag_name} Failure! Task failed: {task} Check log at: {run_id}".format(**payload_vars)
    payload_vars['json'] = """payload={{"channel":"ChuckNorris","text":"{0}"}}""".format(error_message)

    slack_cmd = """curl -x proxy:port \
    -X POST \
    --data-urlencode '{json}' \
    {url}""".format(**payload_vars)

    slack_alert = BashOperator(
        task_id='slack_alert',
        dag=dag,
        bash_command=slack_cmd,
    )
    slack_alert.execute(context)


default_args = {
    'owner': 'Gandalf and Princes',
    'depends_on_past': False,
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2017, 12, 8),
    'on_failure_callback': send_slack_alert
}

dag = DAG(
    'awesome_dag_{}'.format(ENVIRONMENT),
    schedule_interval="@once",
    default_args=default_args,
    catchup=False
)

# Launch Spark Submit job to union transactions
union_transactions = SparkSubmitOperator(
    dag=dag,
    task_id='union_transactions',
    name="App: union transactions",
    application=os.path.join(SPARK_DIRECTORY, "union_transactions.py"),
    application_args=['-e', "{0}".format(ENVIRONMENT)]
)

# Test union transactions
test_union_transactions = BashOperator(
    task_id='test_union_transactions',
    bash_command='export ENVIRONMENT={environment} && python -m pytest {directory}{script}'.format(
        environment=ENVIRONMENT,
        directory=TESTS_DIRECTORY,
        script='test_union_transactions.py'),
    dag=dag)

# Launch Spark Submit job to enrich the transactions
enrich_transactions = SparkSubmitOperator(
    dag=dag,
    task_id='enrich_transactions',
    name="App: enrich transactions",
    application=os.path.join(SPARK_DIRECTORY, "enrich_transactions.py"),
    application_args=['-e', "{0}".format(ENVIRONMENT)]
)

# Test enrich transactions
test_enrich_transactions = BashOperator(
    task_id='test_enrich_transactions',
    bash_command='export ENVIRONMENT={environment} && python -m pytest {directory}{script}'.format(
        environment=ENVIRONMENT,
        directory=TESTS_DIRECTORY,
        script='test_enrich_transactions.py'),
    dag=dag)

# Launch a Spark Submit job to filter out unwanted countries
filter_countries = SparkSubmitOperator(
    dag=dag,
    task_id='filter_countries',
    name="App: filter countries",
    application=os.path.join(SPARK_DIRECTORY, "filter_countries.py"),
    application_args=['-e', "{0}".format(ENVIRONMENT)]
)

# Test filter countries
test_filter_countries = BashOperator(
    task_id='test_filter_countries',
    bash_command='export ENVIRONMENT={environment} && python -m pytest {directory}{script}'.format(
        environment=ENVIRONMENT,
        directory=TESTS_DIRECTORY,
        script='test_filter_countries.py'),
    dag=dag)

# Trigger the next environment based on current environment
if ENVIRONMENT != 'prd':
    if ENVIRONMENT == 'dev':
        trigger_next_environment_deploy = TriggerDagRunOperator(task_id='trigger_next_environment_deploy',
                                                                python_callable=lambda context, dag_run: dag_run,
                                                                trigger_dag_id="app_tst",
                                                                dag=dag)
        trigger_next_environment_deploy.set_upstream(test_filter_countries)

    elif ENVIRONMENT == 'tst':
        trigger_next_environment_deploy = TriggerDagRunOperator(task_id='trigger_next_environment_deploy',
                                                                python_callable=lambda context, dag_run: dag_run,
                                                                trigger_dag_id="app_acc",
                                                                dag=dag)
        trigger_next_environment_deploy.set_upstream(test_filter_countries)

# Set order of tasks
union_transactions.set_downstream(test_union_transactions)
test_union_transactions.set_downstream(enrich_transactions)
enrich_transactions.set_downstream(test_enrich_transactions)
test_enrich_transactions.set_downstream(filter_countries)
filter_countries.set_downstream(test_filter_countries)
