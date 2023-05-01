from pydantic import BaseModel


class Task(BaseModel):
    dag_id: str
    dag_kwargs: dict = {}
    sub_command: str
