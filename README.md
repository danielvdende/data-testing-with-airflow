# Data Testing With Airflow
[![Build Status](https://travis-ci.org/danielvdende/data-testing-with-airflow.svg?branch=master)](https://travis-ci.org/danielvdende/data-testing-with-airflow)

This repository contains simple examples of how to implement some of the Nine Circles of Data Tests described in our 
[blogpost](https://medium.com/@ingwbaa/datas-inferno-7-circles-of-data-testing-hell-with-airflow-cef4adff58d8). A docker container is provided to run the DTAP and Data Tests examples. The Mock Pipeline tests and
DAG integrity tests are implemented in Travis CI tests. 

## DAG Integrity Tests
The DAG Integrity tests are integrated in our CI pipeline, and check if the DAG definition in your airflowfile is a valid DAG.
This includes not only checking for typos, but also verifying there are no cycles in your DAGs, and that the operators are 
used correctly.

## Mock Pipeline Tests
Mock Pipeline Tests are implemented as a CI pipeline stage, and function as unit tests for your individual DAG tasks. Dummy
data is generated and used to verify that for each expected input, an expected output follows from your code.

## Data Tests
In the `dags` directory, you will find a simple DAG with 3 tasks. Each of these tasks has a companion test that is integrated
into the DAG. These tests are run on every DAG run and are meant to verify that your code makes sense when running on
real data.

## DTAP
In order to show our DTAP logic, we have included a Dockerfile, which builds a Docker image with Airflow and Spark installed.
We then clone this repo 4 times, to represent each environment. To build the docker image:

`docker build -t airflow_testing .`

Once built, you can run it with:

`docker run -p 8080:8080 airflow_testing`

This image contains all necessary logic to initialize the DAGs and connections. One part that is simulated is the promotion
of branches (i.e. environments). The 'promotion' of code from one branch (environment) to another requires write access to
the git repo, something which we don't want to provide publicly :-). To see the environments and triggering in action, kick off 
the 'dev' DAG via the UI (or CLI) to see flow. Please note, the prod DAG will not run after the acc one by default, as we 
prefer to use so called green-light deployments, to verify the logic and prevent unwanted production DAGruns.
