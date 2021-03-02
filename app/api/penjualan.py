from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import db_session
from app.utils import oauth2_scheme, get_current_user, login_required, admin_only
from app.models import Penjualan, ItemPenjualan
from app.schemas import CreatePenjualan, PenjualanInfo, ItemPenjualanInfo

router = APIRouter(
    prefix="/penjualan",
    tags=["api", "penjualan"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/",
    dependencies=[Depends(login_required)],)
async def index(
    type: str = None,
    db: Session = Depends(db_session)
) -> List[Penjualan]:
    if type == "order":
        return db.query(Penjualan).filter(Penjualan.accepted == False).all()
    elif type == "accepted":
        return db.query(Penjualan).filter(Penjualan.accepted == True).all()
    else:
        return db.query(Penjualan).all()


@router.get("/{penjualan_id}",
    dependencies=[Depends(login_required)])
async def get_penjualan(
    penjualan_id: int,
    db: Session = Depends(db_session)
) -> Penjualan:
    return db.query(Penjualan).get(penjualan_id)


@router.post("/",
    dependencies=[Depends(login_required)])
async def add_penjualan(
    penjualan: CreatePenjualan,
    db: Session = Depends(db_session)
) -> Penjualan:
    new_penjualan = Penjualan(
        tgl=penjualan.tgl,
        sales_id=penjualan.sales_id,
        pelanggan_id=penjualan.pelanggan_id
    )
    db.add(new_penjualan)
    db.commit()
    db.refresh(new_penjualan)

    for item in penjualan.item_penjualan:
        new_item = ItemPenjualan(
            qty=item.qty,
            barang_id=item.barang_id,
            penjualan_id=new_penjualan.id
        )
        db.add(new_item)
        db.commit()

    return new_penjualan


@router.post("/{penjualan_id}/accept",
    dependencies=[Depends(admin_only)])
async def accept_penjualan(
    penjualan_id: int,
    db: Session = Depends(db_session)
) -> Penjualan:
    penjualan = db.query(Penjualan).get(penjualan_id)
    penjualan.accepted = True
    db.commit()
    return penjualan


@router.post("/{penjualan_id}/items",
    dependencies=[Depends(admin_only)],)
async def item_penjualan(
    penjualan_id: int,
    db: Session = Depends(db_session)
) -> Penjualan:
    items = db.query(ItemPenjualan).filter(
        ItemPenjualan.penjualan_id == penjualan_id).all()
    return items
