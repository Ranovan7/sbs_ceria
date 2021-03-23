from fastapi import Depends
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from app import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app import SessionLocal

Base = declarative_base()
role_str = [
    'admin', # 1
    'sales', # 2
    'gudang' # 3
]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    role = Column(Integer, nullable=False)
    last_login = Column(DateTime)

    @property
    def role_tag(self):
        return role_str[self.role - 1]

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def create_access_token(self, expires_delta: Optional[timedelta] = None):
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {
            "username": self.username,
            "exp": expire
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


class UserLog:
    tanggal = Column(DateTime)
    tindakan = Column(String(6))  # insert, update, delete

    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    object = Column(Text)
    object_id = Column(Integer)


class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    kode = Column(String(3), unique=True, nullable=False)
    nama = Column(Text, nullable=False)
    alamat = Column(Text)
    kota = Column(Text)
    telepon = Column(String(13))
    keterangan = Column(Text)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User", lazy='joined')

    @property
    def user(self):
        db = SessionLocal()
        user = db.query(User).get(self.user_id)
        db.close()
        return user


class Antar(Base):
    __tablename__ = "antar"

    id = Column(Integer, primary_key=True, index=True)
    kode = Column(String(3), unique=True, nullable=False)
    nama = Column(Text, nullable=False)
    alamat = Column(Text)
    kota = Column(Text)
    telepon = Column(String(13))
    keterangan = Column(Text)


class Pelanggan(Base):
    __tablename__ = "pelanggan"

    id = Column(Integer, primary_key=True, index=True)
    kode = Column(Text, unique=True, nullable=False)
    nama = Column(Text, nullable=False)
    alamat = Column(Text)
    kota = Column(Text)
    telepon = Column(String(13))
    keterangan = Column(Text)

    limits = Column(Integer, default=0)
    toleransi = Column(Integer, default=0)
    diskon = Column(Float, default=0)

    sales_id = Column(Integer, ForeignKey('sales.id'), nullable=True)
    info_pajak_id = Column(Integer, ForeignKey('info_pajak.id'), nullable=True)


class Supplier(Base):
    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True, index=True)
    kode = Column(Text, unique=True, nullable=False)
    nama = Column(Text, nullable=False)
    alamat = Column(Text)
    kota = Column(Text)
    telepon = Column(String(13))
    keterangan = Column(Text)

    info_pajak_id = Column(Integer, ForeignKey('info_pajak.id'), nullable=True)


class InfoPajak(Base):
    __tablename__ = "info_pajak"

    id = Column(Integer, primary_key=True, index=True)
    npwp = Column(Text, nullable=False)
    ppn = Column(Boolean)
    pkp = Column(Text)
    nama = Column(Text)
    alamat = Column(Text)

    obj_type = Column(Text)  # supplier, pelanggan
    obj_id = Column(Integer)


class Pabrik(Base):
    __tablename__ = "pabrik"

    id = Column(Integer, primary_key=True, index=True)
    kode = Column(Text, unique=True, nullable=False)
    nama = Column(Text, nullable=False)


class Obat(Base):
    __tablename__ = "obat"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(Text, nullable=False)
    jenis = Column(Text, nullable=False)  # btl, box, tube, dsb

    barang = relationship("Barang", back_populates="obat")


class Barang(Base):
    __tablename__ = "barang"

    id = Column(Integer, primary_key=True, index=True)
    batch = Column(Text, nullable=False)
    expired_date = Column(DateTime, nullable=False)
    stock = Column(Integer, nullable=False, default=1)

    obat_id = Column(Integer, ForeignKey('obat.id'), nullable=True)
    obat = relationship("Obat", back_populates="barang")

    __table_args__ = (UniqueConstraint('batch', 'expired_date', 'obat_id',
                                          name='barang_batch_date_obat'),)


class Penjualan(Base):
    __tablename__ = "penjualan"

    id = Column(Integer, primary_key=True, index=True)
    tgl = Column(DateTime, nullable=False, default=datetime.now())
    accepted = Column(Boolean, nullable=False, default=False)

    sales_id = Column(Integer, ForeignKey('sales.id'), nullable=True)
    pelanggan_id = Column(Integer, ForeignKey('pelanggan.id'), nullable=True)

    item_penjualan = relationship("ItemPenjualan", back_populates="penjualan", lazy='joined')


class ItemPenjualan(Base):
    __tablename__ = "item_penjualan"

    id = Column(Integer, primary_key=True, index=True)
    qty = Column(Integer)
    satuan = Column(String(10))
    diskon = Column(Float)

    penjualan_id = Column(Integer, ForeignKey('penjualan.id'), nullable=True)
    barang_id = Column(Integer, ForeignKey('barang.id'), nullable=True)

    penjualan = relationship("Penjualan", back_populates="item_penjualan")
