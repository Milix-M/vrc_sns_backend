from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.db.dao.post_dao import PostDAO
from api.web.api.post.schema import PostBase, Post, PostID
from api.web.api.users.schema import AuthenticatedUser
from api.libs.middleware.auth import is_authenticated

router = APIRouter()


@router.post("/create", response_model=Post)
async def add_post(
    post: PostBase,
    user_info: AuthenticatedUser = Depends(is_authenticated),
    post_dao: PostDAO = Depends(),
) -> Post:
    return await post_dao.create_post(
        userid=user_info.id,
        content=post.content
    )


@router.post("/show", response_model=Post)
async def get_post(
    post: PostID,
    post_dao: PostDAO = Depends(),
):
    post_data = await post_dao.get_post_by_id(post)

    if post_data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post not found. Please check the post ID and try again."
        )

    return await post_dao.get_post_by_id(
        postid=post.postid
    )


@router.post("/delete")
async def delete_post(
    postid: PostID,
    post_dao: PostDAO = Depends(),
):
    post_data = await post_dao.get_post_by_id(postid)

    if post_data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post not found. Please check the post ID and try again."
        )

    return await post_dao.delete_post(
        postid=postid.postid
    )


@router.get("/get-latest")
async def get_latest_post():
    return
