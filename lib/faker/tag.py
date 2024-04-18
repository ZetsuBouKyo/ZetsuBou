from enum import Enum
from typing import List

from pydantic import BaseModel


class TagAttributeEnum(str, Enum):
    DESCRIPTION: str = "description"
    NOTE: str = "note"
    SOURCE: str = "source"


class TagCategoryEnum(str, Enum):
    COLOR: str = "Color"
    COUNTRY: str = "Country"
    LANGUAGE: str = "Language"
    SUBJECT: str = "Subject"
    TEST: str = "Test"


class TagColorEnum(str, Enum):
    GREEN: str = "green"
    RED: str = "red"
    YELLOW: str = "yellow"


class TagCountryEnum(str, Enum):
    GERMANY: str = "Germany"
    JAPAN: str = "Japan"
    PERU: str = "Peru"
    TAIWAN: str = "Taiwan"
    US: str = "U.S."


class TagLanguageEnum(str, Enum):
    CHINESE: str = "Chinese"
    ENGLISH: str = "English"
    JAPANESE: str = "Japanese"


class TagSubjectEnum(str, Enum):
    MATH: str = "Math"
    PHYSICS: str = "Physics"


class FakerTag(BaseModel):
    name: str
    categories: List[str] = []


# the order matter
tags = [
    FakerTag(name=TagCategoryEnum.TEST.value),
    FakerTag(name=TagCategoryEnum.COLOR.value, categories=[TagCategoryEnum.TEST.value]),
    FakerTag(
        name=TagCategoryEnum.COUNTRY.value, categories=[TagCategoryEnum.TEST.value]
    ),
    FakerTag(
        name=TagCategoryEnum.LANGUAGE.value, categories=[TagCategoryEnum.TEST.value]
    ),
    FakerTag(
        name=TagCategoryEnum.SUBJECT.value, categories=[TagCategoryEnum.TEST.value]
    ),
    FakerTag(
        name=TagColorEnum.GREEN.value,
        categories=[TagCategoryEnum.TEST.value, TagCategoryEnum.COLOR.value],
    ),
    FakerTag(
        name=TagColorEnum.RED.value,
        categories=[TagCategoryEnum.TEST.value, TagCategoryEnum.COLOR.value],
    ),
    FakerTag(
        name=TagColorEnum.YELLOW.value,
        categories=[TagCategoryEnum.TEST.value, TagCategoryEnum.COLOR.value],
    ),
    FakerTag(
        name=TagCountryEnum.GERMANY.value,
        categories=[TagCategoryEnum.TEST.value, TagCategoryEnum.COUNTRY.value],
    ),
    FakerTag(
        name=TagCountryEnum.JAPAN.value,
        categories=[TagCategoryEnum.TEST.value, TagCategoryEnum.COUNTRY.value],
    ),
    FakerTag(
        name=TagCountryEnum.PERU.value,
        categories=[TagCategoryEnum.TEST.value, TagCategoryEnum.COUNTRY.value],
    ),
    FakerTag(
        name=TagCountryEnum.TAIWAN.value,
        categories=[TagCategoryEnum.TEST.value, TagCategoryEnum.COUNTRY.value],
    ),
    FakerTag(
        name=TagCountryEnum.US.value,
        categories=[TagCategoryEnum.TEST.value, TagCategoryEnum.COUNTRY.value],
    ),
    FakerTag(
        name=TagLanguageEnum.CHINESE.value,
        categories=[TagCategoryEnum.TEST.value, TagCategoryEnum.LANGUAGE.value],
    ),
    FakerTag(
        name=TagLanguageEnum.ENGLISH.value,
        categories=[TagCategoryEnum.TEST.value, TagCategoryEnum.LANGUAGE.value],
    ),
    FakerTag(
        name=TagLanguageEnum.JAPANESE.value,
        categories=[TagCategoryEnum.TEST.value, TagCategoryEnum.LANGUAGE.value],
    ),
    FakerTag(
        name=TagSubjectEnum.MATH.value,
        categories=[TagCategoryEnum.TEST.value, TagCategoryEnum.SUBJECT.value],
    ),
    FakerTag(
        name=TagSubjectEnum.PHYSICS.value,
        categories=[TagCategoryEnum.TEST.value, TagCategoryEnum.SUBJECT.value],
    ),
]
