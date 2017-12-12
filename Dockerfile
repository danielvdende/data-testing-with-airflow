# VERSION 1.8.1-1
# AUTHOR: Matthieu "Puckel_" Roisil
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t puckel/docker-airflow .
# SOURCE: https://github.com/puckel/docker-airflow

FROM python:3.6
MAINTAINER Puckel_

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_VERSION=1.8.2
ARG AIRFLOW_HOME=/usr/local/airflow
ENV AIRFLOW_HOME=/usr/local/airflow

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN set -ex \
    && buildDeps=' \
        python3-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        build-essential \
        libblas-dev \
        liblapack-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        python3-pip \
        python3-requests \
        apt-utils \
        curl \
        netcat \
        locales \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow \
    && python -m pip install -U pip setuptools wheel \
    && pip install Cython \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install apache-airflow[crypto,celery,postgres,hive,jdbc]==$AIRFLOW_VERSION \
    && pip install celery[redis]==3.1.17 \
    && pip install pyspark \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY docker_files/entrypoint.sh /entrypoint.sh
COPY docker_files/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

RUN chown -R airflow: ${AIRFLOW_HOME}
RUN chown airflow: /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8080 5555 8793

WORKDIR ${AIRFLOW_HOME}
# dev
RUN mkdir -p ${AIRFLOW_HOME}/dags
RUN cd ${AIRFLOW_HOME}/dags && git clone https://github.com/danielvdende/data-testing-with-airflow.git development
RUN cd ${AIRFLOW_HOME}/dags/development && git checkout development

# tst
RUN cd ${AIRFLOW_HOME} && git clone https://github.com/danielvdende/data-testing-with-airflow.git test
RUN cd ${AIRFLOW_HOME}/test && git checkout test
#
## acc
RUN cd ${AIRFLOW_HOME} && git clone https://github.com/danielvdende/data-testing-with-airflow.git acceptance
RUN cd ${AIRFLOW_HOME}/acceptance && git checkout acceptance
#
## prd
RUN cd ${AIRFLOW_HOME} && git clone https://github.com/danielvdende/data-testing-with-airflow.git production
RUN cd ${AIRFLOW_HOME}/production && git checkout master
RUN cd ${AIRFLOW_HOME} && ls
ENTRYPOINT /entrypoint.sh


#ADD dags/dev/airflowfile.py /usr/local/airflow/dags/
#ADD dags/tst/airflowfile.py /usr/local/airflow/dags/
#ADD dags/acc/airflowfile.py /usr/local/airflow/dags/
#ADD dags/prd/airflowfile.py /usr/local/airflow/dags/