from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import db_session
from app.utils import oauth2_scheme, get_current_user, login_required, admin_only
from app.models import Barang
from app.schemas import CreateBarang

router = APIRouter(
    prefix="/barang",
    tags=["api", "barang"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(login_required)])
async def index(
    db: Session = Depends(db_session)
) -> List[Barang]:
    return db.query(Barang).all()


@router.get("/{barang_id}", dependencies=[Depends(login_required)])
async def get_barang(
    barang_id: int,
    db: Session = Depends(db_session)
) -> Barang:
    return db.query(Barang).get(barang_id)


@router.post("/", dependencies=[Depends(admin_only)])
async def add_barang(
    barang: CreateBarang,
    db: Session = Depends(db_session)
) -> Barang:
    new_barang = Barang(**barang.dict())
    db.add(new_barang)
    db.commit()
    db.refresh(new_barang)
    return new_barang
