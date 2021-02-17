from fastapi import Depends, FastAPI, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

templates = Jinja2Templates(directory="./app/templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Routes
from app.routes import main
from app.routes import users
from app.routes import sdm
from app.routes import sales


app.include_router(main.router)
app.include_router(users.router)
app.include_router(sdm.router)
app.include_router(sales.router)
