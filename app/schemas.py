from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


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


class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(BasePost):
    pass


class ResponsePost(BasePost):
    id: int
    created_at: datetime
    user: ResponseUser

    class Config:
        orm_mode = True


class ResponsePostAndVotes(BaseModel):
    Post: ResponsePost
    votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)
