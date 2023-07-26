from pathlib import Path

from PIL.Image import registered_extensions

from back.model.image import BrowserImageFormatEnum

image_formats = {f.lower() for f in registered_extensions().keys()}
browser_image_formats = {f.value for f in BrowserImageFormatEnum}


def is_image(fpath: Path):
    return fpath.suffix.lower() in image_formats


def is_browser_image(fpath: Path):
    return fpath.suffix.lower() in browser_image_formats
