from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from api.db.base import Base


if TYPE_CHECKING:
    from api.db.models.user_model import User


class Post(Base):
    """Model for Post data."""
    __tablename__ = "posts"

    postid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", onupdate="CASCADE", ondelete="CASCADE"))
    display_id: Mapped[str] = mapped_column(ForeignKey(
        "users.display_id", onupdate="CASCADE", ondelete="CASCADE"
    ))
    content: Mapped[str] = mapped_column(String(500))
    favorite_count: Mapped[int] = mapped_column(default=0)
    repost_count: Mapped[int] = mapped_column(default=0)

    # なんもわからんけど動く
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
