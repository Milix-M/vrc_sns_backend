from typing import TYPE_CHECKING, Optional

from fastapi import Cookie, Depends, Header, HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt

from api.db.dao.user_dao import UserDAO
from api.settings import settings

if TYPE_CHECKING:
    from api.web.api.users.schema import SessionUser

async def is_authenticated(
        user_dao: UserDAO = Depends(),
        access_token: str = Cookie(default=None),
        session_id: str = Cookie(default=None),
        authorization: Optional[str] = Header(default=None),
) -> "SessionUser":
    """Middleware function to check if the user is authenticated.

    This function checks the provided authorization credentials
    and returns the authenticated user if the credentials are valid.
    :param user_dao: The UserDAO instance to use for user authentication.
    :param access_token: The access token from the cookie (default: None).
    :param session_id: The session ID from the cookie (default: None).
    :param authorization: The authorization header (default: None).
    :returns: The authenticated user if the credentials are valid.
    :raises: HTTPException if the credentials are missing, expired, or invalid.
    """
    from api.web.api.users.schema import SessionUser

    if authorization is None and access_token is None:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization credentials is missing.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_request"'},
        )

    if authorization is not None:
        jwt_token = authorization.rsplit(maxsplit=1)[-1]
    elif access_token is not None:
        jwt_token = access_token
    else:
        raise HTTPException(
            status_code=401,
            detail="Token has expired.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )

    try:
        payload = jwt.decode(
            jwt_token, settings.token_secret_key, algorithms=[settings.token_algorithm]
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )

    user = await user_dao.get_user_by_id(payload["user_id"])

    if user is not None:
        authenticated_user = SessionUser.model_validate(user, from_attributes=True)
        if session_id is not None:
            authenticated_user.session_cert = session_id
        return authenticated_user

    raise HTTPException(
        status_code=404,
        detail="Not found user.",
        headers={"WWW-Authenticate": 'Bearer error="not_found_user"'},
    )