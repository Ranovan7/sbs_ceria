from fastapi import APIRouter, Request, Depends, Form, Response, HTTPException
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import templates, oauth2_scheme
from app.models import User
from app.utils import db_session, current_user, login_required, authenticate_user
from app.utils import admin_only
import datetime

router = APIRouter(
    prefix="/sdm",
    tags=[],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(admin_only)])
async def index(request: Request, user=Depends(current_user)):
    return templates.TemplateResponse("sdm/index.html", {"request": request, "user": user})
