from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.db.base import Base

class Post(Base):
    __tablename__ = "posts"

    postid = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    content = Column(String(500))
    favorite_count = Column(Integer, default=0)
    repost_count = Column(Integer, default=0)

    # なんもわからんけど動く
    user = relationship("User")