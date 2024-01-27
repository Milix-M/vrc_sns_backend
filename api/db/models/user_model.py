from sqlalchemy import Column, Integer, String, Boolean

from api.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    userid = Column(String, unique=True)
    username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_initialized: Column(Boolean, default=False)
