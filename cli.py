import json
import os
import shutil
import tempfile
from pathlib import Path
from uuid import uuid4

import fire
from pdf2image import convert_from_path

from back.model.gallery import Gallery as GalleryModel
from back.settings import setting
from back.utils.dt import get_now
from command.backup import Backup
from command.build import CmdBuild
from command.db import Db
from command.elastic import Elastic
from command.gallery import Gallery
from command.init import init
from command.sync import Sync
from command.tag import Tag
from command.tests import Tests
from command.utils import is_empty_dir
from command.video import Video

try:
    from plugins.cli import Plugin  # type: ignore

    plugin = Plugin()
except ModuleNotFoundError:
    plugin = None

dir_fname = setting.gallery_dir_fname
tag_fname = setting.gallery_tag_fname


class Cmd:
    """This is the CLI for ZetsuBou.

    Examples:
        - HELP
            `python cli.py --help`
            `python cli.py <group> --help`
            `python cli.py <group> <command> --help`
            `python cli.py <command> --help`

    """

    def __init__(self):
        self.init = init
        self.backup = Backup()
        self.build = CmdBuild()
        self.db = Db()
        self.elastic = Elastic()
        self.tag = Tag()
        self.tests = Tests()
        self.sync = Sync()
        self.gallery = Gallery()
        self.video = Video()
        if plugin is not None:
            self.plugin = plugin

    def setting(self):
        """To print the backend setting in JSON."""
        print(setting.json(indent=4))

    def batch_pdf2png(
        self,
        src: str,
        dest: str,
        dpi: int = 200,
        width: int = 1280,
        height: int = None,
        fmt: str = "png",
        prefix: str = "",
    ):
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

    def pdf2png(
        self,
        pdf: str,
        out: str,
        dpi: int = 200,
        width: int = 1280,
        height: int = None,
        fmt: str = "png",
        prefix: str = "",
    ):
        """To transfer PDF into png files.

        Args:
            pdf (str): Description: The Path of PDF file.
            out (str): Description: The output folder Path for the images. This folder
                       must be empty.
            dpi (int, optional): Description: Dots Per Inch. Defaults to 200.
            width (int, optional): Description: The width of the output image. Defaults
                                   to 1280.
            height (int, optional): Description: The height of the output image.
                                    Defaults to None.
            fmt (str, optional): Description: The format of the image. Defaults to
                                              "png".
            prefix (str, optional): Description: The prefix for the image file name.
                                    Defaults to "".
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
    cmd = Cmd()
    fire.Fire(cmd)
