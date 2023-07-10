from command.test.gallery import app as gallery
from command.test.service import app as service
from lib.typer import ZetsuBouTyper

_help = """
Build the testing cases.
"""
app = ZetsuBouTyper(name="test", help=_help)

app.add_typer(gallery)
app.add_typer(service)
