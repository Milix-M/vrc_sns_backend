
from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.dependencies import get_db_session
from api.db.models.user_follow_model import FollowModel


class FollowDAO:
    """Class for follow table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_user_followers(self, user_id: int) -> List[int]:
        query = select(FollowModel).where(FollowModel.follower_id == user_id)

        rows = await self.session.execute(query)

        return rows.scalars().all()

    async def get_user_following(self, user_id: int) -> List[int]:
        query = select(FollowModel).where(FollowModel.following_id == user_id)

        rows = await self.session.execute(query)

        return rows.scalars().all()

    # async def create_follow(self, follower_id: int, following_id: int) -> FollowModel:
    #     new_follow = FollowModel(follower_id=follower_id, following_id=following_id)
    #     self.session.add(new_follow)
    #     await self.session.commit()

    # async def delete_follow(self, follower_id: int, following_id: int) -> None:
    #     # Delete the relationship
    #     self.session.delete(following_id)
    #     await self.session.commit()
