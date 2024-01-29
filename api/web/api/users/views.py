from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from api.db.dao.user_dao import UserDAO
from api.web.api.users.schema import AuthenticatedUser, UserUpdate, User
from api.libs.middleware.auth import is_authenticated

router = APIRouter()


@router.get("/me", response_model=AuthenticatedUser)
async def user_me(
    user_info: AuthenticatedUser = Depends(is_authenticated),
) -> AuthenticatedUser:
    return user_info


@router.patch("/me")
async def update_user(
    user_update: UserUpdate,
    user_info: User = Depends(is_authenticated),
    user_dao: UserDAO = Depends(),
) -> Response:
    """
    Update user information.
    Args:
        user_update (UserUpdate): The updated user information.
        user_info (User): The authenticated user information.
        user_dao (UserDAO): The user data access object.

    Returns:
        Response: The HTTP response.
    """
    user = await user_dao.get_user_by_id(id=user_info.id)
    user.update_info(data=user_update.model_dump())

    update_info = {
        "detail": "successfully updated."
    }

    response = JSONResponse(update_info)
    return response


@router.get("/initialized", response_model=bool)
async def user_initialized(
    user_info: AuthenticatedUser = Depends(is_authenticated),
    user_dao: UserDAO = Depends(),
) -> bool:
    """check user already initilized"""

    userdata = await user_dao.get_user_by_id(id=user_info.id)

    return userdata.is_initialized
