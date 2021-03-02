from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app import db_session
from app.utils import oauth2_scheme, get_current_user, login_required
from app.models import Pelanggan

router = APIRouter(
    prefix="/pelanggan",
    tags=["api", "pelanggan"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(login_required)])
async def index(
    sales_id: int = None,
    db: Session = Depends(db_session)
) -> List[Pelanggan]:
    if sales_id:
        return db.query(Pelanggan).filter(Pelanggan.sales_id == sales_id).all()
    else:
        return db.query(Pelanggan).all()


@router.get("/{pelanggan_id}", dependencies=[Depends(login_required)])
async def get_pelanggan(
    pelanggan_id: int,
    db: Session = Depends(db_session)
) -> List[Pelanggan]:
    return db.query(Pelanggan).get(pelanggan_id)
