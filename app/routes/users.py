from fastapi import APIRouter, Request, Depends, Form, Cookie, status
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app import templates
from app.models import User, Sales
from app.schemas import CreateSales, BaseUser
from app.utils import db_session, current_user, admin_only, get_message
from app.utils import RedirectWithMessage, CustomTemplateResponse

router = APIRouter(
    prefix="/users",
    tags=["html"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(admin_only)])
async def index(request: Request, user = Depends(current_user), db: Session = Depends(db_session), message = Depends(get_message)):
    users = db.query(User).order_by(User.id).all()
    return CustomTemplateResponse("users/index.html", {"request": request, "user": user, 'users': users, 'message': message})


@router.post("/{user_id}/password", dependencies=[Depends(admin_only)])
async def change_password(user_id: int, password: str = Form(...), password2: str = Form(...), db: Session = Depends(db_session), user = Depends(current_user)):
    print("Changing Password")
    if password != password2:
        return RedirectResponse(f"/users", status_code=status.HTTP_303_SEE_OTHER)
    _user = db.query(User).get(user_id)
    _user.set_password(password)
    db.commit()
    return RedirectResponse(f"/users", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/sales/{sales_id}", dependencies=[Depends(admin_only)])
async def user_for_existing_sales(sales_id: int, sales_form: BaseUser = Depends(BaseUser.as_form), user=Depends(current_user), db = Depends(db_session)):
    sales = db.query(Sales).get(sales_id)

    if not sales:
        return {"status": "error", "details": "Sales data now found"}

    # create user
    user = User(
        username=sales_form.username,
        role=2 # sales
    )
    user.set_password(sales_form.password)

    db.add(user)
    db.commit()
    db.refresh(user)

    sales.user_id = user.id
    db.commit()

    return RedirectWithMessage("/", f"User untuk sales {sales.nama} berhasil ditambahkan!", "success")
