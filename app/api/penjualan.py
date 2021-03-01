from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import db_session
from app.utils import get_current_user
from app.models import Penjualan

router = APIRouter(
    prefix="/penjualan",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[])
async def index(
    type: str = None,
    user=Depends(get_current_user),
    db: Session = Depends(db_session)
) -> List[Penjualan]:
    if type == "pesanan":
        results = db.query(Penjualan).filter(Penjualan.accepted == False).all()
    else:
        results = db.query(Penjualan).filter(Penjualan.accepted == True).all()
    return results
