from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import db_session
from app.utils import oauth2_scheme, get_current_user, api_admin_only
from app.models import User
from app.schemas import BaseUser, UserInfo, CreateUser

router = APIRouter(
    prefix="/users",
    tags=["api", "users"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/",
    dependencies=[Depends(api_admin_only)],
    response_model=List[UserInfo])
async def index(
    db: Session = Depends(db_session)
):
    results = db.query(User).all()
    return results


@router.post("/",
    dependencies=[Depends(api_admin_only)],
    response_model=UserInfo)
async def add_users(
    user_data: CreateUser,
    db: Session = Depends(db_session)
):
    new_user = User(username=user_data.username, role=user_data.role)
    new_user.set_password(user_data.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}",
    dependencies=[Depends(api_admin_only)],
    response_model=UserInfo)
async def get_users(
    user_id: int,
    db: Session = Depends(db_session)
):
    return db.query(User).get(user_id)


@router.post("/{user_id}",
    dependencies=[Depends(api_admin_only)],
    response_model=UserInfo)
async def get_users(
    user_id: int,
    user_data: CreateUser,
    db: Session = Depends(db_session)
):
    user = db.query(User).get(user_id)
    user.set_password(user_data.password)

    db.commit()
    db.refresh(user)
    return user
