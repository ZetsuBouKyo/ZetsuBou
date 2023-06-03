import json
import os
import shutil
import tempfile
from pathlib import Path
from uuid import uuid4

import typer
from pdf2image import convert_from_path

from back.model.gallery import Gallery as GalleryModel
from back.settings import setting
from back.utils.dt import get_now
from command.backup import app as backup
from command.build import app as build
from command.db import app as db
from command.elasticsearch import app as elasticsearch
from command.gallery import app as gallery
from command.migrate import app as migrate
from command.s3 import app as s3
from command.standalone import app as standalone
from command.sync import app as sync
from command.tag import app as tag
from command.test import app as test
from command.utils import is_empty_dir
from command.video import app as video

try:
    from plugins.cli import app as plugin  # type: ignore
except ModuleNotFoundError:
    plugin = None

dir_fname = setting.gallery_dir_fname
tag_fname = setting.gallery_tag_fname

_help = """
The CLI for ZetsuBou
"""

app = typer.Typer(rich_markup_mode="rich", help=_help)
app.add_typer(backup)
app.add_typer(build)
app.add_typer(db)
app.add_typer(elasticsearch)
app.add_typer(gallery)
app.add_typer(migrate)
app.add_typer(s3)
app.add_typer(standalone)
app.add_typer(sync)
app.add_typer(tag)
app.add_typer(test)
app.add_typer(video)

if plugin is not None:
    app.add_typer(plugin)


@app.command()
def batch_pdf2img(
    src: str = typer.Argument(..., help="The repository path of the PDFs."),
    dest: str = typer.Argument(..., help="The home path of the output galleries."),
    dpi: int = typer.Option(default=200, help="Dots per Inch."),
    width: int = typer.Option(default=1280, help="Image width."),
    height: int = typer.Option(default=None, help="Image height."),
    fmt: str = typer.Option(default="png", help="Output image format."),
    prefix: str = typer.Option(default="", help="Prefix of the image file name."),
):
    """
    Convert PDF files under source into images inside galleries.
    """
    src = Path(src)
    dest = Path(dest)
    print(f"source: {src}")
    print(f"destination: {dest}")
    for fpath in src.glob("**/*.pdf"):
        print(f"pdf: {fpath}")
        new_fname = str(uuid4())
        new_fpath = dest / new_fname / fpath.name
        tag_path = dest / new_fname / dir_fname / tag_fname
        os.makedirs(tag_path.parent, exist_ok=True)
        gallery = GalleryModel(
            **{
                "id": str(uuid4()),
                "timestamp": get_now(),
                "mtime": get_now(),
                "attributes": {"name": fpath.stem},
            }
        )
        with tag_path.open(mode="w", encoding="utf-8") as fp:
            json.dump(gallery.dict(), fp, indent=4, ensure_ascii=False)
        shutil.copy(fpath, new_fpath)
        with tempfile.TemporaryDirectory():
            convert_from_path(
                new_fpath,
                output_folder=new_fpath.parent,
                output_file=prefix,
                dpi=dpi,
                fmt=fmt,
                size=(width, height),
            )


@app.command()
def pdf2img(
    pdf: str = typer.Argument(..., help="PDF path."),
    out: str = typer.Argument(..., help="The output gallery path. This must be empty."),
    dpi: int = typer.Option(default=200, help="Dots per Inch."),
    width: int = typer.Option(default=1280, help="Image width."),
    height: int = typer.Option(default=None, help="Image height."),
    fmt: str = typer.Option(default="png", help="Output image format."),
    prefix: str = typer.Option(default="", help="Prefix of the image file name."),
):
    """
    Convert PDF file into image files.
    """

    pdf_path = Path(pdf)
    if not pdf_path.exists():
        print(f"PDF: {pdf} not found")
        return

    out_path = Path(out)
    if not is_empty_dir(out_path):
        return

    with tempfile.TemporaryDirectory():
        convert_from_path(
            pdf,
            output_folder=out,
            output_file=prefix,
            dpi=dpi,
            fmt=fmt,
            size=(width, height),
        )


if __name__ == "__main__":
    app()
