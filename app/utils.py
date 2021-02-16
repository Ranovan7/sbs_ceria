from uvicorn.workers import UvicornWorker
from fastapi import Depends, HTTPException, Request, Cookie, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from functools import wraps
from typing import Callable, List, Dict
from jose import JWTError, jwt

from app import app, oauth2_scheme, db_session
from app import SECRET_KEY, ALGORITHM
from app.models import User


### Workers ###
class MyUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "auto", "http": "auto"}


### Workers Enc ###

### Exceptions ###
class NotLoggedInException(Exception):
    def __init__(self, name: str = "NotLoggedInException"):
        self.name = name


class NotAllowedException(Exception):
    def __init__(self, name: str = "NotLoggeNotAllowedExceptiondInException"):
        self.name = name


@app.exception_handler(NotLoggedInException)
async def not_logged_in_exception_handler(request: Request, exc: NotLoggedInException):
    params = "message_text=Please Login to Access the Page"
    params += "&message_type=danger"
    return RedirectResponse(f"/login?{params}")


@app.exception_handler(NotAllowedException)
async def not_allowed_exception_handler(request: Request, exc: NotAllowedException):
    return RedirectResponse("/forbidden")


### Exceptions End ###

### Dependencies ###


async def current_user(token: str = Cookie(None), db: Session = Depends(db_session)):
    if not token:
        return None
    else:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("username")
            if username is None:
                return None
            user = db.query(User).filter(User.username == username).first()
            return user
        except Exception as e:
            print(f"Error while reading token payload: {e}")
            return None


class RoleChecker:
    def __init__(self, roles: List = []):
        self.roles = roles

    def __call__(self, user = Depends(current_user)):
        if not user:
            raise NotLoggedInException()

        if not self.roles or user.role_tag in self.roles:
            return user
        else:
            raise NotAllowedException()


login_required = RoleChecker()
admin_only = RoleChecker(['admin'])
sales_only = RoleChecker(['sales'])


### Dependencies End ###


### Responses ###

templates = Jinja2Templates(directory="./app/templates")


def RedirectWithMessage(url: str, message: str, type: str):
    response = RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="message_text", value=message)
    response.set_cookie(key="message_type", value=type)
    response.set_cookie(key="is_message", value="true")
    return response


def CustomTemplateResponse(filepath:str, data: Dict, message_text: str = Cookie(None), message_type: str = Cookie(None), is_message: str = Cookie(None)):
    if is_message == "true":
        data['message'] = {
            'text': message_text,
            'type': message_type or "info"
        }

    response = templates.TemplateResponse(filepath, data)
    response.set_cookie(key="message_text", value=None)
    response.set_cookie(key="message_type", value=None)
    response.set_cookie(key="is_message", value="false")
    return response


### Responses End ###
