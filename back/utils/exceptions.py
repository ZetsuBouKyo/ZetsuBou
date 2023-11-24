from fastapi import HTTPException


class RequiresLoginException(HTTPException):
    ...


class MaxRetriesExceededException(Exception):
    ...


AirflowConflictInArgumentsException = HTTPException(
    status_code=409,
    detail="Conflict in arguments",
)


def AirflowDagIDNotFoundException(dag_id):
    return HTTPException(status_code=404, detail=f"Dag ID: {dag_id} not found")
