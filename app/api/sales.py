from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List
from app import db_session
from app.utils import oauth2_scheme, api_admin_or_sales, api_admin_only, get_current_user
from app.models import User, Sales
from app.schemas import SalesInfo, CreateSales

router = APIRouter(
    prefix="/sales",
    tags=["api", "sales"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/",
    dependencies=[Depends(api_admin_or_sales)],
    response_model=List[SalesInfo])
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
    return query.order_by(Sales.id).all()


@router.get("/{sales_id}",
    dependencies=[Depends(api_admin_only)],
    response_model=SalesInfo)
async def get_sales(
    sales_id: int,
    db: Session = Depends(db_session)
) -> Sales:
    return db.query(Sales).get(sales_id)


@router.post("/{sales_id}",
    dependencies=[Depends(api_admin_only)],
    response_model=SalesInfo)
async def post_sales(
    sales_id: int,
    sales_data: CreateSales,
    db: Session = Depends(db_session)
) -> Sales:
    sales = db.query(Sales).get(sales_id)

    for col, value in vars(sales_data).items():
        setattr(sales, col, value)

    db.commit()
    db.refresh(sales)
    return sales
