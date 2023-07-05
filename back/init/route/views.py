from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from back.route.views import index

router = APIRouter()

router.add_api_route("/initialization", index)


def redirect():
    return RedirectResponse("/initialization")


router.add_api_route("/", redirect)
router.add_api_route("/NotFound", redirect)
