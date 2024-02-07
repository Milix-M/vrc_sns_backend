from typing import Any
from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import EmailType

from api.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    display_id: Mapped[str] = mapped_column(String(15), unique=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[EmailType] = mapped_column(unique=True)
    icon: Mapped[str]
    header: Mapped[str]
    date_of_birth: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True)
    profile: Mapped[str]
    hashed_password: Mapped[str]
    is_initialized: Mapped[bool] = mapped_column(default=False)

    @hybrid_method
    async def update_info(self, data: dict[str, Any]) -> None:
        print(self.is_initialized)
        if not self.is_initialized:
            self.is_initialized = True
        for key, value in data.items():
            setattr(self, key, value)
