import os
from pathlib import Path
from random import randrange
from typing import Iterator
from uuid import uuid4

import typer
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


def generate_gallery_name() -> str:
    return str(uuid4())


def generate_galleries(
    root: str,
    gallery_names: Iterator[str],
    img_names: Iterator[str],
    format: str = ".jpg",
):
    root = Path(root)

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


def generate_galleries_by_random_names(
    root: Path, nums: int, img_names: Iterator[str], format: str = ".jpg"
):
    gallery_names = [str(uuid4()) for _ in range(nums)]
    generate_galleries(root, gallery_names, img_names, format)


app = typer.Typer(name="gallery")


@app.command()
def generate(
    root: str = typer.Argument(..., help="Parent of the generated gallery."),
    gallery_name: str = typer.Option(
        default=generate_gallery_name,
        help="Gallery name. Default value comes from uuid4.",
    ),
    num_img: int = typer.Option(default=5, help="Number of image in gallery."),
    img_names: str = typer.Option(
        default=None,
        help="Image names without extensions. This value should be split by `,`.",
    ),
):
    """
    Generate the gallery.

    Image name: `--img-names` has higher priority than `--num-img`.
    """

    if img_names is None:
        img_names = [str(i) for i in range(1, num_img + 1)]
    else:
        img_names = img_names.split(",")
    generate_galleries(
        root,
        [
            gallery_name,
        ],
        img_names,
    )
