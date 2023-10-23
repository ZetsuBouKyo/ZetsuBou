from fastapi import HTTPException


class RequiresLoginException(HTTPException):
    ...


class MaxRetriesExceededException(Exception):
    ...
