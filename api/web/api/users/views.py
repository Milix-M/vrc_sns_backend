from fastapi import APIRouter, Depends

from api.db.dao.user_dao import UserDAO
from api.web.api.users.schema import AuthenticatedUser
from api.libs.middleware.auth import is_authenticated

router = APIRouter()


@router.get("/me", response_model=AuthenticatedUser)
async def user_me(
    user_info: AuthenticatedUser = Depends(is_authenticated),
) -> AuthenticatedUser:
    return user_info


@router.get("/initialized", response_model=bool)
async def user_initialized(
    user_info: AuthenticatedUser = Depends(is_authenticated),
    user_dao: UserDAO = Depends(),
) -> bool:
    """check user already initilized"""

    userdata = await user_dao.get_user_by_id(id=user_info.id)

    return userdata.is_initialized
