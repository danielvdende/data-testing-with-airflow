import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow_dbt.operators.dbt_operator import DbtRunOperator, DbtTestOperator


# Configuration variables
THIS_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)))
SPARK_DIRECTORY = THIS_DIRECTORY + '/spark/'
DBT_DIRECTORY = THIS_DIRECTORY + '/dbt/'
TESTS_DIRECTORY = THIS_DIRECTORY + '/tests/'
ENV_CONFIG_PATH = THIS_DIRECTORY + '/environment.conf'
# need to go up to parent dag directory so we can switch to next environment
DAG_LOCATION = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SPARK_HOME = '/usr/spark'


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
    --data-urlencode '{message}' \
    {url}""".format(**payload_vars)

    slack_alert = BashOperator(
        task_id='slack_alert',
        dag=dag,
        bash_command=slack_cmd,
    )
    slack_alert.execute(context)


pytest_cmd = """
export PYTHONPATH=/usr/spark/python/:/usr/spark/python/lib/py4j-0.10.4-src.zip:{spark_directory} &&\
export SPARK_HOME={spark_home} &&\
export ENVIRONMENT={environment} &&\
export MASTER=local &&\
cd /usr/local/airflow &&\
python -m pytest {directory}{script}
"""


default_args = {
    'owner': 'Gandalf and Princess',
    'depends_on_past': False,
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2017, 12, 8)
    # 'on_failure_callback': send_slack_alert
}

dag = DAG(
    'awesome_dag',
    schedule_interval="@once",
    default_args=default_args,
    catchup=True
)

# Launch Spark Submit job to union transactions
union_transactions = SparkSubmitOperator(
    dag=dag,
    conn_id='spark_local',
    task_id='union_transactions',
    name="App: union transactions",
    application=os.path.join(SPARK_DIRECTORY, "union_transactions.py")
)

dbt_run = DbtRunOperator(
    dag=dag,
    task_id='dbt_run',
    dir=DBT_DIRECTORY
)

dbt_test = DbtTestOperator(
    dag=dag,
    task_id='dbt_test',
    dir=DBT_DIRECTORY
)

union_transactions >> dbt_run >> dbt_test

# # Test union transactions
# test_union_transactions = BashOperator(
#     task_id='test_union_transactions',
#     bash_command=pytest_cmd.format(
#         environment=ENVIRONMENT,
#         directory=TESTS_DIRECTORY,
#         spark_directory=SPARK_DIRECTORY,
#         script='test_union_transactions.py',
#         spark_home=SPARK_HOME),
#     dag=dag)
#
# # Launch Spark Submit job to enrich the transactions
# enrich_transactions = SparkSubmitOperator(
#     dag=dag,
#     conn_id='spark',
#     task_id='enrich_transactions',
#     name="App: enrich transactions",
#     application=os.path.join(SPARK_DIRECTORY, "enrich_transactions.py"),
#     application_args=['-e', "{0}".format(ENVIRONMENT)]
# )
#
# # Test enrich transactions
# test_enrich_transactions = BashOperator(
#     task_id='test_enrich_transactions',
#     bash_command=pytest_cmd.format(
#         environment=ENVIRONMENT,
#         directory=TESTS_DIRECTORY,
#         spark_directory=SPARK_DIRECTORY,
#         script='test_enrich_transactions.py',
#         spark_home=SPARK_HOME),
#     dag=dag)
#
# # Launch a Spark Submit job to filter out unwanted countries
# filter_countries = SparkSubmitOperator(
#     dag=dag,
#     conn_id='spark',
#     task_id='filter_countries',
#     name="App: filter countries",
#     application=os.path.join(SPARK_DIRECTORY, "filter_countries.py"),
#     application_args=['-e', "{0}".format(ENVIRONMENT)]
# )
#
# # Test filter countries
# test_filter_countries = BashOperator(
#     task_id='test_filter_countries',
#     bash_command=pytest_cmd.format(
#         environment=ENVIRONMENT,
#         directory=TESTS_DIRECTORY,
#         spark_directory=SPARK_DIRECTORY,
#         script='test_filter_countries.py',
#         spark_home=SPARK_HOME),
#     dag=dag)
#
# # Trigger the next environment based on current environment
# if ENVIRONMENT != 'prd':
#     if ENVIRONMENT == 'dev':
#         trigger_next_environment_deploy = TriggerDagRunOperator(task_id='trigger_next_environment_deploy',
#                                                                 python_callable=lambda context, dag_run: dag_run,
#                                                                 trigger_dag_id="awesome_dag_tst",
#                                                                 dag=dag)
#         trigger_next_environment_deploy.set_upstream(test_filter_countries)
#
#     elif ENVIRONMENT == 'tst':
#         trigger_next_environment_deploy = TriggerDagRunOperator(task_id='trigger_next_environment_deploy',
#                                                                 python_callable=lambda context, dag_run: dag_run,
#                                                                 trigger_dag_id="awesome_dag_acc",
#                                                                 dag=dag)
#         trigger_next_environment_deploy.set_upstream(test_filter_countries)
#
# # Set order of tasks
# union_transactions.set_downstream(test_union_transactions)
# test_union_transactions.set_downstream(enrich_transactions)
# enrich_transactions.set_downstream(test_enrich_transactions)
# test_enrich_transactions.set_downstream(filter_countries)
# filter_countries.set_downstream(test_filter_countries)
