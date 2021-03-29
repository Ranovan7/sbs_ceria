from fastapi import APIRouter
from app.routes import main, pesanan, sdm

router = APIRouter(
    prefix="",
    tags=[],
    responses={404: {"description": "Not found"}},
)

router.include_router(main.router)
router.include_router(pesanan.router)
router.include_router(sdm.router)
