from fastapi import APIRouter, Depends, Response, HTTPException

from api.web.api.users.schema import User, UserCreate
from api.db.dao.user_dao import UserDAO

router = APIRouter()

@router.post("/signin", response_model=User)
async def create_user(
    user: UserCreate,
    user_dao: UserDAO = Depends(),
    ) -> Response:
    """
    Create User endpoint.
    """
    db_userid = await user_dao.get_user_by_userid(user.userid)
    if db_userid:
        raise HTTPException(status_code=400, detail="userid is already registered")

    return await user_dao.create_user(
        userid=user.userid,
        username=user.username,
        email=user.email,
        password=user.password
        )
    #todo 続きを書く