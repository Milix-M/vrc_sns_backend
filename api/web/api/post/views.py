from fastapi import APIRouter, Depends

from api.db.dao.post_dao import PostDAO
from api.web.api.post.schema import PostBase, Post

router = APIRouter()


@router.post("/create", response_model=Post)
async def add_post(
    post: PostBase,
    post_dao: PostDAO = Depends(),
):
    return await post_dao.create_post(
        userid=post.userid,
        content=post.content
    )
    # Todo Validationする、useridじゃなくてcredentialを必須としてそのcredentialに紐付けられているユーザーからpostできるようにする


@router.post("/get-post", response_model=Post)
async def get_post(
):
    return


@router.post("/delete-post")
async def delete_post():
    return


@router.get("/get-latest-post")
async def get_latest_post():
    return
