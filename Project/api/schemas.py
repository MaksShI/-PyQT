from pydantic import BaseModel, validator
from typing import Optional


class UserBase(BaseModel):
    login: str
    info: Optional[str] = None
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
