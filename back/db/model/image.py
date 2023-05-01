from pydantic import BaseModel


class Image(BaseModel):
    id: int
    gallery_id: str
    width: int
    height: int
    slope: float
    fname: str
    md5: str
