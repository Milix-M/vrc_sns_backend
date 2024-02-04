from typing import Any
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.hybrid import hybrid_method

from api.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    userid = Column(String, unique=True)
    username = Column(String)
    email = Column(String, unique=True)
    icon = Column(String)
    header = Column(String)
    date_of_birth = Column(DateTime(timezone=True), nullable=True)
    profile = Column(String)
    hashed_password = Column(String)
    is_initialized = Column(Boolean, default=False)

    @hybrid_method
    async def update_info(self, data: dict[str, Any]) -> None:
        print(self.is_initialized)
        if not self.is_initialized:
            self.is_initialized = True
        for key, value in data.items():
            setattr(self, key, value)
