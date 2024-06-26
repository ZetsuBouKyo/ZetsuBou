from copy import deepcopy
from typing import List, Optional, Tuple
from uuid import uuid4

import pytz
from faker import Faker

from back.model.base import SourceProtocolEnum
from back.model.gallery import Gallery
from back.utils.dt import datetime_formats
from lib.faker.gallery import galleries
from lib.faker.tag import FakerTag, TagAttributeEnum, TagCategoryEnum, tags

image_sizes = [
    (300, 200),
    (1280, 1825),
    (1280, 1826),
    (1140, 644),
    (1280, 1805),
    (1280, 191),
    (1280, 581),
]

image_formats = [(".png", "PNG", "image/png"), (".jpg", "JPEG", "image/jpeg")]


class ZetsuBouFaker(Faker):
    def uuid4(self) -> str:
        return str(uuid4())

    def random_string(self, number: int = 8, is_lower: bool = False) -> str:
        s = "".join(self.random_letters(number))
        if is_lower:
            s = s.lower()
        return s

    def random_datetime_with_utc(self):
        date = self.date_time()
        # If we don't apply the timezone here, there will be an inconsistency between
        # datetime, datetime format, and datetime string.
        date_with_tz = pytz.utc.localize(date)
        return date_with_tz

    def random_datetime_str(
        self, datetime_formats: List[str] = datetime_formats
    ) -> str:
        date = self.random_datetime_with_utc()

        f = self.random_sample(datetime_formats, length=1)[0]
        date_str = date.strftime(f)

        return date_str

    def lower_name(self) -> str:
        return self.name().lower()

    def image_size(
        self, image_sizes: List[Tuple[int, int]] = image_sizes
    ) -> Tuple[int, int]:
        return self.random_sample(image_sizes, length=1)[0]

    def image_format(
        self, image_formats: List[str] = image_formats
    ) -> Tuple[str, str, str]:
        return self.random_sample(image_formats, length=1)[0]

    def minio_folder_path(self) -> str:
        bucket_name = self.random_string()
        path = f"{SourceProtocolEnum.MINIO.value}-{self.random_int()}://{bucket_name}"
        prefix_length = self.random_int(min=0, max=3)
        prefix = "/".join([self.random_string() for _ in range(prefix_length)])
        return f"{path}/{prefix}/"

    def tag_attributes(self) -> List[str]:
        return [attr.value for attr in TagAttributeEnum]

    def tag_attribute_description(self) -> str:
        return TagAttributeEnum.DESCRIPTION.value

    def tag_attribute_note(self) -> str:
        return TagAttributeEnum.NOTE.value

    def tag_attribute_source(self) -> str:
        return TagAttributeEnum.SOURCE.value

    def tag_categories(self) -> List[str]:
        return [category.value for category in TagCategoryEnum]

    def tags(self) -> List[FakerTag]:
        return deepcopy(tags)

    def simple_galleries(self) -> List[Gallery]:
        return deepcopy(galleries)

    def simple_gallery_by_name(self, name: str) -> Optional[Gallery]:
        for gallery in galleries:
            if gallery.name == name:
                return deepcopy(gallery)
        return None

    def random_minimum_gallery(self) -> Gallery:
        author_name = self.name()
        book_name = self.sentence()
        gallery = Gallery(
            **{
                "name": f"[{author_name}] {book_name}",
                "attributes": {
                    "pages": 1,
                },
            }
        )
        return gallery
