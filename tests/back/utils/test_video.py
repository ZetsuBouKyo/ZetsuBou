from pathlib import Path

from back.utils.video import is_video


def test():
    data = [
        "example.mp4",
        "example.MP4",
        "/tmp/example.mp4",
        "./example.mp4",
        "folder/example.mp4",
    ]
    for d in data:
        assert is_video(Path(d))
