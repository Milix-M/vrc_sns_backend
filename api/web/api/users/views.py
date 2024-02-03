from fastapi import APIRouter, Depends, Response, Path
from fastapi.responses import JSONResponse

from api.db.dao.user_dao import UserDAO
from api.web.api.users.schema import AuthenticatedUser, UserBase, UserUpdate, User
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
    user_info: AuthenticatedUser = Depends(is_authenticated),
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
    await user.update_info(data=user_update.model_dump(exclude_unset=True))

    update_info = {
        "detail": "successfully updated."
    }

    response = JSONResponse(update_info)
    return response


@router.get("/{user_id}/info", response_model=UserBase)
async def get_user_info(
    user_id: str = Path(title="User id of the user to be retrieved"),
    user_dao: UserDAO = Depends(),
) -> UserBase:
    """
    Get user information.
    Args:
        user_info (str): The user user_id.
        user_dao (UserDAO): The user data access object.

    Returns:
        UserBase: return UserBase schema.
    """
    userdata = await user_dao.get_user_by_userid(userid=user_id)

    return userdata


@router.get("/initialized", response_model=bool)
async def user_initialized(
    user_info: AuthenticatedUser = Depends(is_authenticated),
    user_dao: UserDAO = Depends(),
) -> bool:
    """check user already initilized"""

    userdata = await user_dao.get_user_by_id(id=user_info.id)

    return userdata.is_initialized
