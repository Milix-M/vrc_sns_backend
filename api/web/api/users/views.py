from typing import List
from fastapi import APIRouter, Depends, Response, Path, HTTPException, status
from fastapi.responses import JSONResponse
from api.db.dao.post_dao import PostDAO

from api.db.dao.user_dao import UserDAO
from api.db.dao.user_follow_dao import FollowDAO
from api.web.api.users.schema import AuthenticatedUser, UserBase, UserUpdate, User
from api.web.api.post.schema import PostWOUser, UserPostsGet
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
    user = await user_dao.get_user_by_id(user_id=user_info.id)
    await user.update_info(data=user_update.model_dump(exclude_unset=True))

    update_info = {
        "detail": "successfully updated."
    }

    response = JSONResponse(update_info)
    return response


@router.get("/{display_id}/info", response_model=UserBase)
async def get_user_info(
    display_id: str = Path(title="display id of the user to be retrieved"),
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
    userdata = await user_dao.get_user_by_display_id(display_id=display_id)

    if userdata:
        return userdata

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="user id is not found."
    )


@router.get("/initialized", response_model=bool)
async def user_initialized(
    user_info: AuthenticatedUser = Depends(is_authenticated),
    user_dao: UserDAO = Depends(),
) -> bool:
    """check user already initilized"""

    userdata = await user_dao.get_user_by_id(user_id=user_info.id)

    return userdata.is_initialized


@router.get("/{display_id}/posts", response_model=List[PostWOUser])
async def user_posts(
    display_id: str = Path(title="display id of the user to be retrieved"),
    get_post_info: UserPostsGet = Depends(),
    post_dao: PostDAO = Depends(),
) -> List[PostWOUser]:
    """
    Get user posts.
    """

    return await post_dao.get_user_posts(
        display_id=display_id,
        **get_post_info.model_dump()
    )

# follwersとfollowingsは統合するべきかもしれない

@router.get("/{display_id}/followers")
async def get_follwers(
    display_id: str = Path(title="display id of the user to be retrieved"),
    user_dao: UserDAO = Depends(),
    follow_dao: FollowDAO = Depends(),
) -> List[int]:
    userdata = await user_dao.get_user_by_display_id(display_id=display_id)

    if userdata is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user is not found."
        )

    return await follow_dao.get_user_followers(
        userdata.id
    )

@router.get("/{display_id}/followings")
async def get_follwers(
    display_id: str = Path(title="display id of the user to be retrieved"),
    user_dao: UserDAO = Depends(),
    follow_dao: FollowDAO = Depends(),
) -> List[int]:
    userdata = await user_dao.get_user_by_display_id(display_id=display_id)

    if userdata is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user is not found."
        )

    return await follow_dao.get_user_following(
        userdata.id
    )
