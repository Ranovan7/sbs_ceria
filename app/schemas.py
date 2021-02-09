from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    password: str
    role: int
