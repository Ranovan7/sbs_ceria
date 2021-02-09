from fastapi import APIRouter, Request, Depends, Form, Response, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import templates, db_session, current_user
from app.models import User

router = APIRouter(
    prefix="",
    tags=["main"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def index(request: Request, user=Depends(current_user)):
    if not user:
        return RedirectResponse("/login")

    text = "Hello, World!"
    return templates.TemplateResponse("index.html", {"request": request, 'text': text})


@router.get("/example")
def example(request: Request, text: str = None):
    return templates.TemplateResponse("index.html", {"request": request, 'text': text or 'Example'})


@router.get("/login")
def example(request: Request, text: str = None):
    return templates.TemplateResponse("main/login.html", {"request": request})


@router.post("/login")
def example(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_session)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user and not user.verify_password(form_data.password):
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    else:
        token = "randomtoken"
        response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="token", value=user.create_access_token())
        return response
