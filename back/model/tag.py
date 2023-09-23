from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from back.utils.model import TagStr


class TagInsert(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    category_ids: List[int] = []
    synonym_ids: List[int] = []
    representative_id: Optional[int] = None
    attributes: Dict[int, str] = {}


class TagCreate(BaseModel):
    name: TagStr
    category_ids: List[int] = []
    synonym_ids: List[int] = []
    representative_id: Optional[int] = None
    attributes: Dict[int, str] = {}


class TagUpdate(BaseModel):
    id: int
    name: str
    category_ids: List[int] = []
    synonym_ids: List[int] = []
    representative_id: Optional[int] = None
    attributes: Dict[int, str] = {}


class TagElastic(BaseModel):
    id: int
    category_ids: List[int] = []
    synonym_ids: List[int] = []
    representative_id: Optional[int] = None
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
    representative: Optional[TagToken] = None
    attributes: List[TagAttribute] = []


TagInterpretation = Tag
