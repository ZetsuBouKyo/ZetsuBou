from back.route.views import index
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

router.add_api_route("/initialization", index)


@router.get("/")
async def redirect_to_initialization():
    return RedirectResponse("/initialization")
