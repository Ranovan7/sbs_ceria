from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import db_session
from app.utils import oauth2_scheme, get_current_user, admin_only
from app.models import User
from app.schemas import BaseUser

router = APIRouter(
    prefix="/users",
    tags=["api", "users"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(admin_only)])
async def index(
    db: Session = Depends(db_session)
) -> List[User]:
    return db.query(User).all()


@router.get("/{user_id}", dependencies=[Depends(admin_only)])
async def get_users(
    user_id: int,
    db: Session = Depends(db_session)
) -> User:
    return db.query(User).get(user_id)


@router.post("/", dependencies=[Depends(admin_only)])
async def add_users(
    user: BaseUser,
    db: Session = Depends(db_session)
) -> User:
    new_user = User(username=user.username)
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
