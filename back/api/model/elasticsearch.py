from typing import Optional

from pydantic import BaseModel


class ElasticsearchQueryExampleValue(BaseModel):
    body: dict


class ElasticsearchQueryExample(BaseModel):
    summary: str
    description: Optional[str] = None
    value: ElasticsearchQueryExampleValue


class ElasticsearchAnalyzer(BaseModel):
    name: str
