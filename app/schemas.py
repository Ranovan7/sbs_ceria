from fastapi import Form
from pydantic import BaseModel
from typing import Optional


class CreateSales(BaseModel):
    nama: str
    kode: str
    username: str
    password: str
    alamat: str
    kota: str
    telepon: str
    keterangan: str

    @classmethod
    def as_form(cls,
        nama: str = Form(...),
        kode: str = Form(...),
        username: str = Form(...),
        password: str = Form(...),
        alamat: Optional[str] = Form(""),
        kota: Optional[str] = Form(""),
        telepon: Optional[str] = Form(""),
        keterangan: Optional[str] = Form("")):
        return cls(nama=nama,
            kode=kode,
            username=username,
            password=password,
            alamat=alamat,
            kota=kota,
            telepon=telepon,
            keterangan=keterangan)
