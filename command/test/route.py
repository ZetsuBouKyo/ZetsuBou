import typer
from fastapi.params import Security

from back.api import router as api
from lib.typer import ZetsuBouTyper

_help = """
Test the services.
"""
app = ZetsuBouTyper(name="route", help=_help)


@app.command()
def get_routes():
    for route in api.routes:
        print(route)
        for dep in route.dependencies:
            if type(dep) == Security:
                print(dep.scopes)
