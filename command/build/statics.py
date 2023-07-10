import typer
from back.init.statics import get_static_file

from lib.typer import ZetsuBouTyper

_help = """
Download the statics.
"""
app = ZetsuBouTyper(name="statics", help=_help)


@app.command()
async def download(
    url: str = typer.Argument(..., help="Static url."),
    statics_home: str = typer.Argument(..., help="Static home."),
):
    await get_static_file(url, statics_home)
