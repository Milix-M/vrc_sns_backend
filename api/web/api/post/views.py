from fastapi import APIRouter, Depends

from api.db.dao.post_dao import PostDAO
from api.web.api.post.schema import PostBase, Post, ShowPost

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


@router.post("/show", response_model=Post)
async def get_post(
    post: ShowPost,
    post_dao: PostDAO = Depends(),
):
    return await post_dao.get_post_by_id(
        postid=post.id
    )


@router.post("/delete")
async def delete_post():
    return


@router.get("/get-latest")
async def get_latest_post():
    return
