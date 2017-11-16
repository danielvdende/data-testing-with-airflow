FROM puckel/docker-airflow

ADD dags/dev/airflowfile.py /usr/local/airflow/dags/
ADD dags/tst/airflowfile.py /usr/local/airflow/dags/
ADD dags/acc/airflowfile.py /usr/local/airflow/dags/
ADD dags/prd/airflowfile.py /usr/local/airflow/dags/