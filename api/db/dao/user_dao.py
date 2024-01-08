from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from api.db.dependencies import get_db_session
from api.db.models.user_model import User
from api.libs.security import get_password_hash

class UserDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_user(
            self,
            userid: str,
            username: str,
            email: str,
            password: str
        ) -> User:
        user = User(userid=userid, username=username, email=email, hashed_password=get_password_hash(password))
        self.session.add(user)
        await self.session.commit()

        return user
        # todo 続きを書く
