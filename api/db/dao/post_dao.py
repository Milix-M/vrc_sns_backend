from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from api.db.dependencies import get_db_session
from api.db.models.user_model import User
from api.db.models.post_model import Post
from api.libs.security import get_password_hash

class PostDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_post(
            self,
            userid: str,
            content: str,
    ) -> Post:
        """
        Creates a new post with the given user id and content.
        """
        post = Post(userid=userid, content=content)
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def get_post_by_id(
            self,
            postid: str,
    ) -> Post:
        """
        This function reads a post with the given id.
        """
        post = await self.session.execute(select(Post).where(Post.id == postid))
        return post.scalar_one_or_none()

    async def delete_post(
            self,
            postid: str,
    ) -> None:
        """
        This function deletes a post with the given id.
        """
        post = await self.session.execute(select(Post).where(Post.id == postid))
        if post is not None:
            self.session.delete(post)
            await self.session.commit()
