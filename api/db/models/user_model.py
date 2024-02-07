from typing import Any
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import EmailType

from api.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    display_id: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[EmailType] = mapped_column(EmailType, unique=True)
    icon: Mapped[str] = mapped_column(String)
    header: Mapped[str] = mapped_column(String)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    profile: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    is_initialized: Mapped[bool] = mapped_column(Boolean, default=False)

    @hybrid_method
    async def update_info(self, data: dict[str, Any]) -> None:
        print(self.is_initialized)
        if not self.is_initialized:
            self.is_initialized = True
        for key, value in data.items():
            setattr(self, key, value)
