from sqlalchemy.orm import Session

from api.db.models.user_model import User
from api.web.api.users import schema

from api.libs.security import get_password_hash


def create_user(db: Session, user: schema.UserCreate):
    db_user = User(email=user.email, username=user.username, userid=user.userid, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user