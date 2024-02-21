from typing import Any
from datetime import date

from sqlalchemy import String, Date
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import EmailType

from api.db.base import Base


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
    followers_count: Mapped[int] = mapped_column(default=0)
    following_count: Mapped[int] = mapped_column(default=0)
    is_initialized: Mapped[bool] = mapped_column(default=False)

    @hybrid_method
    async def update_info(self, data: dict[str, Any]) -> None:
        print(self.is_initialized)
        if not self.is_initialized:
            self.is_initialized = True
        for key, value in data.items():
            setattr(self, key, value)
