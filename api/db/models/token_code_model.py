from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import Mapped, mapped_column

from api.db.base import Base
from api.static import static


class TokenCode(Base):
    """Model for code token."""

    __tablename__ = "token_code"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", onupdate="CASCADE", ondelete="CASCADE"))
    seal: Mapped[str] = mapped_column(String(100))
    is_used: Mapped[bool] = mapped_column(default=False)

    @hybrid_method
    def is_valid(self) -> bool:
        if self.is_used:
            return False

        expire_time = (
            self.created_at.astimezone(
                static.TIME_ZONE) + static.TOKEN_CODE_EXPIRE_TIME
        )
        return datetime.now(static.TIME_ZONE) < expire_time

    @hybrid_method
    def expire(self) -> None:
        self.is_used = True
