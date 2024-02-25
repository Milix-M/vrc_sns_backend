
from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.dependencies import get_db_session
from api.db.models.user_follow_model import FollowModel
from api.web.api.users.schema import UserBase


class FollowDAO:
    """Class for follow table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_user_followers(self, user_id: int) -> List[UserBase]:
        query = select(FollowModel).where(FollowModel.follower_id == user_id).options(selectinload(FollowModel.follower))

        rows = await self.session.execute(query)
    
        followers = [row.follower for row in rows.scalars().all()]
        return followers


    async def get_user_following(self, user_id: int) -> List[UserBase]:
        query = select(FollowModel).where(FollowModel.following_id == user_id).options(selectinload(FollowModel.following))

        rows = await self.session.execute(query)
    
        following = [row.following for row in rows.scalars().all()]
        return following

    async def check_aleady_following(self, follower_id: int, following_id: int):
        query = select(FollowModel)
        query = query.filter(FollowModel.follower_id == follower_id,
                             FollowModel.following_id == following_id)

        row = await self.session.execute(query)

        return row.scalar_one_or_none()

    async def create_follow(self, follower_id: int, following_id: int) -> FollowModel:
        new_follow = FollowModel(
            follower_id=follower_id, following_id=following_id)
        self.session.add(new_follow)
        await self.session.commit()

    async def delete_follow(self, follower_id: int, following_id: int) -> None:
        query = select(FollowModel)
        query = query.filter(FollowModel.follower_id == follower_id,
                             FollowModel.following_id == following_id)

        follow_row = (await self.session.execute(query)).scalar_one_or_none()

        if follow_row is not None:
            await self.session.delete(follow_row)
            await self.session.commit()
