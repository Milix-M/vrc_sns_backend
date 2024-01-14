from sqlalchemy import Column, Integer, String, ForeignKey

from api.db.base import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    content = Column(String(500))
    like = Column(Integer, default=0)
    repost = Column(Integer, default=0)