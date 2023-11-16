from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, EmailStr

from back.settings import DEFAULT_ADMIN_EMAIL
from back.utils.model import JsonStr as JSON


class User(BaseModel):
    email: EmailStr
    text: JSON = "{}"


app = FastAPI()


@app.get("/user", response_model=User)
def foo():
    return User(email=DEFAULT_ADMIN_EMAIL)


client = TestClient(app)


def test_custom_response_schema():
    response = client.get("/openapi.json")
    openapi = response.json()

    f = (
        openapi.get("components", {})
        .get("schemas", {})
        .get("User", {})
        .get("properties", {})
        .get("text", {})
        .get("format", None)
    )

    assert f == "json"
