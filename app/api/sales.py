from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import db_session
from app.utils import oauth2_scheme, api_admin_or_sales, api_admin_only, get_current_user
from app.models import User, Sales

router = APIRouter(
    prefix="/sales",
    tags=["api", "sales"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(api_admin_or_sales)])
async def index(
    skip: int = 0,
    limit: int = 100,
    user = Depends(get_current_user),
    db: Session = Depends(db_session)
) -> List[Sales]:
    query = db.query(Sales)
    if user.role_tag == "sales":
        query = query.filter(Sales.user_id == user.id)

    # query = query.offset(skip).limit(limit)
    return query.all()


@router.get("/{sales_id}", dependencies=[Depends(api_admin_only)])
async def get_sales(
    sales_id: int,
    db: Session = Depends(db_session)
) -> Sales:
    return db.query(Sales).get(sales_id)
