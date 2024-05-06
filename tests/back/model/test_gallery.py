from back.model.gallery import Gallery
from back.settings import setting
from lib.faker import ZetsuBouFaker
from tests.general.logging import logger

DIR_FNAME = setting.gallery_dir_fname
TAG_FNAME = setting.gallery_tag_fname


def test_gallery():
    Gallery()


def test_gallery_tag_source():
    faker = ZetsuBouFaker()
    gallery = faker.simple_galleries()[0]
    gallery.path = faker.minio_folder_path()

    logger.debug(f"gallery folder path: {gallery.path}")

    gallery_tag_path = f"{gallery.path}{DIR_FNAME}/{TAG_FNAME}"
    logger.debug(f"gallery tag path: {gallery.tag_source.path}")
    logger.debug(f"gallery tag path (ans): {gallery_tag_path}")

    assert gallery.tag_source.path == gallery_tag_path
