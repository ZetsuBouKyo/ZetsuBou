from back.model.gallery import Gallery
from lib.faker.tag import (
    TagCategoryEnum,
    TagColorEnum,
    TagCountryEnum,
    TagLanguageEnum,
    TagSubjectEnum,
)

galleries = [
    Gallery(
        **{
            "name": "[Zhonghua Book Company (Sun Zhu, Syu Lan Ying)] Three Hundred Tang Poems (Qing dynasty) [Chinese]",
            "raw_name": "[中華書局 (孫洙, 徐蘭英)] 唐詩三百首 (清朝) [中文]",
            "src": ["https://zh.wikipedia.org/wiki/唐詩三百首"],
            "labels": [TagLanguageEnum.ENGLISH.value, TagLanguageEnum.CHINESE.value],
            "tags": {
                TagCategoryEnum.COLOR.value: [TagColorEnum.YELLOW.value],
                TagCategoryEnum.COUNTRY.value: [TagCountryEnum.TAIWAN.value],
            },
            "attributes": {"rating": 4, "pages": 3},
        }
    ),
    Gallery(
        **{
            "name": "[Barton Zwiebach] A First Course in String Theory 2nd edition",
            "src": [
                "https://en.wikipedia.org/wiki/String_theory",
                "https://www.amazon.com/First-Course-String-Theory-2nd/dp/0521880327",
                "https://www.cambridge.org/highereducation/books/a-first-course-in-string-theory/F5F70646703D818EA10E37C58948CC1B#overview",
            ],
            "labels": [TagLanguageEnum.ENGLISH.value],
            "tags": {
                TagCategoryEnum.COLOR.value: [
                    TagColorEnum.GREEN.value,
                    TagColorEnum.YELLOW.value,
                ],
                TagCategoryEnum.COUNTRY.value: [
                    TagCountryEnum.PERU.value,
                    TagCountryEnum.US.value,
                ],
            },
            "attributes": {
                "category": TagSubjectEnum.PHYSICS.value,
                "rating": 5,
                "pages": 2,
            },
        }
    ),
    Gallery(
        **{
            "name": "[Richard Courant] Introduction to Calculus and Analysis vol.1",
            "src": [
                "https://en.wikipedia.org/wiki/Richard_Courant",
                "https://www.amazon.com/Introduction-Calculus-Analysis-Classics-Mathematics/dp/354065058X",
            ],
            "labels": [TagLanguageEnum.ENGLISH.value],
            "tags": {
                TagCategoryEnum.COLOR.value: [
                    TagColorEnum.GREEN.value,
                    TagColorEnum.YELLOW.value,
                ],
                TagCategoryEnum.COUNTRY.value: [
                    TagCountryEnum.GERMANY.value,
                    TagCountryEnum.US.value,
                ],
            },
            "attributes": {
                "category": TagSubjectEnum.MATH.value,
                "rating": 5,
                "pages": 2,
            },
        }
    ),
]
