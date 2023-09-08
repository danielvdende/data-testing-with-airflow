ARG AIRFLOW_VERSION=2.7.0
ARG PYTHON_VERSION=3.10
FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

USER root

ARG AIRFLOW_VERSION=2.7.0
ENV AIRFLOW_VERSION=${AIRFLOW_VERSION}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN echo "airflow ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER airflow
EXPOSE 5000

COPY --chown=airflow:root docker/entrypoint.sh /entrypoint-custom.sh
RUN chmod +x /entrypoint-custom.sh
COPY --chown=airflow:root docker/add_spark_config.sh /add_spark_config.sh
RUN chmod +x /add_spark_config.sh
COPY --chown=airflow:root docker/install_packages.sh /install_packages.sh
RUN chmod +x /install_packages.sh
COPY --chown=airflow:root docker/setup_mockdata.sh /setup_mockdata.sh
RUN chmod +x /setup_mockdata.sh

COPY --chown=airflow:root dbt-inferno/ /opt/airflow/dags/

ENV PATH="${PATH}:/home/airflow/.local/bin"
ENTRYPOINT ["/entrypoint-custom.sh"]
CMD ["airflow", "--help"]