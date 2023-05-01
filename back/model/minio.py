from pydantic import BaseModel


class MinioObject(BaseModel):
    bucket_name: str = None
    object_name: str = None
