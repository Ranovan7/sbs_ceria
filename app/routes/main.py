from fastapi import APIRouter, Request, Depends, Form, Response, HTTPException
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import templates, oauth2_scheme
from app.models import User
from app.utils import db_session, current_user, login_required, authenticate_user
from app.utils import api_any_user, get_current_user
import datetime

router = APIRouter(
    prefix="",
    tags=["main"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login")
async def login_get(request: Request, message_text: str = None, message_type: str = None):
    return templates.TemplateResponse("login/index.html", {
        "request": request,
        "message_text": message_text,
        "message_type": message_type})


@router.post("/login")
async def login_post(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_session)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

    if user.verify_password(form_data.password):
        # update user last_login
        user.last_login = datetime.datetime.now()
        db.commit()

        response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="token", value=user.create_access_token())
        response.set_cookie(
            key="Authorization",
            value=f"Bearer {user.create_access_token()}")
        return response
    else:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db_session)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # update user last_login
    user.last_login = datetime.datetime.now()
    db.commit()
    return {"access_token": user.create_access_token(), "token_type": "bearer"}


@router.get("/info", dependencies=[Depends(oauth2_scheme), Depends(api_any_user)])
async def user_info(
    user = Depends(get_current_user)
):
    return {"username": user.username, "role": user.role_tag}


@router.get("/logout", dependencies=[Depends(login_required)])
async def logout(response: Response):
    params = "message_text=Logout Sukses"
    params += "&message_type=info"
    response = RedirectResponse(f"/login?{params}")

    token = "not-logged-in"
    response.set_cookie(key="token", value=token)
    return response


@router.get("/forbidden")
async def forbidden(request: Request):
    return templates.TemplateResponse("errors/403.html", {"request": request})
