from fastapi import APIRouter, Request, Depends, Form, Response, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import templates
from app.models import User
from app.utils import db_session, current_user, login_required

router = APIRouter(
    prefix="",
    tags=["main"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(login_required)])
async def index(request: Request, user=Depends(current_user)):
    return templates.TemplateResponse("main/index.html", {"request": request, 'user': user})


@router.get("/login")
async def login_get(request: Request, text: str = None):
    return templates.TemplateResponse("main/login.html", {"request": request})


@router.post("/login")
async def login_post(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_session)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

    if user.verify_password(form_data.password):
        response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="token", value=user.create_access_token())
        return response
    else:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/logout", dependencies=[Depends(login_required)])
async def logout(response: Response):
    token = "not-logged-in"
    response = RedirectResponse("/")
    response.set_cookie(key="token", value=token)
    return response
