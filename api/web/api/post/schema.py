from pydantic import BaseModel

class PostBase(BaseModel):
    userid: int
    content: str

class Post(PostBase):
    id: int
    like: int
    repost: int

class ShowPost(BaseModel):
    id: int