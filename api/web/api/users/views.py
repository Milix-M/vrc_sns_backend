from fastapi import APIRouter, Depends

from api.web.api.users.schema import AuthenticatedUser
from api.libs.middleware.auth import is_authenticated

router = APIRouter()

@router.get("/me", response_model=AuthenticatedUser)
async def user_me(
    user_info: AuthenticatedUser = Depends(is_authenticated),
) -> AuthenticatedUser:
    return user_info