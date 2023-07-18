import typer

from back.utils.keyword import KeywordParser
from command.test.gallery import app as gallery
from command.test.service import app as service
from lib.typer import ZetsuBouTyper
from lib.uvicorn.files import get_watched_files

_help = """
Build the testing cases.
"""
app = ZetsuBouTyper(name="test", help=_help)

app.add_typer(gallery)
app.add_typer(service)


@app.command(name="parse-keywords")
def _parse_keywords(keywords: str = typer.Argument(..., help="Keywords.")):
    parser = KeywordParser()
    print(parser.parse(keywords=keywords))


@app.command()
def watch_files():
    filenames = get_watched_files()
    for filename in filenames:
        print(filename)
