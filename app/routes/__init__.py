from fastapi import APIRouter
from app.routes import main, penjualan, sdm

router = APIRouter(
    prefix="",
    tags=[],
    responses={404: {"description": "Not found"}},
)

router.include_router(main.router)
router.include_router(penjualan.router)
router.include_router(sdm.router)
