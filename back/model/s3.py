from typing import Any, List

from pydantic import BaseModel


class S3Object(BaseModel):
    bucket_name: str = ""
    prefix: str = ""


class S3GetPaginatorResponseContent(BaseModel):
    Key: str


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


class S3ResponseBucket(BaseModel):
    Name: str


class S3ListBucketsResponse(BaseModel):
    ResponseMetadata: S3ResponseMetadata
    Buckets: List[S3ResponseBucket] = []


class S3GetObjectResponse(BaseModel):
    ResponseMetadata: S3ResponseMetadata
    ContentLength: int
    ETag: str
    ContentType: str
    Metadata: dict
    Body: Any


class S3PutObjectResponse(BaseModel):
    ResponseMetadata: S3ResponseMetadata
    ETag: str


class S3DeleteObjectResponse(BaseModel):
    ResponseMetadata: S3ResponseMetadata


class S3DeleteObjectsResponseDeleted(BaseModel):
    Key: str
    VersionId: str = None
    DeleteMarker: bool = None
    DeleteMarkerVersionId: str = None


class S3DeleteObjectsResponseError(BaseModel):
    Key: str
    VersionId: str = None
    Code: str = None
    Message: str = None


class S3DeleteObjectsResponse(BaseModel):
    Deleted: List[S3DeleteObjectsResponseDeleted] = []
    Errors: List[S3DeleteObjectsResponseError] = []
