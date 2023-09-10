from enum import Enum
from typing import Any, Generic, List, NewType, Optional, TypeVar

from pydantic import BaseModel, Field
from rich import print_json

SourceT = TypeVar("SourceT")

ElasticsearchField = NewType("ElasticsearchField", str)


class AnalyzerEnum(str, Enum):
    DEFAULT: str = "default"
    KEYWORD: str = "keyword"
    NGRAM: str = "ngram"
    STANDARD: str = "standard"
    SYNONYM: str = "synonym"
    URL: str = "url"


class QueryBooleanEnum(str, Enum):
    MUST: str = "must"
    SHOULD: str = "should"


class Total(BaseModel):
    value: int = 0


class Hit(BaseModel, Generic[SourceT]):
    id: str = Field(alias="_id")
    source: Optional[SourceT] = Field(default={}, alias="_source")
    score: Optional[float] = Field(default=None, alias="_score")
    sort: List[Any] = Field(default=[])


class Hits(BaseModel, Generic[SourceT]):
    total: Total = Total()
    hits: List[Hit[SourceT]] = []


class SearchResult(BaseModel, Generic[SourceT]):
    scroll_id: Optional[str] = Field(default=None, alias="_scroll_id")
    hits: Hits[SourceT] = Field(default=Hits[SourceT]())

    def print(self):
        print_json(data=self.model_dump())


class Count(BaseModel):
    count: int


class ElasticsearchHealthResponse(BaseModel):
    status: str = None
