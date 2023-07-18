from typing import List, Tuple

from pydantic import BaseModel


class ParsedKeywords(BaseModel):
    keywords: str = ""
    remaining_keywords: str = ""
    includes: List[Tuple[str, str]] = []
    excludes: List[Tuple[str, str]] = []
