from fastapi import APIRouter, Depends, Response, HTTPException

from api.web.api.users.schema import User, UserCreate
from api.db.dao.user_dao import UserDAO
from api.db.dao.post_dao import PostDAO
from api.web.api.post.schema import Post

router = APIRouter()

@router.post("/post", response_model=Post)
async def add_post(
    ):
    return


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