from typing import Dict, List, Optional

from pydantic import BaseModel

from back.utils.model import TagStr


class _TagBase(BaseModel):
    category_ids: List[int] = []
    synonym_ids: List[int] = []
    representative_id: Optional[int] = None
    attributes: Dict[int, str] = {}


class TagCreate(_TagBase):
    name: TagStr


class TagInsert(TagCreate):
    id: Optional[int] = None


class TagInserted(TagCreate):
    id: int


TagUpdate = TagInserted


class TagElasticsearch(_TagBase):
    id: int


class TagToken(BaseModel):
    id: int
    name: str


class TagAttribute(BaseModel):
    id: int
    name: str
    value: str


class Tag(BaseModel):
    id: int
    name: str
    categories: List[TagToken] = []
    synonyms: List[TagToken] = []
    representative: Optional[TagToken] = None
    attributes: List[TagAttribute] = []


TagInterpretation = Tag
