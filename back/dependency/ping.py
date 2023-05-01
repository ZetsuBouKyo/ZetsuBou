from fastapi import HTTPException
from tasks import celery_app


def ping_celery():
    if len(celery_app.control.ping(timeout=0.3)) > 0:
        return

    raise HTTPException(status_code=500, detail="Celery worker did not work")
