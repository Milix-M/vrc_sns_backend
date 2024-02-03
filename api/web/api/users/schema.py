from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    id: int
    username: str
    userid: str | None
    icon: str | None
    headder: str | None
    profile: str | None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    email: str


class AuthenticatedUser(UserBase):
    email: str


class SessionUser(AuthenticatedUser):
    session_cert: Optional[str] = None

# ユーザー情報アップデート時用schema
class UserUpdate(BaseModel):
    username: str | None = None
    userid: str | None = None
