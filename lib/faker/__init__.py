from typing import List, Tuple
from uuid import uuid4

from faker import Faker

from back.model.gallery import Gallery
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
        return tags

    def simple_galleries(self) -> List[Gallery]:
        return galleries

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
