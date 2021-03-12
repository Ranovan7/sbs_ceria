from fastapi import APIRouter, Request
from app import templates

router = APIRouter(
    prefix="/penjualan",
    tags=["html"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("penjualan/index.html", {'request': request})
