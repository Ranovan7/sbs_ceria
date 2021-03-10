from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List
from app import db_session
from app.utils import oauth2_scheme, api_any_user, api_admin_only
from app.models import Barang
from app.schemas import CreateBarang, BarangInfo

router = APIRouter(
    prefix="/barang",
    tags=["api", "barang"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/",
    dependencies=[Depends(api_any_user)],
    response_model=List[BarangInfo])
async def index(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db_session)
) -> List[BarangInfo]:
    return db.query(Barang).offset(skip).limit(limit).all()


@router.get("/{barang_id}", dependencies=[Depends(api_any_user)])
async def get_barang(
    barang_id: int,
    db: Session = Depends(db_session)
) -> Barang:
    return db.query(Barang).get(barang_id)


@router.post("/", dependencies=[Depends(api_admin_only)])
async def add_barang(
    barang: CreateBarang,
    db: Session = Depends(db_session)
) -> Barang:
    new_barang = Barang(**barang.dict())
    db.add(new_barang)
    db.commit()
    db.refresh(new_barang)
    return new_barang
