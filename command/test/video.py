from pathlib import Path
from random import randrange
from uuid import uuid4

import cv2
import numpy
import typer
from PIL import Image

from lib.typer import ZetsuBouTyper


def generate_video_name() -> str:
    return str(uuid4())


def generate_frame(width: int, height: int):
    img = Image.new(
        "RGB",
        (width, height),
        (randrange(255), randrange(255), randrange(255)),
    )
    return numpy.asarray(img)


def generate_video(video_path: str, width: int, height: int, frames: int, fps: int = 1):
    # Chrome did not support mp4v (MPEG-4 Visual video)
    fourcc = cv2.VideoWriter_fourcc(*"vp09")
    video = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    for _ in range(frames):
        frame = generate_frame(width, height)
        video.write(frame)

    cv2.destroyAllWindows()
    video.release()


app = ZetsuBouTyper(name="video")


@app.command()
def generate_videos(
    root: str = typer.Argument(..., help="Parent of the generated gallery."),
    num_videos: int = typer.Option(
        default=1, help="Number of videos. Video names come from uuid4."
    ),
    width: int = typer.Option(default=300, help="Video height."),
    height: int = typer.Option(default=200, help="Video height."),
    frames: int = typer.Option(default=5, help="Video frames."),
    fps: int = typer.Option(default=1, help="Video FPS (Frames Per Second)."),
):
    """
    Generate the videos.
    """
    _root = Path(root)
    if not _root.is_dir():
        return

    for _ in range(num_videos):
        video_name = generate_video_name()
        video_name = f"{video_name}.mp4"
        video_path = _root / video_name
        video_path = str(video_path)
        generate_video(video_path, width, height, frames, fps=fps)
