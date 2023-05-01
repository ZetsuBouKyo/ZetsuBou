import shutil
from pathlib import Path

from back.settings import setting


class Gallery:
    """Operations for Gallery in ZetsuBou."""

    def clone(self, home: str = None, fname: str = None):
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
