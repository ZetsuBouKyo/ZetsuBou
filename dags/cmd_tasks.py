from datetime import datetime

from airflow import DAG  # type: ignore
from airflow.operators.bash import BashOperator  # type: ignore
from model import Task

PYTHON_PATH = "/opt/airflow/zetsubou-venv/.venv/bin/python3"
CLI_FNAME = "cli.py"
BASE_COMMAND = f"{PYTHON_PATH} {CLI_FNAME}"
ZETSUBOU_SETTING_PATH = "/opt/airflow/zetsubou/etc/settings.airflow.env"
CWD = "/opt/airflow/zetsubou"


tasks = [
    Task(
        dag_id="sync-minio-storages",
        sub_command="sync sync-minio-storages",
        dag_kwargs={
            "start_date": datetime(2021, 1, 1),
            "schedule_interval": None,
            "catchup": False,
            "tags": ["sync", "minio"],
            "max_active_runs": 1,
        },
    ),
    Task(
        dag_id="sync-storages",
        sub_command="sync storages",
        dag_kwargs={
            "start_date": datetime(2021, 1, 1),
            "schedule_interval": None,
            "catchup": False,
            "tags": ["sync", "storage"],
            "max_active_runs": 1,
        },
    ),
    Task(
        dag_id="sync-minio-storage",
        sub_command="sync sync-minio-storage",
        dag_kwargs={
            "start_date": datetime(2021, 1, 1),
            "schedule_interval": None,
            "catchup": False,
            "tags": ["sync", "minio"],
        },
    ),
    Task(
        dag_id="sync-storage",
        sub_command="sync storage",
        dag_kwargs={
            "start_date": datetime(2021, 1, 1),
            "schedule_interval": None,
            "catchup": False,
            "tags": ["sync", "storage"],
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
    Task(
        dag_id="video-generate-cover",
        sub_command="video generate-cover",
        dag_kwargs={
            "start_date": datetime(2021, 1, 1),
            "schedule_interval": None,
            "catchup": False,
            "tags": ["video"],
            "max_active_runs": 1,
        },
    ),
]

try:
    import sys

    sys.path.append("/opt/airflow/zetsubou")
    from plugins.dags import plugin_tasks  # type: ignore

    tasks += plugin_tasks
except ModuleNotFoundError:
    pass

for task in tasks:
    with DAG(dag_id=task.dag_id, **task.dag_kwargs) as dag:
        command = BashOperator(
            task_id=task.dag_id,
            cwd=CWD,
            bash_command=f"{BASE_COMMAND} {task.sub_command} "
            + '{{ dag_run.conf.get("args", "") }}',
            env={
                "PYTHONPATH": PYTHON_PATH,
                # See `/mnt/hdd1/project/ZetsuBou/back/model/envs.py`
                "ZETSUBOU_SETTING_PATH": ZETSUBOU_SETTING_PATH,
            },
        )

    globals()[task.dag_id] = dag
