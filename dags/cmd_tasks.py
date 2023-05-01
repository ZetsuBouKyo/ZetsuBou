from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

from model import Task

python_path = "/opt/airflow/zetsubou-venv/.venv/bin/python3"
cli_fname = "cli.py"
base_command = f"{python_path} {cli_fname}"

cwd = "/opt/airflow/zetsubou"


tasks = [
    Task(
        dag_id="sync-minio-storages",
        sub_command="sync sync_minio_storages",
        dag_kwargs={
            "start_date": datetime(2021, 1, 1),
            "schedule_interval": None,
            "catchup": False,
            "tags": ["sync", "minio"],
            "max_active_runs": 1,
        },
    ),
    Task(
        dag_id="sync-minio-storage",
        sub_command="sync sync_minio_storage",
        dag_kwargs={
            "start_date": datetime(2021, 1, 1),
            "schedule_interval": None,
            "catchup": False,
            "tags": ["sync", "minio"],
        },
    ),
    Task(
        dag_id="backup-dump",
        sub_command="backup dump",
        dag_kwargs={
            "start_date": datetime(2021, 1, 1),
            "schedule_interval": None,
            "catchup": False,
            "tags": ["backup"],
            "max_active_runs": 1,
        },
    ),
    Task(
        dag_id="backup-load",
        sub_command="backup load",
        dag_kwargs={
            "start_date": datetime(2021, 1, 1),
            "schedule_interval": None,
            "catchup": False,
            "tags": ["backup"],
            "max_active_runs": 1,
        },
    ),
]

try:
    import sys

    sys.path.append("/opt/airflow/zetsubou")
    from plugins.dags import plugin_tasks

    tasks += plugin_tasks
except ModuleNotFoundError:
    pass

for task in tasks:
    with DAG(dag_id=task.dag_id, **task.dag_kwargs) as dag:
        command = BashOperator(
            task_id=task.dag_id,
            cwd=cwd,
            bash_command=f"{base_command} {task.sub_command} "
            + '{{ dag_run.conf.get("args", "") }}',
            env={"PYTHONPATH": python_path},
        )

    globals()[task.dag_id] = dag
