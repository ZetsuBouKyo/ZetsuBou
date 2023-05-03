from pathlib import Path

from back.env import Env

default_env_path = Path(".env")


def test_env():
    env = Env(_env_file=str(default_env_path))
    env_json = env.json(indent=4, ensure_ascii=False)
    print(env_json)
