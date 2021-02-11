from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app import templates
from app.utils import db_session, current_user, sales_only

router = APIRouter(
    prefix="/sales",
    tags=["sales"],
    dependencies=[Depends(sales_only)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def index(request: Request, user = Depends(current_user), db: Session = Depends(db_session)):
    return templates.TemplateResponse("sales/index.html", {"request": request, "user": user})
