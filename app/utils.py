from uvicorn.workers import UvicornWorker
from fastapi import Depends, HTTPException, Request, Cookie, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.orm import Session
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
    def __init__(self, name: str = "NotAllowedException"):
        self.name = name


@app.exception_handler(NotLoggedInException)
async def not_logged_in_exception_handler(request: Request, exc: NotLoggedInException):
    params = "message_text=Please Login to Access the Page"
    params += "&message_type=danger"
    if "/api" in request.url.path:
        return JSONResponse(
            status_code=401,
            content={
                "error": {
                    "type": "Not Authorized",
                    "message": "Please Log In to access endpoint"
                },
            },
        )
    else:
        return RedirectResponse(f"/login?{params}")


@app.exception_handler(NotAllowedException)
async def not_allowed_exception_handler(request: Request, exc: NotAllowedException):
    if "/api" in request.url.path:
        return JSONResponse(
            status_code=403,
            content={
                "error": {
                    "type": "Not Authorized",
                    "message": "Please Log In as user with appropriate role"
                },
            },
        )
    else:
        return RedirectResponse("/forbidden")


### Exceptions End ###

### Dependencies ###


def authenticate_user(
    username: str,
    password: str,
    db: Session
):
    user = db.query(User).filter(User.username == username).first()
    if user and user.verify_password(password):
        return user

    return None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(db_session)
):
    print("Getting Current User")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_message(message_text: str = Cookie(None), message_type: str = Cookie(None), message: str = Cookie(None)):
    if message == 'false':
        return None

    return {
        'text': message_text,
        'type': message_type
    }


async def current_user(auth_token: str = Cookie(None), db: Session = Depends(db_session)):
    if not auth_token:
        return None
    else:
        try:
            payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
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
            print(f"{user.username} - {user.role_tag}")
            return user
        else:
            raise NotAllowedException()


login_required = RoleChecker()
admin_only = RoleChecker(['admin'])
sales_only = RoleChecker(['sales'])
admin_or_sales = RoleChecker(['admin', 'sales'])


class APIRoleChecker:
    def __init__(self, roles: List = []):
        self.roles = roles

    def __call__(self, user = Depends(get_current_user)):
        if not user:
            raise NotLoggedInException()

        if not self.roles or user.role_tag in self.roles:
            print(f"{user.username} - {user.role_tag}")
            return user
        else:
            raise NotAllowedException()


api_any_user = APIRoleChecker()
api_admin_only = APIRoleChecker(['admin'])
api_sales_only = APIRoleChecker(['sales'])
api_admin_or_sales = APIRoleChecker(['admin', 'sales'])


### Dependencies End ###


### Responses ###

templates = Jinja2Templates(directory="./app/templates")


def RedirectWithMessage(url: str, message: str, type: str):
    response = RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="message_text", value=message)
    response.set_cookie(key="message_type", value=type)
    response.set_cookie(key="message", value="true")
    return response


def CustomTemplateResponse(filepath:str, data: Dict):
    response = templates.TemplateResponse(filepath, data)
    response.set_cookie(key="message_text", value=None)
    response.set_cookie(key="message_type", value=None)
    response.set_cookie(key="message", value="false")
    return response


### Responses End ###
