from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from api.db.base import Base


class FollowModel(Base):
    """Model for follow and follower."""
    __tablename__ = "following"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", onupdate="CASCADE", ondelete="CASCADE")
    )

    follower_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
        nullable=True,
    )

    following_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
        nullable=True,
    )
