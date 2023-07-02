import typer
from command.test.gallery import app as gallery
from command.test.service import app as service

_help = """
Build the testing cases.
"""
app = typer.Typer(name="test", help=_help)

app.add_typer(gallery)
app.add_typer(service)
