import mimetypes
import os
import subprocess
from pathlib import Path

import typer

from back.crud.async_video import CrudAsyncVideo
from lib.typer import ZetsuBouTyper

reserved_symbols = ["#"]


def remove_reserved_symbols(fpath: Path):
    if fpath.is_dir():
        print(f"path: {fpath} is dir")
        return
    new_name = fpath.name

    to_rename = False
    for symbol in reserved_symbols:
        if symbol in fpath.name:
            to_rename = True
            print(f"path: {fpath} needs to be renamed")
        new_name = new_name.replace(symbol, "")

    if not to_rename:
        return

    new_name.replace("   ", " ")
    new_name.replace("  ", " ")
    new_path = fpath.parent / new_name
    fpath.rename(new_path)


_help = """
Manipulate the video.
"""

app = ZetsuBouTyper(name="video", help=_help)


@app.command(name="remove-reserved-symbols")
def _remove_reserved_symbols(
    home: str = typer.Argument(..., help="The path for the upper layer of the videos")
):
    """
    Remove the reserved symbols in video file name for minio.
    """

    home = Path(home)
    for fpath in home.glob("**/*"):
        if fpath.is_dir():
            for symbol in reserved_symbols:
                if symbol in str(fpath):
                    print(fpath)
            continue
        remove_reserved_symbols(fpath)


@app.command()
def remove_broken(
    home: str = typer.Argument(..., help="The path for the upper layer of the videos")
):
    """
    Remove broken videos.
    """

    home = Path(home)
    for fpath in home.glob("**/*"):
        if fpath.is_dir():
            continue

        if fpath.stat().st_size == 0:
            fpath.unlink()


@app.command()
def to_h264(
    src: str = typer.Argument(..., help="The repository of the origin videos."),
    dest: str = typer.Argument(..., help="The repository of the output h264 videos."),
    limit: int = typer.Option(
        default=None,
        help="The number of videos for converting. If this is None, all videos would be converted.",  # noqa
    ),
):
    """
    Convert the videos into h264 video through ffmpeg.
    """
    root = Path(src)
    root_h264 = Path(dest)

    c = 0
    for f in root.rglob("**/*"):
        f_h264 = root_h264 / f.relative_to(root).parent / f"{f.name}.h264.mp4"
        if f_h264.exists():
            continue

        f_mimetypes = mimetypes.guess_type(f.absolute())[0]

        # f_ext = f.suffix.lower()
        # if not f_ext:
        #     print(f.stem)

        if f_mimetypes and (
            f_mimetypes.startswith("video") or f_mimetypes == "audio/x-pn-realaudio"
        ):
            print(f)
            c += 1
            os.makedirs(f_h264.parent, exist_ok=True)
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    str(f),
                    "-vcodec",
                    "libx264",
                    "-movflags",
                    "faststart",
                    str(f_h264),
                ]
            )

            if c >= limit:
                break

    print(f"convert: {c}")


@app.command(
    airflow_dag_id="video-generate-cover",
    airflow_dag_sub_command="video generate-cover",
)
async def generate_cover(
    video_id: str = typer.Argument(..., help="Video ID."),
    frame: int = typer.Option(default=None, help="Current frame count."),
):
    """
    Generate cover for video.
    """

    if frame is None:
        return
    async with CrudAsyncVideo(video_id, is_from_setting_if_none=True) as crud:
        await crud.generate_cover(frame=frame)
