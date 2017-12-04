from airflow import DAG
from airflow.operators import BashOperator, TriggerDagRunOperator

ENV_CONFIG_PATH = "environment"

config = {
    # random transactions, no networks can be found
    "dev": {
        "message": "Hello from DEV!",
        "iterations": 1
    },
    # only certain grid's available, but their network should be correct
    "tst": {
        "message": "Hello from TST!",
        "iterations": 2
    },
    # all transactions for all companies available. Should be identical to prd.
    "acc": {
        "message": "Hello from ACC!",
        "iterations": 4
    },
    # all transactions for all companies available.
    "prd": {
        "message": "Hello from PRD!",
         "iterations": 4
    }
}


# Read environment
with open(ENV_CONFIG_PATH, 'r') as environment_file:
    ENVIRONMENT = environment_file.read().lower().strip()

if ENVIRONMENT == 'prd':
    YARN_QUEUE = 'root.production'
    DAG_SCHEDULE = "0 0 * * SUN,WED"
    DAG_SCHEDULE_CATCHUP = False
    SPARK_CONN_ID = 'spark_prod'


first_task = BashOperator(
    dag=dag,
    bash_command="""
        echo 'Hello there! Welcome to this DTAP example dag. You're looking at {environment}.'
    """.format(ENVIRONMENT)
)

promote_branch = BashOperator(
    dag=dag,
    bash_command="""
        
    """
)

for i in range(0, config[ENVIRONMENT]["iterations"]):
    do_stuff = BashOperator(
        dag=dag,
        bash_command="""
            echo 'Message from your config: {message}'
        """.format(config[ENVIRONMENT]["message"])
    )
    do_stuff.set_upstream(first_task)
    do_stuff.set_downstream(promote_branch)

trigger_next_env = TriggerDagRunOperator(
    dag=dag,
)

