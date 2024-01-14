from pydantic import BaseModel

class PostBase(BaseModel):
    userid: int
    content: str

class Post(PostBase):
    postid: int
    like: int
    repost: int

class ShowPost(BaseModel):
    postid: int