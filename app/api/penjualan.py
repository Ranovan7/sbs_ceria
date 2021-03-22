from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import db_session
from app.utils import oauth2_scheme, api_any_user, api_admin_only, get_current_user
from app.models import Penjualan, ItemPenjualan, Sales
from app.schemas import CreatePenjualan, PenjualanInfo, ItemPenjualanInfo

router = APIRouter(
    prefix="/penjualan",
    tags=["api", "penjualan"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/",
    dependencies=[Depends(api_any_user)],
    response_model=List[PenjualanInfo])
async def index(
    type: str = None,
    skip: int = 0,
    limit: int = 100,
    user = Depends(get_current_user),
    db: Session = Depends(db_session)
) -> List[Penjualan]:
    query = db.query(Penjualan)
    if type == "order":
        query = query.filter(
                Penjualan.accepted == False
            )
    elif type == "accepted":
        query = query.filter(
                Penjualan.accepted == True
            )

    if user.role_tag == "sales":
        sales = db.query(Sales).filter(Sales.user_id == user.id).first()
        query = query.filter(
                Penjualan.sales_id == sales.id
            )

    # query = query.offset(skip).limit(limit)
    return query.all()


@router.get("/{penjualan_id}",
    dependencies=[Depends(api_any_user)],
    response_model=PenjualanInfo)
async def get_penjualan(
    penjualan_id: int,
    db: Session = Depends(db_session)
) -> Penjualan:
    return db.query(Penjualan).get(penjualan_id)


@router.post("/",
    dependencies=[Depends(api_any_user)],
    response_model=PenjualanInfo)
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
    print("penjualan added")

    for item in penjualan.item_penjualan:
        new_item = ItemPenjualan(
            qty=item.qty,
            barang_id=item.barang_id,
            penjualan_id=new_penjualan.id
        )
        db.add(new_item)
        db.commit()

    print("returning penjualan")

    return new_penjualan


@router.post("/{penjualan_id}/accept",
    dependencies=[Depends(api_admin_only)])
async def accept_penjualan(
    penjualan_id: int,
    db: Session = Depends(db_session)
) -> Penjualan:
    penjualan = db.query(Penjualan).get(penjualan_id)
    penjualan.accepted = True
    db.commit()
    return penjualan


@router.post("/{penjualan_id}/items",
    dependencies=[Depends(api_admin_only)],)
async def item_penjualan(
    penjualan_id: int,
    db: Session = Depends(db_session)
) -> Penjualan:
    items = db.query(ItemPenjualan).filter(
        ItemPenjualan.penjualan_id == penjualan_id).all()
    return items
