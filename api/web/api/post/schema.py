from pydantic import BaseModel

class Post(BaseModel):
    id: int
    userid: int
    content: str
    like: int
    repost: int