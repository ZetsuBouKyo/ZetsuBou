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


class ElasticsearchQueryBooleanEnum(str, Enum):
    MUST: str = "must"
    SHOULD: str = "should"


class ElasticsearchTotal(BaseModel):
    value: int = 0


class ElasticsearchHit(BaseModel, Generic[SourceT]):
    id: str = Field(alias="_id")
    source: Optional[SourceT] = Field(default={}, alias="_source")
    score: Optional[float] = Field(default=None, alias="_score")
    sort: List[Any] = Field(default=[])


class ElasticsearchHits(BaseModel, Generic[SourceT]):
    total: ElasticsearchTotal = ElasticsearchTotal()
    hits: List[ElasticsearchHit[SourceT]] = []


class ElasticsearchSearchResult(BaseModel, Generic[SourceT]):
    scroll_id: Optional[str] = Field(default=None, alias="_scroll_id")
    hits: ElasticsearchHits[SourceT] = Field(default=ElasticsearchHits[SourceT]())


class ElasticsearchCountResult(BaseModel):
    count: int


class ElasticsearchHealthResponse(BaseModel):
    status: str = None
