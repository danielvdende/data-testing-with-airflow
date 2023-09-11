# Data Testing With Airflow

This repository contains simple examples of how to implement the 7 layers of Data Testing Hell as described initially in 2017 in [this blogpost]() and revisited in 2023 during a PyData talk. For reference, the original version of the examples has been tagged with `1.0.0`. The latest code on the main branch here is that of the 2023 version.

There are a few notable differences between the versions:
1. Dbt is used in the 2023 version to implement the data tests. This is a more modern approach than the original version, which used Spark directly.
2. Travis CI has been switched out in favour of Github Actions.
3. Some small fixes have been applied to update the Integrity Tests.
4. The compression used in the examples has been set to `gzip`. This is to workaround some issues encountered when running snappy encoding on M1 CPUs.

## Running locally
To run this locally, you can use the provided Dockerfile. First, build the Docker image (assumed path is the root of this project):
```shell
docker build -t datas_inferno .
```
and then run it with:
```shell
docker run -p 5000:5000 datas_inferno
```

## DAG Integrity Tests
The DAG Integrity tests are integrated in our CI pipeline, and check if your DAG definition is a valid DAG.
This includes not only checking for typos, but also verifying there are no cycles in your DAGs, and that the operators are 
used correctly.

## Mock Pipeline Tests
Mock Pipeline Tests should be as a CI pipeline stage, and function as unit tests for your individual DAG tasks. Dummy
data is generated and used to verify that for each expected input, an expected output follows from your code. Because we use dbt, this is a simple additional target in our dbt project, which ensures that the same logic is applied to a specific set of data. There were some issues getting dbt to talk to the right spark-warehouse and hive metastore in github actions. Workarounds are being looked at to resolve this, this is unrelated to the concept, but rather related to the specific environment setup.

## Data Tests
Data tests are implemented in dbt in a similar way to the integrity tests.
