from fastapi import APIRouter, Request, Depends, Form, Response, HTTPException
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import templates, oauth2_scheme
from app.models import User
from app.utils import db_session, current_user, login_required, authenticate_user
from app.utils import admin_or_sales, sales_only
import datetime

router = APIRouter(
    prefix="/pesanan",
    tags=[],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(admin_or_sales)])
async def index(request: Request, user=Depends(current_user)):
    return templates.TemplateResponse("pesanan/index.html", {"request": request, "user": user})


@router.get("/order", dependencies=[Depends(sales_only)])
async def order(request: Request, user=Depends(current_user)):
    return templates.TemplateResponse("pesanan/order.html", {"request": request, "user": user})
