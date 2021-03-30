from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from app import db_session
from app.utils import oauth2_scheme, api_any_user, api_admin_only, get_current_user
from app.models import PesananIn, ItemPesananIn, PesananOut, ItemPesananOut, Sales
from app.schemas import CreatePesanan, PesananInfo, ItemPesananInfo

router = APIRouter(
    prefix="/pesanan",
    tags=["api", "pesanan"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/",
    dependencies=[Depends(api_any_user)],
    response_model=List[PesananInfo])
async def index(
    type: str = None,
    skip: int = 0,
    limit: int = 100,
    user = Depends(get_current_user),
    db: Session = Depends(db_session)
) -> List[PesananInfo]:
    query = db.query(PesananIn)
    if type == "order":
        query = query.filter(
                PesananIn.accepted == False
            )
    elif type == "accepted":
        query = query.filter(
                PesananIn.accepted == True
            )

    if user.role_tag == "sales":
        sales = db.query(Sales).filter(Sales.user_id == user.id).first()
        query = query.filter(
                PesananIn.sales_id == sales.id
            )

    # query = query.offset(skip).limit(limit)
    return query.order_by(PesananIn.tgl.desc()).all()


@router.get("/{pesanan_id}",
    dependencies=[Depends(api_any_user)],
    response_model=PesananInfo)
async def get_pesanan(
    pesanan_id: int,
    db: Session = Depends(db_session)
) -> PesananInfo:
    return db.query(PesananIn).get(pesanan_id)


@router.post("/",
    dependencies=[Depends(api_any_user)],
    response_model=PesananInfo)
async def add_pesanan(
    pesanan: CreatePesanan,
    db: Session = Depends(db_session)
) -> PesananInfo:
    try:
        new_pesanan = PesananIn(
            tgl=pesanan.tgl,
            sales_id=pesanan.sales_id,
            pelanggan_id=pesanan.pelanggan_id
        )
        db.add(new_pesanan)
        db.commit()
        db.refresh(new_pesanan)
        print("pesanan added")

        for item in pesanan.item_pesanan:
            new_item = ItemPesananIn(
                qty=item.qty,
                barang_id=item.barang_id,
                pesanan_id=new_pesanan.id
            )
            db.add(new_item)
            db.commit()

        return new_pesanan
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Terjadi Kesalahan dalam Data")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=422, detail="Terjadi Error saat melakukan penambahan Order")


@router.post("/{pesanan_id}/accept",
    dependencies=[Depends(api_admin_only)],
    response_model=PesananInfo)
async def accept_pesanan(
    pesanan_id: int,
    db: Session = Depends(db_session)
) -> PesananInfo:
    pesanan = db.query(PesananIn).get(pesanan_id)
    pesanan.accepted = True
    db.commit()
    db.refresh(pesanan)

    # create new PesananOut
    print("Adding PesananOut")
    pesanan_out = PesananOut(
        tgl=pesanan.tgl,
        sales_id=pesanan.sales_id,
        pelanggan_id=pesanan.pelanggan_id,
        accepted=pesanan.accepted
    )
    db.add(pesanan_out)
    db.commit()
    db.refresh(pesanan_out)

    print("Adding ItemPesananOut")
    for item in pesanan.item_pesanan:
        new_item = ItemPesananOut(
            qty=item.qty,
            barang_id=item.barang_id,
            pesanan_id=pesanan_out.id
        )
        db.add(new_item)
        db.commit()
    print("Done")

    return pesanan


@router.post("/{pesanan_id}/items",
    dependencies=[Depends(api_admin_only)],)
async def item_pesanan(
    pesanan_id: int,
    db: Session = Depends(db_session)
) -> PesananInfo:
    items = db.query(ItemPesananIn).filter(
        ItemPesananIn.pesanan_id == pesanan_id).all()
    return items
