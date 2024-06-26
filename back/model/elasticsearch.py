from collections import defaultdict
from enum import Enum
from typing import (
    Any,
    DefaultDict,
    Generic,
    List,
    NewType,
    Optional,
    TypedDict,
    TypeVar,
)

from pydantic import BaseModel, Field

SourceT = TypeVar("SourceT")

ElasticsearchField = NewType("ElasticsearchField", str)


class ElasticsearchAnalyzerEnum(str, Enum):
    DEFAULT: str = "default"
    KEYWORD: str = "keyword"
    NGRAM: str = "ngram"
    STANDARD: str = "standard"
    SYNONYM: str = "synonym"
    URL: str = "url"


ElasticsearchKeywordAnalyzers = TypedDict(
    "ElasticsearchKeywordAnalyzers",
    {
        "default": List[str],
        "keyword": List[str],
        "ngram": List[str],
        "standard": List[str],
        "url": List[str],
    },
)


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


class ElasticsearchCleanResult(BaseModel):
    total: int = 0
    storage: DefaultDict[str, int] = defaultdict(lambda: 0)
