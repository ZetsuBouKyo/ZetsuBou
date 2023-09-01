import inspect
from pathlib import Path

import typer
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from PIL import Image

from back.init.statics import STATICS_HOME, get_static_file
from lib.typer import ZetsuBouTyper

_help = """
Download the statics.
"""
app = ZetsuBouTyper(name="statics", help=_help)


def get_kwargs(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


@app.command()
async def download(
    statics_home: str = typer.Option(default=STATICS_HOME, help="Static home."),
):
    """
    Get static files from default values of FastAPI functions.
    """
    urls = []

    # get swagger statics
    key_swagger_js_url = "swagger_js_url"
    key_swagger_css_url = "swagger_css_url"
    swagger_kwargs = get_kwargs(get_swagger_ui_html)

    swagger_js_url = swagger_kwargs.get(key_swagger_js_url, None)
    if swagger_js_url is None:
        return
    swagger_js_url_map = f"{swagger_js_url}.map"

    swagger_css_url = swagger_kwargs.get(key_swagger_css_url, None)
    if swagger_css_url is None:
        return
    swagger_css_url_map = f"{swagger_css_url}.map"

    urls += [swagger_js_url, swagger_js_url_map, swagger_css_url, swagger_css_url_map]

    # get redoc statics
    key_redoc_js_url = "redoc_js_url"
    redoc_kwargs = get_kwargs(get_redoc_html)

    redoc_js_url = redoc_kwargs.get(key_redoc_js_url, None)
    if redoc_js_url is None:
        return
    redoc_js_url_map = f"{redoc_js_url}.map"

    urls += [redoc_js_url, redoc_js_url_map]

    for url in urls:
        await get_static_file(url, statics_home)


@app.command()
def favicon(
    source: str = typer.Argument(..., help="Source image."),
    out: str = typer.Argument(..., help="Output folder."),
):
    """
    Turn an image into a favicon.
    """
    _source = Path(source)
    if not _source.exists() or not _source.is_file():
        return
    _out = Path(out)
    if not _out.is_dir():
        return

    filepath = _out / "favicon.ico"

    img = Image.open(source)
    img.save(filepath)
