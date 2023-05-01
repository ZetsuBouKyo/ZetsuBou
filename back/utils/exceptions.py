from fastapi import HTTPException


class RequiresLoginException(HTTPException):
    pass
