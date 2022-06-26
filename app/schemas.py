from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(BasePost):
    pass


class ResponsePost(BasePost):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    email: EmailStr
    password: str


class CreateUser(BaseUser):
    pass


class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class AuthenticateUser(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
