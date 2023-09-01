"""Test integrity of dags."""

import importlib
import os

import pytest
from airflow import models as af_models
from airflow.utils.dag_cycle_tester import check_cycle

DAG_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'dags'
)

DAG_FILES = [f for f in os.listdir(DAG_PATH) if f.endswith('*.py')]


@pytest.mark.parametrize('dag_file', DAG_FILES)
def test_dag_integrity(dag_file):
    """Import dag files and check for DAG."""
    module_name, _ = os.path.splitext(dag_file)
    module_path = os.path.join(DAG_PATH, dag_file)
    mod_spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(module)

    dag_objects = [var for var in vars(module).values() if isinstance(var, af_models.DAG)]

    for dag in dag_objects:
        check_cycle(dag)
