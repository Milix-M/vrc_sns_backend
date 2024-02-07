from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from api.db.dependencies import get_db_session
from api.db.models.user_model import User
from api.libs.security import get_password_hash


class UserDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_user(
        self,
        display_id: str,
        username: str,
        email: str,
        password: str
    ) -> User:
        if password:
            user = User(display_id=display_id, username=username, email=email,
                        hashed_password=get_password_hash(password))
        # Googleログイン用
        else:
            user = User(display_id=display_id, username=username, email=email,
                        hashed_password="")

        self.session.add(user)
        await self.session.commit()

        return user

    async def get_user_by_id(self, user_id: int):
        """Function can get the user from id.

        If not found, return None.

        :param user_id: id of the user you want to get.
        :returns: if not found user, will return None.
        """
        query = select(User).where(User.id == user_id)
        rows = await self.session.execute(query)

        return rows.scalar_one_or_none()


    async def get_user_by_display_id(self, display_id: str):
        """Function can get the user from user_display_id.

        If not found, return None.

        :param display_id: email of the user you want to get.
        :returns: if not found user, will return None.
        """
        query = select(User).where(User.display_id == display_id)
        rows = await self.session.execute(query)

        return rows.scalar_one_or_none()

    async def get_user_by_email(self, email: str):
        """Function can get the user from user_email.

        If not found, return None.

        :param email: email of the user you want to get.
        :returns: if not found user, will return None.
        """
        query = select(User).where(User.email == email)
        rows = await self.session.execute(query)

        return rows.scalar_one_or_none()
