from fastapi import Depends, FastAPI, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
origins = ["*"]
templates = Jinja2Templates(directory="./app/templates")


async def not_found(request, exc):
    if request.url.path.split("/")[1] == "api":
        return JSONResponse(content={'detail': "API not Found"})
    return templates.TemplateResponse("errors/404.html", {"request": request, "nav_off": True})


exception_handlers = {
    404: not_found,
}

app = FastAPI(
    docs_url="/docs",
    redoc_url=None,
    title="SBSehati",
    description="api documentations",
    version="0.1.0",
    exception_handlers=exception_handlers)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
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
from app import routes
from app import api


app.include_router(api.router)
app.include_router(routes.router)
