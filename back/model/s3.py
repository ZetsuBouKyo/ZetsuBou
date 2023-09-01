from typing import Any, List, Optional

from pydantic import BaseModel, Field


class S3Object(BaseModel):
    bucket_name: str = ""
    prefix: str = ""


class S3GetPaginatorResponseContent(BaseModel):
    Key: str
    Size: int = Field(..., description="Size in bytes of the object")


class S3GetPaginatorResponseCommonPrefix(BaseModel):
    Prefix: str


class S3GetPaginatorResponse(BaseModel):
    Name: str
    Delimiter: str
    MaxKeys: int
    Contents: List[S3GetPaginatorResponseContent] = []
    CommonPrefixes: List[S3GetPaginatorResponseCommonPrefix] = []
    KeyCount: int


class S3ResponseMetadata(BaseModel):
    RequestId: str
    HTTPStatusCode: int


class S3Response(BaseModel):
    ResponseMetadata: S3ResponseMetadata


class S3ResponseBucket(BaseModel):
    Name: str


class S3ListBucketsResponse(S3Response):
    Buckets: List[S3ResponseBucket] = []


class S3GetObjectResponse(S3Response):
    ContentLength: int
    ETag: str
    ContentType: str
    Metadata: dict
    Body: Any


class S3PutObjectResponse(S3Response):
    ETag: str


S3DeleteObjectResponse = S3Response


class S3DeleteObjectsResponseDeleted(BaseModel):
    Key: str
    VersionId: Optional[str] = None
    DeleteMarker: Optional[bool] = None
    DeleteMarkerVersionId: Optional[str] = None


class S3DeleteObjectsResponseError(BaseModel):
    Key: str
    VersionId: Optional[str] = None
    Code: Optional[str] = None
    Message: Optional[str] = None


class S3DeleteObjectsResponse(BaseModel):
    Deleted: List[S3DeleteObjectsResponseDeleted] = []
    Errors: List[S3DeleteObjectsResponseError] = []
