from fastapi import Form
from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    password: str
    role: int

    @classmethod
    def as_form(cls, username: str = Form(...), password: str = Form(...), role: int = Form(...)):
        return cls(username=username, password=password, role=role)
