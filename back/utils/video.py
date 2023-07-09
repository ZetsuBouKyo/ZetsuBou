from pathlib import Path


def is_video(fpath: Path) -> bool:
    return fpath.suffix.lower() == ".mp4"
