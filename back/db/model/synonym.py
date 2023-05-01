from pydantic import BaseModel


class SynonumLanguage(BaseModel):
    id: int
    lang: str


class SynonymGroup(BaseModel):
    id: int
    definition: str = None


class SynonymToken(BaseModel):
    id: int
    group_id: int
    word: str
    lang: int
    definition: str = None
