import datetime
from pydantic import BaseModel, Field

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

class PostWOUser(BaseModel):
    """
    userのpost取得など,userの情報がすべて全く同じ時の為のschema
    """
    postid: int
    content: str
    created_at: datetime.datetime
    favorite_count: int
    repost_count: int

class UserPostsGet(BaseModel):
    userid: int
    includeReplies: bool | None = Field(False, description="Whether to include replies or not")
    limit: int | None = Field(15, description="Limit for fetching posts")
    sinceid: int | None = Field(None)
    untilid: int | None = Field(None)

class PostID(BaseModel):
    postid: int