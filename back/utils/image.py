from pathlib import Path

from PIL.Image import registered_extensions

image_formats = {f.lower() for f in registered_extensions().keys()}


def is_image(fpath: Path):
    return fpath.suffix.lower() in image_formats
