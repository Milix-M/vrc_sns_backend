from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from api.db.base import Base

if TYPE_CHECKING:
    from api.db.models.user_model import User

class FollowModel(Base):
    """Model for follow and follower."""
    __tablename__ = "following"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    follower_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    following_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )


    follower: Mapped["User"] = relationship("User", foreign_keys=[follower_id], back_populates='followers')
    following: Mapped["User"] = relationship("User", foreign_keys=[following_id], back_populates='followings')