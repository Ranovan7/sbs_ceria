from fastapi import APIRouter, Request, Depends, Form
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
def get_users(request: Request, db: Session = Depends(db_session), user=Depends(admin_only)):
    if not user:
        return RedirectResponse("/login")

    users = db.query(User).all()
    return templates.TemplateResponse("users/index.html", {"request": request, "user": user, 'users': users})


@router.post("/")
def create_user(user_form: CreateUser, user=Depends(admin_only)):
    user = User(
        username=user_form.username,
        role=user_form.role
    )
    user.set_password(user_form.password)

    db.add(user)
    db.commit()
    return RedirectResponse("/users")


@router.get("/<user_id>")
def get_user(request: Request, user_id: int, user=Depends(admin_only)):
    user = db.query(User).filter(User.id == user_id).all()
    return templates.TemplateResponse("index.html", {"request": request, 'text': text or 'Example'})


@router.post("/<user_id>/password")
def change_password(user_id: int, password: str = Form(...), db: Session = Depends(db_session), user = Depends(admin_only)):
    user = db.query(User).filter(User.id == user_id).all()
    user.set_password(password)
    db.commit()
    return RedirectResponse(f"/users/{user_id}")
