from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app import templates
from app.models import User, Sales
from app.schemas import CreateSales, BaseUser
from app.utils import db_session, current_user, admin_only
from app.utils import RedirectWithMessage, CustomTemplateResponse

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(admin_only)])
async def index(request: Request, user = Depends(current_user), db: Session = Depends(db_session)):
    sales = db.query(Sales).order_by(Sales.id).all()
    return CustomTemplateResponse("admin/index.html", {"request": request, "user": user, 'sales': sales})


@router.post("/users/sales", dependencies=[Depends(admin_only)])
async def create_user(sales_form: CreateSales = Depends(CreateSales.as_form), user=Depends(current_user), db = Depends(db_session)):
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

    return RedirectResponse("/admin", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/users/sales/{sales_id}", dependencies=[Depends(admin_only)])
async def user_for_existing_sales(sales_id: int, sales_form: BaseUser = Depends(BaseUser.as_form), user=Depends(current_user), db = Depends(db_session)):
    sales = db.query(Sales).get(sales_id)

    if not sales:
        return {"status": "error", "details": "Sales data now found"}

    # # create user
    # user = User(
    #     username=sales_form.username,
    #     role=2 # sales
    # )
    # user.set_password(sales_form.password)
    #
    # db.add(user)
    # db.commit()
    # db.refresh(user)
    #
    # sales.user_id = user.id
    # db.commit()

    return RedirectWithMessage("/", f"User untuk sales {sales.nama} berhasil ditambahkan!", "success")


@router.post("/users/{user_id}/password", dependencies=[Depends(admin_only)])
async def change_password(user_id: int, password: str = Form(...), password2: str = Form(...), db: Session = Depends(db_session), user = Depends(current_user)):
    print("Changing Password")
    if password != password2:
        return RedirectResponse(f"/admin", status_code=status.HTTP_303_SEE_OTHER)
    _user = db.query(User).get(user_id)
    _user.set_password(password)
    db.commit()
    return RedirectResponse(f"/admin", status_code=status.HTTP_303_SEE_OTHER)
