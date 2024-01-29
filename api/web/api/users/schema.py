from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: str
    username: str
    userid: str | None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int


class AuthenticatedUser(UserBase):
    id: int


class SessionUser(AuthenticatedUser):
    session_cert: Optional[str] = None

# ユーザー情報アップデート時用schema
class UserUpdate(BaseModel):
    username: str
    userid: str
