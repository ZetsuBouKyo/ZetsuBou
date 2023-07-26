import typer

from back.model.image import ImageFormatEnum
from back.utils.keyword import KeywordParser
from command.test.gallery import app as gallery
from command.test.service import app as service
from lib.typer import ZetsuBouTyper
from lib.uvicorn.files import get_watched_files

_help = """
Test the functions or services.
"""
app = ZetsuBouTyper(name="test", help=_help)

app.add_typer(gallery)
app.add_typer(service)


@app.command(name="parse-keywords")
def _parse_keywords(keywords: str = typer.Argument(..., help="Keywords.")):
    """
    Parse the keywords.
    """
    parser = KeywordParser()
    print(parser.parse(keywords=keywords))


@app.command()
def watch_files():
    """
    Get all watched files.
    """
    filenames = get_watched_files()
    for filename in filenames:
        print(filename)


@app.command()
def list_image_formats():
    """
    List the image formats available in the system.
    """
    for f in ImageFormatEnum:
        print(f"{f.name} : {f.value}")
