FROM python:3.6

RUN update-ca-certificates -f \
  && apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y \
    wget \
    git \
    libatlas3-base \
    libopenblas-base \
  && apt-get clean \
&& git config --global http.sslverify false

RUN pip install --upgrade pip \
&& pip install airflow pyspark --quiet

RUN airflow initdb

# dev
RUN cd /usr/local/airflow/dags && git clone https://github.com/danielvdende/data-testing-with-airflow.git development && cd development && git checkout origin/development

# tst
#RUN

# acc
#RUN

# prd
#RUN

# TODO: this needs to change to 4 git checkouts, each of a different branch.
#ADD dags/dev/airflowfile.py /usr/local/airflow/dags/
#ADD dags/tst/airflowfile.py /usr/local/airflow/dags/
#ADD dags/acc/airflowfile.py /usr/local/airflow/dags/
#ADD dags/prd/airflowfile.py /usr/local/airflow/dags/