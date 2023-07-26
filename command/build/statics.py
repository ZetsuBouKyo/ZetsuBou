import typer
from back.init.statics import get_static_file
from PIL import Image
from pathlib import Path
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
    """
    Get static files via URL.
    """
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
