from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app import db_session
from app.utils import oauth2_scheme, api_any_user
from app.models import Pelanggan

router = APIRouter(
    prefix="/pelanggan",
    tags=["api", "pelanggan"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(api_any_user)])
async def index(
    sales_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db_session)
) -> List[Pelanggan]:
    if sales_id:
        query = db.query(
                Pelanggan
            ).filter(
                Pelanggan.sales_id == sales_id
            )
    else:
        query = db.query(Pelanggan)

    # query = query.offset(skip).limit(limit)
    return query.order_by(Pelanggan.id).all()


@router.get("/{pelanggan_id}", dependencies=[Depends(api_any_user)])
async def get_pelanggan(
    pelanggan_id: int,
    db: Session = Depends(db_session)
) -> List[Pelanggan]:
    return db.query(Pelanggan).get(pelanggan_id)
