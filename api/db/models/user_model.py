from typing import TYPE_CHECKING, Any, List
from datetime import date

from sqlalchemy import String, Date
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import EmailType

from api.db.base import Base

if TYPE_CHECKING:
    from api.db.models.user_follow_model import FollowModel


class User(Base):
    """Model for user data."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    display_id: Mapped[str | None] = mapped_column(String(15), unique=True)
    username: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[EmailType] = mapped_column(EmailType, unique=True)
    icon: Mapped[str | None]
    header: Mapped[str | None]
    date_of_birth: Mapped[date | None] = mapped_column(
        Date())
    profile: Mapped[str | None]
    hashed_password: Mapped[str]
    is_initialized: Mapped[bool] = mapped_column(default=False)

    # followers: Mapped["FollowModel"] = relationship("FollowModel", foreign_keys='FollowModel.follower_id', back_populates='follower')
    # followings: Mapped["FollowModel"] = relationship("FollowModel", foreign_keys='FollowModel.following_id', back_populates='following')

    @property
    def followers_count(self):
        # print(self.followers)
        # print(111111111111111)
        # print(self.followers)
        # return await self.followers.count()
        return 111
    
    @property
    def following_count(self):
        # print(self.followings)
        # return self.followings.count()
        return 1

    @hybrid_method
    async def update_info(self, data: dict[str, Any]) -> None:
        print(self.is_initialized)
        if not self.is_initialized:
            self.is_initialized = True
        for key, value in data.items():
            setattr(self, key, value)
