import os
from pathlib import Path
from random import randrange
from typing import Iterator
from uuid import uuid4

from PIL import Image
from PIL.Image import registered_extensions

image_sizes = [
    (300, 200),
    (1280, 1825),
    (1280, 1826),
    (1140, 644),
    (1280, 1805),
    (1280, 191),
    (1280, 581),
]
image_format = [("png", "png"), ("jpeg", "jpg")]


def create_img(fpath: Path, format: str = "jpeg"):
    img = Image.new(
        "RGB",
        image_sizes[randrange(len(image_sizes))],
        (randrange(255), randrange(255), randrange(255)),
    )
    img.save(fpath, format)


def get_gallery_names(num: int) -> str:
    padding = len(str(num))
    if padding < 3:
        padding = 3
    for i in range(num):
        yield f"{i:0{padding}d}"


def get_image_names(num: int, format: str = ".jpg") -> str:
    for i in range(num):
        yield f"{i}{format}"


def generate_galleries(
    root: Path,
    gallery_names: Iterator[str],
    img_names: Iterator[str],
    format: str = ".jpg",
):
    registered_formats = registered_extensions()
    pil_format = registered_formats.get(format, None)
    if pil_format is None:
        raise ValueError(f"unknown file extension: {format}")

    for gallery_name in gallery_names:
        gallery_path = root / gallery_name
        os.makedirs(gallery_path, exist_ok=True)
        for img_name in img_names:
            img_path = gallery_path / f"{img_name}{format}"
            create_img(img_path, pil_format)
