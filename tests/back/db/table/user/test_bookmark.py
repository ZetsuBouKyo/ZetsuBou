from back.db.table import UserBookmarkGalleryBase, UserBookmarkVideoBase
from tests.general.database import datetime_validator


def test_bookmark_validator():
    assert datetime_validator(UserBookmarkGalleryBase, "validate_modified")
    assert datetime_validator(UserBookmarkVideoBase, "validate_modified")
