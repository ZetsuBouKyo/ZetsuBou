from fastapi import HTTPException, status


class RequiresLoginException(HTTPException): ...


class MaxRetriesExceededException(Exception): ...


AirflowConflictInArgumentsException = HTTPException(
    status_code=409,
    detail="Conflict in arguments",
)


class AirflowDagIDNotFoundException(HTTPException):
    def __init__(
        self,
        dag_id: str,
    ):
        super().__init__(status_code=404, detail=f"Dag ID: {dag_id} not found")


class NotAuthenticatedException(HTTPException):
    def __init__(self, scopes: str, detail: str = None):
        authenticate_value = "Bearer"
        if scopes:
            authenticate_value = f"Bearer scope={scopes}"
        if detail is None:
            detail = "Not authenticated"

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": authenticate_value},
        )


class BaseException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


NotFoundException = BaseException
ServicesNotFoundException = NotFoundException("Services not found.")
StorageServiceNotFoundException = NotFoundException("Storage service not found.")


class SessionNotFoundException(Exception):
    def __init__(self):
        super().__init__(
            "Session not found. Please ensure that the method is called within a context manager, e.g. `async with YourClass() as session: ...`."
        )


NotEmptyException = BaseException("Should be empty.")
