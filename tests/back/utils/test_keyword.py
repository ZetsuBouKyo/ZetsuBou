from typing import List, Tuple

from pydantic import BaseModel

from back.utils.keyword import KeywordParser
from tests.general.logger import logger
from tests.general.summary import print_divider


class DataModel(BaseModel):
    keywords: List[str]
    ans_remaining_keywords: str
    ans_includes: List[Tuple[str, str]]
    ans_excludes: List[Tuple[str, str]]
    docs: str
    show_docs: bool


raw_data = [
    {
        "keywords": ["-tags.language"],
        "ans_remaining_keywords": "",
        "ans_includes": [],
        "ans_excludes": [("tags.language", "")],
        "docs": "Excludes all documents that have a `tags.language` field.",
        "show_docs": True,
    },
    {
        "keywords": [
            "-tags.language=english",
            '-tags.language="english"',
            '-"tags.language"=english',
            '-"tags.language"="english"',
        ],
        "ans_remaining_keywords": "",
        "ans_includes": [],
        "ans_excludes": [("tags.language", "english")],
        "docs": "Excludes documents that have an `english` value in a `tags.language` field.",
        "show_docs": True,
    },
    {
        "keywords": [
            "tags.language=中文",
            'tags.language="中文"',
            '"tags.language"=中文',
            '"tags.language"="中文"',
        ],
        "ans_remaining_keywords": "",
        "ans_includes": [("tags.language", "中文")],
        "ans_excludes": [],
        "docs": "Includes documents that have a `中文` value in a `tags.language` field.",
        "show_docs": True,
    },
    {
        "keywords": ["tags.language==中文"],
        "ans_remaining_keywords": "",
        "ans_includes": [("tags.language", "=中文")],
        "ans_excludes": [],
        "docs": "Includes documents that have a `=中文` value in a `tags.language` field.",
        "show_docs": True,
    },
    {
        "keywords": ["tags.language==中=文="],
        "ans_remaining_keywords": "",
        "ans_includes": [("tags.language", "=中=文=")],
        "ans_excludes": [],
        "docs": "Includes documents that have a `=中=文=` value in a `tags.language` field.",
        "show_docs": True,
    },
    {
        "keywords": [
            " tags.language=中文",
            " tags.language=中文 ",
            " tags.language=中文  ",
            "tags.language=中文 ",
            "tags.language=中文  ",
        ],
        "ans_remaining_keywords": "",
        "ans_includes": [("tags.language", "中文")],
        "ans_excludes": [],
        "docs": "",
        "show_docs": False,
    },
    {
        "keywords": ['tags.language="English (UK)"'],
        "ans_remaining_keywords": "",
        "ans_includes": [("tags.language", "English (UK)")],
        "ans_excludes": [],
        "docs": "Includes documents that have an `English (UK)` value in a `tags.language` field.",
        "show_docs": True,
    },
    {
        "keywords": ['"file page"=12'],
        "ans_remaining_keywords": "",
        "ans_includes": [("file page", "12")],
        "ans_excludes": [],
        "docs": "",
        "show_docs": False,
    },
    {
        "keywords": [
            'tags.language=中文 text="hello world"wrong"  format" -"tags.language"=en "tags.subject"=math   tags.color=yellow'
        ],
        "ans_remaining_keywords": "wrong  format",
        "ans_includes": [
            ("tags.language", "中文"),
            ("text", "hello world"),
            ("tags.subject", "math"),
            ("tags.color", "yellow"),
        ],
        "ans_excludes": [("tags.language", "en")],
        "docs": "",
        "show_docs": False,
    },
    {
        "keywords": ["[社會 (歷史)] 今天天氣真好=(三國演義) [Chn]"],
        "ans_remaining_keywords": "[社會 (歷史)] [Chn]",
        "ans_includes": [("今天天氣真好", "(三國演義)")],
        "ans_excludes": [],
        "docs": "",
        "show_docs": False,
    },
    {
        "keywords": ['"["社會" (歷史)] 今天天氣真好=(三國演義) [Chn]'],
        "ans_remaining_keywords": '"["社會" (歷史)] 今天天氣真好=(三國演義) [Chn]',
        "ans_includes": [],
        "ans_excludes": [],
        "docs": "If there is an odd number of quotes, it is treated as a normal keyword string.",
        "show_docs": True,
    },
]


def get_data():
    return [DataModel(**d) for d in raw_data]


def test():
    parser = KeywordParser()
    data = get_data()
    for i, d in enumerate(data):
        case_index = i + 1
        for keywords in d.keywords:
            parsed_keywords = parser.parse(keywords)
            print_divider()
            logger.debug(f"case: {case_index}")
            logger.debug(f"keywords: {parsed_keywords.keywords}")
            logger.debug(f"remaining keywords: {parsed_keywords.remaining_keywords}")
            logger.debug(f"includes: {parsed_keywords.includes}")
            logger.debug(f"excludes: {parsed_keywords.excludes}")

            assert parsed_keywords.keywords == keywords
            assert parsed_keywords.remaining_keywords == d.ans_remaining_keywords
            assert parsed_keywords.includes == d.ans_includes
            assert parsed_keywords.excludes == d.ans_excludes
