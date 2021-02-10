from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app import templates, db_session, admin_only
from app.models import User
from app.schemas import CreateUser

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_users(request: Request, user = Depends(admin_only), db: Session = Depends(db_session)):
    if not user:
        return RedirectResponse("/login")

    users = db.query(User).order_by(User.id).all()
    return templates.TemplateResponse("users/index.html", {"request": request, "user": user, 'users': users})


@router.post("/")
def create_user(user_form: CreateUser = Depends(CreateUser.as_form), user=Depends(admin_only), db = Depends(db_session)):
    if not user:
        return RedirectResponse(f"/", status_code=status.HTTP_303_SEE_OTHER)

    user = User(
        username=user_form.username,
        role=user_form.role
    )
    user.set_password(user_form.password)

    db.add(user)
    db.commit()
    return RedirectResponse("/users", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/{user_id}/password")
def change_password(user_id: int, password: str = Form(...), password2: str = Form(...), db: Session = Depends(db_session), user = Depends(admin_only)):
    if not user:
        return RedirectResponse(f"/", status_code=status.HTTP_303_SEE_OTHER)

    print("Changing Password")
    if password != password2:
        return RedirectResponse(f"/users", status_code=status.HTTP_303_SEE_OTHER)
    _user = db.query(User).get(user_id)
    _user.set_password(password)
    db.commit()
    return RedirectResponse(f"/users", status_code=status.HTTP_303_SEE_OTHER)
