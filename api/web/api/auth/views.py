from fastapi import APIRouter, Depends, Response

from api.web.api.users.schema import User, UserCreate
from api.db.dao.user_dao import UserDAO

router = APIRouter()

@router.post("/signin")
async def create_user(
    user: UserCreate,
    user_dao: UserDAO = Depends(),
    ) -> Response:
    """
    Create User endpoint.
    """
    await user_dao.create_user(
        userid=user.userid,
        username=user.username,
        email=user.email,
        password=user.password
        )
    return
    #todo 続きを書く