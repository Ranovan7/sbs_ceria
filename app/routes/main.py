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
    if user.role_tag == 'admin':
        return RedirectResponse("/admin")
    elif user.role_tag == 'sales':
        return RedirectResponse("/sales")    
    return templates.TemplateResponse("main/index.html", {"request": request, 'user': user})


@router.get("/login")
async def login_get(request: Request, message_text: str = None, message_type: str = None):
    return templates.TemplateResponse("main/login.html", {
        "request": request,
        "message_text": message_text,
        "message_type": message_type})


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
    params = "message_text=Logout Sukses"
    params += "&message_type=info"
    response = RedirectResponse(f"/login?{params}")

    token = "not-logged-in"
    response.set_cookie(key="token", value=token)
    return response


@router.get("/forbidden")
async def forbidden(request: Request):
    return templates.TemplateResponse("errors/403.html", {"request": request})
