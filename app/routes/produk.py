from fastapi import APIRouter, Request, Depends, Form, Cookie, status
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app import templates
from app.models import Barang, Obat
from app.schemas import CreateBarang
from app.utils import db_session, current_user, admin_only, get_message
from app.utils import RedirectWithMessage, CustomTemplateResponse

router = APIRouter(
    prefix="/produk",
    tags=["produk"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(admin_only)])
async def index(request: Request, user = Depends(current_user), db: Session = Depends(db_session), message = Depends(get_message)):
    obats = db.query(Obat).order_by(Obat.id).all()
    barangs = db.query(Barang).order_by(Barang.id).all()
    return CustomTemplateResponse("produk/index.html", {"request": request, "user": user, 'barangs': barangs, 'obats': obats, 'message': message})


@router.post("/barang", dependencies=[Depends(admin_only)])
async def create_user(barang_form: CreateBarang = Depends(CreateBarang.as_form), user=Depends(current_user), db = Depends(db_session)):
    # create sales
    barang = Barang(
        batch=barang_form.batch,
        expired_date=barang_form.expired_date,
        stock=barang_form.stock,
        obat_id=barang_form.obat_id
    )

    db.add(barang)
    db.commit()
    db.refresh(barang)

    return RedirectResponse("/produk", status_code=status.HTTP_303_SEE_OTHER)
