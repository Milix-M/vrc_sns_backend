from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.hybrid import hybrid_method

from api.db.base import Base
from api.static import static

class TokenCode(Base):
    """Model for code token."""

    __tablename__ = "token_code"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    seal = Column(String(100))
    is_used = Column(Boolean, default=False)

    @hybrid_method
    def is_valid(self) -> bool:
        if self.is_used:
            return False

        expire_time = (
            self.created_at.astimezone(static.TIME_ZONE) + static.TOKEN_CODE_EXPIRE_TIME
        )
        return datetime.now(static.TIME_ZONE) < expire_time

    @hybrid_method
    def expire(self) -> None:
        self.is_used = True