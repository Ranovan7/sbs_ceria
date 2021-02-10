from fastapi import Depends, FastAPI, Cookie, Header, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from dotenv import load_dotenv
from jose import JWTError, jwt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

templates = Jinja2Templates(directory="./app/templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
from app.models import User


def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def current_user(token: str = Cookie(None), db: Session = Depends(db_session)):
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


def admin_only(user=Depends(current_user)):
    if not user or user.role != 1:
        return None

    return user


# Routes
from app.routes import main
from app.routes import users


app.include_router(main.router)
app.include_router(users.router)
