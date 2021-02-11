from fastapi import Depends
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from app import SECRET_KEY, ALGORITHM
from app import db_session

Base = declarative_base()
role_str = [
    'admin',
    'sales',
    'gudang'
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
    kode = Column(String(2), unique=True, nullable=False)
    nama = Column(Text, nullable=False)
    alamat = Column(Text)
    kota = Column(Text)
    telepon = Column(String(13))
    keterangan = Column(Text)
    bayar = Column(Integer, default=0)
    total_jual = Column(Integer, default=0)
    jumlah_komi = Column(Integer)
    komisi = Column(Integer)
    total_retur = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    @property
    def user(self, db: Session = Depends(db_session)):
        return db.query(User).get(self.user_id)
