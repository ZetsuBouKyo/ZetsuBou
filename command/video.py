import mimetypes
import os
import subprocess
from pathlib import Path

import typer
from back.crud.video import get_crud_video

from command.utils import sync

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

app = typer.Typer(name="video", help=_help)


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


@app.command()
@sync
async def create_cover(
    video_id: str = typer.Argument(..., help="Video ID."),
    time: float = typer.Option(default=None, help="Current time in seconds."),
    frame: int = typer.Option(default=None, help="Current frame count."),
):
    """
    Create cover for video.
    """

    if time is None and frame is None:
        return

    crud = await get_crud_video(video_id)
    crud.set_cover(time=time, frame=frame)
