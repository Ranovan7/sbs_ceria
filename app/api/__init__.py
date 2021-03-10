from fastapi import APIRouter
from app.api import obat, barang, pelanggan, penjualan, sales, users

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)

router.include_router(users.router)
router.include_router(sales.router)
router.include_router(obat.router)
router.include_router(barang.router)
router.include_router(pelanggan.router)
router.include_router(penjualan.router)
