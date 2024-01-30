from pydantic import BaseModel

class PostBase(BaseModel):
    content: str

class Post(PostBase):
    userid: int
    postid: int
    like: int
    repost: int

class PostID(BaseModel):
    postid: int