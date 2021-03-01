from fastapi import APIRouter
from app.api import barang, pelanggan, penjualan

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)

router.include_router(barang.router)
router.include_router(pelanggan.router)
router.include_router(penjualan.router)
