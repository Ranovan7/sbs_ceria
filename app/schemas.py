from fastapi import Form
from pydantic import BaseModel
from typing import Optional, List
import datetime


class BaseUser(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(cls, username: str = Form(...), password: str = Form(...)):
        return cls(username=username, password=password)


class BaseSales(BaseModel):
    nama: str
    kode: str
    alamat: str
    kota: str
    telepon: str
    keterangan: str


class CreateSales(BaseSales):
    username: str
    password: str

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


class CreateBarang(BaseModel):
    batch: str
    expired_date: datetime.date
    stock: str
    obat_id: int

    @classmethod
    def as_form(cls,
        batch: str = Form(...),
        expired_date: datetime.date = Form(...),
        stock: str = Form(...),
        obat_id: int = Form(...)):
        return cls(batch=batch,
            expired_date=expired_date,
            stock=stock,
            obat_id=obat_id)


class BasePelangganSupplier(BaseModel):
    nama: str
    kode: str
    alamat: str
    kota: str
    telepon: str
    keterangan: str


class MasterSupplier(BasePelangganSupplier):
    npwp: str


class MasterPelanggan(BasePelangganSupplier):
    limit: str
    toleransi: str
    diskon: str

    kode_sales: str

    npwp: str
    ppn: str
    pkp: str
    nama_pajak: str
    alamat_pajak: str

    def limit_int(self):
        return None if not self.limit else int(self.limit)

    def toleransi_int(self):
        return None if not self.toleransi else int(self.toleransi)

    def diskon_float(self):
        return None if not self.diskon else float(self.diskon)

    def ppn_bool(self):
        return True if self.ppn == 'True' else False


class BaseObat(BaseModel):
    nama: str
    jenis: str


class BaseItemPenjualan(BaseModel):
    qty: int
    satuan: str
    diskon: Optional(int)
    barang_id: int


class ItemPenjualan(BaseItemPenjualan):
    penjualan_id: int


class BasePenjualan(BaseModel):
    tgl: datetime.datetime
    sales_id: int
    pelanggan_id: int


class Penjualan(BasePenjualan):
    accepted: boolean


class CreatePenjualan(BasePenjualan):
    item_penjualan: List[BaseItemPenjualan]
