import os
from pathlib import Path

from back.settings import setting
from back.utils.gen.gallery import generate_image

TEST_VOLUMES_FILES = setting.test_volumes_files


class ImageSession:
    def __init__(self, home: str = TEST_VOLUMES_FILES):
        self.home = home
        self.image_path = Path(home, "test.png")

    def _generate_image(self):
        if self.image_path.exists():
            return

        os.makedirs(self.image_path.parent, exist_ok=True)
        img_bytes = generate_image((16, 16), (1, 1, 1), "PNG")
        with self.image_path.open(mode="wb") as f:
            f.write(img_bytes)

    def __enter__(self):
        self._generate_image()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb): ...
