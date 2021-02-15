from fastapi import Depends
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from app import SECRET_KEY, ALGORITHM
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

    @property
    def role_tag(self):
        return role_str[self.role - 1]

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def create_access_token(self, expires_delta: Optional[timedelta] = None):
        to_encode = {
            "username": self.username
        }
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=720)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


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

    limit = Column(Integer, default=0)
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
    npwp = Column(Text, unique=True, nullable=False)
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
