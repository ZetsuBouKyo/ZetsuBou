import asyncio
import json
import os
import shutil
import tempfile
import time
from pathlib import Path
from uuid import uuid4

import typer
from pdf2image import convert_from_path

from back.crud.setting import update_settings
from back.init.airflow import init_airflow_simple
from back.init.check import ping
from back.init.logger import UVICORN_LOGGING_CONFIG, init_zetsubou_logger
from back.init.setting import init_example_settings
from back.logging import logger_zetsubou
from back.model.gallery import Gallery as GalleryModel
from back.settings import LoggingLevelEnum, setting
from back.utils.dt import get_now
from command.backup import app as backup
from command.build import app as build
from command.db import app as db
from command.elasticsearch import app as elasticsearch
from command.gallery import app as gallery
from command.migrate import app as migrate
from command.redis import app as redis
from command.s3 import app as s3
from command.standalone import app as standalone
from command.sync import app as sync
from command.tag import app as tag
from command.test import app as test
from command.utils import is_empty_dir
from command.video import app as video
from lib.typer import ZetsuBouTyper

init_zetsubou_logger()

try:
    from plugins.cli import app as plugin  # type: ignore
except ModuleNotFoundError:
    plugin = None

DIR_FNAME = setting.gallery_dir_fname
TAG_FNAME = setting.gallery_tag_fname

APP_SECURITY = setting.app_security
APP_PORT = setting.app_port
APP_HOST = setting.app_host
LOG_LEVEL = setting.app_logging_level


_help = """
The CLI for ZetsuBou
"""

app = ZetsuBouTyper(rich_markup_mode="rich", help=_help)
app.add_typer(backup)
app.add_typer(build)
app.add_typer(db)
app.add_typer(elasticsearch)
app.add_typer(gallery)
app.add_typer(migrate)
app.add_typer(redis)
app.add_typer(s3)
app.add_typer(standalone)
app.add_typer(sync)
app.add_typer(tag)
app.add_typer(test)
app.add_typer(video)

if plugin is not None:
    app.add_typer(plugin)


@app.command()
def init_example():
    """
    Initialize the Airflow and settings files.
    """

    # create settings files if they don't exist
    init_example_settings()

    # create admin user from settings if admin user in settings does not exist
    init_airflow_simple()


@app.command()
def run(
    app_host: str = typer.Option(default=APP_HOST, help="ZetsuBou app host."),
    app_port: int = typer.Option(default=APP_PORT, help="ZetsuBou app port."),
    log_level: LoggingLevelEnum = typer.Option(
        default=LOG_LEVEL, help="Logging level."
    ),
    reload: bool = typer.Option(default=True, help="Uvicorn reload."),
    max_retries: int = typer.Option(
        default=50, help="Maximum retries for pinging the services."
    ),
    interval: int = typer.Option(
        default=5, help="Time interval to retry the service ping."
    ),
):
    from lib import uvicorn

    if LOG_LEVEL != log_level:
        setting.app_logging_level = log_level
        update_settings(setting, force=True)

    if type(log_level) is not str:
        log_level = log_level.value
    uvicorn_log_level = log_level.lower()

    if APP_SECURITY:
        r = 1
        logger_zetsubou.info("Ping the services.")
        are_services = asyncio.run(ping())
        while r < max_retries and not are_services:
            time.sleep(interval)
            logger_zetsubou.info("Ping the services.Retries...")
            r += 1
            are_services = asyncio.run(ping())

    uvicorn.run(
        "app:app",
        log_level=uvicorn_log_level,
        host=app_host,
        port=app_port,
        reload=reload,
        lifespan="on",
        log_config=UVICORN_LOGGING_CONFIG,
    )


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
        tag_path = dest / new_fname / DIR_FNAME / TAG_FNAME
        os.makedirs(tag_path.parent, exist_ok=True)
        gallery = GalleryModel(
            **{
                "id": str(uuid4()),
                "name": fpath.stem,
                "last_updated": get_now(),
                "upload_date": get_now(),
            }
        )
        with tag_path.open(mode="w", encoding="utf-8") as fp:
            json.dump(gallery.model_dump(), fp, indent=4, ensure_ascii=False)
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
