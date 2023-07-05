from typing import Dict, List

from pydantic import BaseModel, Field

from back.utils.model import Str


class TagInsert(BaseModel):
    id: int = None
    name: str = None
    category_ids: List[int] = []
    synonym_ids: List[int] = []
    representative_id: int = None
    attributes: Dict[int, str] = {}


class TagCreate(BaseModel):
    name: Str
    category_ids: List[int] = []
    synonym_ids: List[int] = []
    representative_id: int = None
    attributes: Dict[int, str] = {}


class TagUpdate(BaseModel):
    id: int
    name: str
    category_ids: List[int] = []
    synonym_ids: List[int] = []
    representative_id: int = None
    attributes: Dict[int, str] = {}


class TagElastic(BaseModel):
    id: int
    category_ids: List[int] = []
    synonym_ids: List[int] = []
    representative_id: int = Field(None)
    attributes: Dict[int, str] = {}


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
    representative: TagToken = None
    attributes: List[TagAttribute] = []


TagInterpretation = Tag
