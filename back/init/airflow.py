import json
import subprocess

from packaging import version

from back.model.airflow import AirflowUser
from back.settings import DEFAULT_ADMIN_EMAIL, DEFAULT_SETTING_PATH, Setting, setting

AIRFLOW_CREATE_ADMIN = setting.airflow_create_admin
AIRFLOW_USERNAME = setting.airflow_username
AIRFLOW_PASSWORD = setting.airflow_password


def create_admin(
    username: str = AIRFLOW_USERNAME,
    password: str = AIRFLOW_PASSWORD,
    email: str = DEFAULT_ADMIN_EMAIL,
    first_name: str = "Admin",
    last_name: str = "User",
):
    output = subprocess.run(["airflow", "version"], capture_output=True)
    stdout = output.stdout
    v = stdout.decode("utf-8")

    if version.parse("2.4.0") <= version.parse(v) < version.parse("2.7.0"):
        subprocess.run(["airflow", "db", "init"])

    subprocess.run(
        [
            "airflow",
            "users",
            "create",
            "-e",
            email,
            "-f",
            first_name,
            "-l",
            last_name,
            "-u",
            username,
            "-p",
            password,
            "-r",
            "Admin",
        ]
    )


def init_airflow_simple(s: Setting):
    if AIRFLOW_CREATE_ADMIN:
        output = subprocess.run(
            ["airflow", "users", "list", "-o", "json"], capture_output=True
        )
        stdout = output.stdout
        stdout_str = stdout.decode("utf-8")
        us = json.loads(stdout_str)
        users = [AirflowUser(**u) for u in us]

        for user in users:
            if user.username == AIRFLOW_USERNAME and "Admin" in user.roles:
                break
        else:
            create_admin(
                username=s.airflow_username,
                password=s.airflow_password,
                email=DEFAULT_ADMIN_EMAIL,
            )
