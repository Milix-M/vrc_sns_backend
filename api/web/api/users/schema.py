from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class UserBase(BaseModel):
    id: int
    username: str
    display_id: str | None
    icon: str | None
    header: str | None
    profile: str | None
    date_of_birth: date | None
    created_at: datetime


class UserCreate(BaseModel):
    """
    /api/signin用
    """
    username: str
    display_id: str
    password: str
    email: str
    icon: str | None
    header: str | None
    profile: str | None


class User(UserBase):
    email: str


class AuthenticatedUser(UserBase):
    email: str


class SessionUser(AuthenticatedUser):
    session_cert: Optional[str] = None

# ユーザー情報アップデート時用schema
class UserUpdate(BaseModel):
    username: str | None = None
    display_id: str | None = None
    profile: str | None = None
    date_of_birth: str | None = None
