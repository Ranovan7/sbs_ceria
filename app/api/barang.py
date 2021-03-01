from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import db_session
from app.utils import get_current_user
from app.models import Barang

router = APIRouter(
    prefix="/barang",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[])
async def index(
    user=Depends(get_current_user),
    db: Session = Depends(db_session)
) -> List[Barang]:
    return db.query(Barang).all()
