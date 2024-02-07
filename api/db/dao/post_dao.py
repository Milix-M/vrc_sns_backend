
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from api.db.dependencies import get_db_session
from api.db.models.post_model import Post


class PostDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_post(
            self,
            user_id: int,
            content: str,
    ) -> Post:
        """
        Creates a new post with the given user id and content.
        """
        post = Post(user_id=user_id, content=content)
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def get_post_by_id(
            self,
            postid: str,
    ) -> Post | None:
        """
        This function reads a post with the given id.
        """
        post = await self.session.execute(select(Post).where(Post.postid == postid))
        return post.scalar_one_or_none()

    async def delete_post(
            self,
            postid: str,
    ) -> None:
        """
        This function deletes a post with the given id.
        """
        post = await self.session.execute(select(Post).where(Post.postid == postid))
        if post is not None:
            self.session.delete(post)
            await self.session.commit()

    async def get_user(
            self,
            post: Post
    ) -> Post:
        await self.session.refresh(post, attribute_names=["user"])
        return post

    async def get_user_posts(
            self,
            user_id: int,
            includeReplies: bool | None,
            limit: int | None,
            sinceid: int | None,
            untilid: int | None,
    ) -> List[Post]:
        """
        Retrieves posts for a specified user ID. Optionally, it can include replies, limit the number of posts retrieved,
        and filter posts within a specific ID range.

        Args:
            user_id (int): User ID for which posts are to be retrieved.
            includeReplies (bool): Boolean indicating whether to include replies in the posts.
            limit (int): The maximum number of posts to retrieve.
            sinceid (int): The lower bound of the post ID range for filtering.
            untilid (int): The upper bound of the post ID range for filtering.

        Returns:
            list[Post]: A list of Post objects.
        """
        query = select(Post).where(Post.user_id == user_id)

        if sinceid is not None:
            query = query.filter(Post.postid > sinceid)

        if untilid is not None:
            query = query.filter(Post.postid < untilid)

        query = query.order_by(Post.created_at.desc()).limit(limit)

        row = await self.session.execute(query)

        return row.scalars().all()
