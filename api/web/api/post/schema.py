import datetime
from pydantic import BaseModel

from api.web.api.users.schema import UserBase

class PostCreate(BaseModel):
    content: str

class Post(BaseModel):
    postid: int
    content: str
    created_at: datetime.datetime
    user: UserBase
    userid: int
    favorite_count: int
    repost_count: int

class PostID(BaseModel):
    postid: int