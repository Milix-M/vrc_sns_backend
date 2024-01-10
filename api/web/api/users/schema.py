from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str
    userid: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
