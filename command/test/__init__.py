import typer

from back.model.image import ImageFormatEnum
from back.utils.gen.gallery import (
    generate_nested_20200_galleries,
    generate_nested_galleries,
    generate_simple_galleries,
)
from back.utils.gen.tag import generate_tag_attributes, generate_tags
from back.utils.keyword import KeywordParser
from command.logging import logger
from command.test.gallery import app as gallery
from command.test.route import app as route
from command.test.service import app as service
from command.test.video import app as video
from lib.typer import ZetsuBouTyper
from lib.uvicorn.files import get_watched_files

_help = """
Test the functions or services.
"""
app = ZetsuBouTyper(name="test", help=_help)

app.add_typer(gallery)
app.add_typer(route)
app.add_typer(service)
app.add_typer(video)


@app.command()
async def integration():
    await generate_tag_attributes()
    await generate_tags()

    await generate_simple_galleries()
    await generate_nested_galleries()
    await generate_nested_20200_galleries()

    logger.info("finished")


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
    filenames.sort()
    for filename in filenames:
        print(filename)


@app.command()
def list_image_formats():
    """
    List the image formats available in the system.
    """
    for f in ImageFormatEnum:
        print(f"{f.name} : {f.value}")
