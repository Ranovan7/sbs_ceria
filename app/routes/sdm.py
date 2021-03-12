from fastapi import APIRouter, Request
from app import templates

router = APIRouter(
    prefix="/sdm",
    tags=["html"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("sdm/index.html", {'request': request})
