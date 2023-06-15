from enum import Enum


class ServiceEnum(str, Enum):
    AIRFLOW: str = "airflow"
    ELASTICSEARCH: str = "elasticsearch"
    POSTGRES: str = "postgres"
    REDIS: str = "redis"
    STORAGE: str = "storage"
