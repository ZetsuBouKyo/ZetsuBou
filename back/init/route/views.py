from back.route.views import index
from fastapi import APIRouter

router = APIRouter()

router.add_api_route("/initialization", index)
