from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import db_session
from app.utils import oauth2_scheme, api_any_user
from app.models import Obat

router = APIRouter(
    prefix="/obat",
    tags=["api", "obat"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(api_any_user)])
async def index(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db_session)
) -> List[Obat]:
    query = db.query(Obat)
    # query = query.offset(skip).limit(limit)
    return query.all()


@router.get("/{obat_id}", dependencies=[Depends(api_any_user)])
async def get_obat(
    obat_id: int,
    db: Session = Depends(db_session)
) -> Obat:
    return db.query(Obat).get(obat_id)
