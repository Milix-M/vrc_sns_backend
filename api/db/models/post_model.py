from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from api.db.base import Base

class Post(Base):
    __tablename__ = "posts"

    postid: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(String(500))
    favorite_count: Mapped[int] = mapped_column(Integer, default=0)
    repost_count: Mapped[int] = mapped_column(Integer, default=0)

    # なんもわからんけど動く
    user = relationship("User")