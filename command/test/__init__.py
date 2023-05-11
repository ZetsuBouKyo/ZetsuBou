import typer
from command.test.gallery import app as gallery

_help = """
Build the testing cases.
"""
app = typer.Typer(name="test", help=_help)

app.add_typer(gallery)
