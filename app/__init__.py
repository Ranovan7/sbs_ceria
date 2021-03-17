from fastapi import Depends, FastAPI, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
origins = ["*"]

app = FastAPI(
    docs_url="/docs",
    redoc_url=None,
    title="SBSehati",
    description="api documentations",
    version="0.1.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/client",
    StaticFiles(directory="./spa/__sapper__/export/client"),
    name="client")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# templates = Jinja2Templates(directory="./app/templates")
templates = Jinja2Templates(directory="./spa/__sapper__/export")

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
from app.routes import sdm
from app.routes import penjualan
from app import api


app.include_router(main.router)
# app.include_router(sdm.router)
# app.include_router(penjualan.router)
app.include_router(api.router)
