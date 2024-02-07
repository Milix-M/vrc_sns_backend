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
    db_display_id = await user_dao.get_user_by_display_id(user.display_id)
    db_email = await user_dao.get_user_by_email(user.email)

    if db_display_id:
        raise HTTPException(status_code=400, detail="display_id is already registered")

    if db_email:
        raise HTTPException(status_code=400, detail="email is already registered")

    return await user_dao.create_user(
        display_id=user.display_id,
        username=user.username,
        email=user.email,
        password=user.password
        )
    #todo 続きを書く