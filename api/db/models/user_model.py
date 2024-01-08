from sqlalchemy import Column, Integer, String

from api.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    userid = Column(String)
    username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
