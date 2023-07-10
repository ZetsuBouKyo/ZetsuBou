from lib.typer import ZetsuBouTyper

from .setting import app as setting
from .statics import app as statics

_help = """
Build document or intermediate components during developing, publishing, and so on.
"""

app = ZetsuBouTyper(name="build", help=_help)

app.add_typer(setting)
app.add_typer(statics)
