import typer

from .setting import app as setting

_help = """
Build document or intermediate components during developing, publishing, and so on.
"""

app = typer.Typer(name="build", help=_help)

app.add_typer(setting)
