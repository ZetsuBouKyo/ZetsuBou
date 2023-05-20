from enum import Enum
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from rich import print_json

SourceT = TypeVar("SourceT")


class AnalyzerEnum(str, Enum):
    DEFAULT: str = "default"
    KEYWORD: str = "keyword"
    STANDARD: str = "standard"
    NGRAM: str = "ngram"
    URL: str = "url"


class QueryBoolean(str, Enum):
    MUST: str = "must"
    SHOULD: str = "should"


class Total(BaseModel):
    value: int = 0


class Hit(GenericModel, Generic[SourceT]):
    id: str = Field(alias="_id")
    source: SourceT = Field(default={}, alias="_source")
    score: Optional[float] = Field(default=None, alias="_score")
    sort: list = []


class Hits(GenericModel, Generic[SourceT]):
    total: Total = Total()
    hits: List[Hit[SourceT]] = []


class SearchResult(GenericModel, Generic[SourceT]):
    scroll_id: Optional[str] = Field(default=None, alias="_scroll_id")
    hits: Hits[SourceT] = Hits[SourceT]()

    def print(self):
        print_json(data=self.dict())


class Count(BaseModel):
    count: int


class ElasticsearchHealthResponse(BaseModel):
    status: str = None
