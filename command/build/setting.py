import typer
from back.settings import Setting, setting

_help = """
Manipulate the setting.
"""
app = typer.Typer(name="setting", help=_help)


@app.command()
def print_docker_envs():
    """
    Print the docker environment variables from Python code.
    """
    setting = Setting()
    env_prefix = setting.Config.env_prefix
    setting = setting.dict()
    keys = list(setting.keys())
    keys.sort()
    for key in keys:
        env_key = env_prefix + key
        env_key = env_key.upper()
        env_value = setting[key]
        if env_value is None:
            env_value = "null"
        env = f"{env_key}: ${{{env_key}:-{env_value}}}"
        print(env)


@app.command()
def print_setting():
    """
    Print setting in the form of JSON.
    """
    print(setting.json(indent=4))
