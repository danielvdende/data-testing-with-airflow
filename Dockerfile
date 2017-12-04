FROM puckel/docker-airflow

# TODO: this needs to change to 4 git checkouts, each of a different branch.
ADD dags/dev/airflowfile.py /usr/local/airflow/dags/
ADD dags/tst/airflowfile.py /usr/local/airflow/dags/
ADD dags/acc/airflowfile.py /usr/local/airflow/dags/
ADD dags/prd/airflowfile.py /usr/local/airflow/dags/