import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.providers.slack.notifications.slack import send_slack_notification

# Configuration variables
THIS_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)))
SPARK_DIRECTORY = THIS_DIRECTORY + '/spark/'
DBT_DIRECTORY = THIS_DIRECTORY + '/dbt/'
SPARK_TESTS_DIRECTORY = SPARK_DIRECTORY + '/tests/'

default_args = {
    'owner': 'Gandalf and Princess',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2017, 12, 8),
    'on_failure_callback': send_slack_notification(
        text="The task {{ ti.task_id }} failed",
        channel="#alerts",
        username="Chuck Norris"
    )
}

dag = DAG(
    'awesome_dag',
    schedule_interval='@once',
    default_args=default_args,
    catchup=True
)

# Launch Spark Submit job to union transactions
union_transactions = SparkSubmitOperator(
    dag=dag,
    conn_id='spark_local',
    task_id='union_transactions',
    name='App: union transactions',
    application=os.path.join(SPARK_DIRECTORY, 'union_transactions.py')
)

test_union_transactions = BashOperator(
    task_id='test_union_transactions',
    bash_command=f'python -m pytest {SPARK_TESTS_DIRECTORY}test_union_transactions.py',
    dag=dag)

dbt_run = BashOperator(
    dag=dag,
    task_id='dbt_run',
    bash_command='dbt run',
    cwd=DBT_DIRECTORY
)

dbt_test = BashOperator(
    dag=dag,
    task_id='dbt_test',
    bash_command='dbt test',
    cwd=DBT_DIRECTORY
)

union_transactions >> test_union_transactions >> dbt_run >> dbt_test
