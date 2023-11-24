from back.model.airflow import AirflowDagCommandRequest
from back.session.async_airflow import get_args


def test_get_args():
    dag_id_1 = "sync-storage"
    data_1 = {
        "args": [{"type": "string", "value": "minio"}, {"type": "number", "value": 1}],
        "kwargs": [{"type": "boolean", "name": "force", "value": True}],
    }

    args_1 = AirflowDagCommandRequest(**data_1)
    cmd_1 = get_args(dag_id_1, command_request=args_1)
    assert cmd_1 == "minio 1 --force"

    dag_id_2 = "sync-storage"
    data_2 = {
        "args": [{"type": "string", "value": "minio"}, {"type": "number", "value": 1}],
        "kwargs": [{"type": "boolean", "name": "force", "key": "-f", "value": True}],
    }

    args_2 = AirflowDagCommandRequest(**data_2)
    cmd_2 = get_args(dag_id_2, command_request=args_2)
    assert cmd_2 == "minio 1 -f"
