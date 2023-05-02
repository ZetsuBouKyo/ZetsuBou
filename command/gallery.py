import shutil
from pathlib import Path

import typer
from back.settings import setting

_help = """
Manipulate the Galleries.
"""
app = typer.Typer(name="gallery", help=_help)


@app.command()
def clone_tags(
    home: str = typer.Argument(
        ..., help="The path for the upper layer of the galleries"
    ),
    fname: str = typer.Argument(..., help="The new file name of the gallery tag."),
):
    """
    Clone the gallery tag.

    Clone all gallery tags under home path with new file name. The new file is placed
     with the origin gallery tag under the same repository.
    """

    if home is None or fname is None:
        return
    home = Path(home)
    if not home.exists() or not home.is_dir():
        return

    for gallery_path in home.iterdir():
        gallery_tag_home_path = gallery_path / setting.gallery_dir_fname
        gallery_tag_path = gallery_tag_home_path / setting.gallery_tag_fname
        gallery_tag_path = str(gallery_tag_path)
        new_gallery_tag_path = gallery_tag_home_path / fname
        new_gallery_tag_path = str(new_gallery_tag_path)
        shutil.copy(gallery_tag_path, new_gallery_tag_path)
