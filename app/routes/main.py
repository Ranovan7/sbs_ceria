from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app import templates, db_session

router = APIRouter(
    prefix="",
    tags=["main"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_incomes(request: Request):
    text = "Hello, World!"
    return templates.TemplateResponse("index.html", {"request": request, 'text': text})


@router.get("/example")
def get_incomes(request: Request, text: str = None):
    return templates.TemplateResponse("index.html", {"request": request, 'text': text or 'Example'})


# @router.get("/query_example")
# def get_incomes(skip: int = 0, limit: int = 100, db: Session = Depends(db_session)):
#     return db.query(Income).offset(skip).limit(limit).all()
