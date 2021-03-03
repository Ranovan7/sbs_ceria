from fastapi import APIRouter, Request, Depends, Form, Cookie, status
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app import templates
from app.models import User, Sales
from app.schemas import CreateSales, BaseUser
from app.utils import db_session, current_user, admin_only, get_message
from app.utils import RedirectWithMessage, CustomTemplateResponse

router = APIRouter(
    prefix="/sdm",
    tags=["html"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(admin_only)])
async def index(request: Request, user = Depends(current_user), db: Session = Depends(db_session), message = Depends(get_message)):
    sales = db.query(Sales).order_by(Sales.id).all()
    print(message)
    return CustomTemplateResponse("sdm/index.html", {"request": request, "user": user, 'sales': sales, 'message': message})


@router.post("/sales", dependencies=[Depends(admin_only)])
async def create_sales(sales_form: CreateSales = Depends(CreateSales.as_form), user=Depends(current_user), db = Depends(db_session)):
    # create user
    user = User(
        username=sales_form.username,
        role=2 # sales
    )
    user.set_password(sales_form.password)

    # create sales
    sales = Sales(
        nama=sales_form.nama,
        kode=sales_form.kode,
        alamat=sales_form.alamat,
        kota=sales_form.kota,
        telepon=sales_form.telepon,
        keterangan=sales_form.keterangan
    )

    db.add(user)
    db.add(sales)
    db.commit()
    db.refresh(user)

    sales.user_id = user.id
    db.commit()

    return RedirectResponse("/sdm", status_code=status.HTTP_303_SEE_OTHER)
