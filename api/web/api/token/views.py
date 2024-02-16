from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse

from api.db.dao.session_dao import SessionDAO
from api.db.dao.token_code_dao import TokenCodeDAO
from api.db.dao.user_dao import UserDAO
from api.settings import settings
from api.static import static
from api.web.api.token.schema import JWTTokenPostDTO, TokenCodeDTO

router = APIRouter()


@router.post("/token")
async def generate_token(
    token_code_dto: TokenCodeDTO,
    token_code_dao: TokenCodeDAO = Depends(),
    session_dao: SessionDAO = Depends(),
) -> Response:
    """
    Function to generate a token from a token code.

    This function first retrieves the token code from the database using the seal from the request.
    If the token code is not found, it raises a 400 Bad Request error.
    If the token code is valid, it expires the token code, creates a new session, and returns the session info.
    The session info is returned as a JSON response and also set as a cookie in the response.

    :param token_code_dto: The token code DTO from the request.
    :param token_code_dao: The Data Access Object for token codes, obtained through dependency injection.
    :param session_dao: The Data Access Object for sessions, obtained through dependency injection.
    :returns: The session info as a JSON response with cookies set.
    :raises: HTTPException with status code 400 if the token code is not found.
    :raises: HTTPException with status code 401 if the token code is expired.
    """
    token_code = await token_code_dao.get_code_from_seal(seal=token_code_dto.seal)

    if token_code is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not found seal to generate token.",
        )

    if token_code.is_valid():
        token_code.expire()
        session_info = await session_dao.create(token_code.user_id)
        response = JSONResponse(session_info)
        response.set_cookie(
            key="access_token",
            value=session_info["access_token"],
            max_age=int(static.ACCESS_TOKEN_EXPIRE_TIME.total_seconds()),
            secure=settings.is_production,
            domain=settings.domain,
            samesite="strict",
            httponly=True,
        )
        response.set_cookie(
            key="session_id",
            value=session_info["session_id"],
            max_age=int(static.REFRESH_TOKEN_EXPIRE_TIME.total_seconds()),
            secure=settings.is_production,
            domain=settings.domain,
            samesite="strict",
            httponly=True,
        )

        return response
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Your seal is expired."
    )


@router.post("/token/refresh")
async def generate_jwt_token(
    token_dto: JWTTokenPostDTO,
    user_dao: UserDAO = Depends(),
    session_dao: SessionDAO = Depends(),
    session_id: str = Cookie(default=None),
) -> Response:
    """
    This function is used to generate a new JWT token from a refresh token.
    It first checks if the session_id is present in the request.
    If the session_id is not found, it raises a 400 Bad Request error.
    If the session_id is valid, it generates a new access token and sets it as a cookie in the response.
    The response is returned as a JSON response.

    :param token_dto: The token DTO from the request.
    :param user_dao: The Data Access Object for users, obtained through dependency injection.
    :param session_dao: The Data Access Object for sessions, obtained through dependency injection.
    :param session_id: The session ID from the request, obtained through dependency injection.
    :returns: The response with the new access token set as a cookie.
    :raises: HTTPException with status code 400 if the session_id is not found.
    :raises: HTTPException with status code 401 if the session_id is expired.
    """
    if session_id is None and token_dto.session_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not found session_id in the request.",
        )

    session_cert = ""
    if token_dto.session_id is not None:
        session_cert = token_dto.session_id
    elif session_id is not None:
        session_cert = session_id

    session = await session_dao.get_from_session_cert(session_cert)

    if session is not None and session.is_valid():
        user = await user_dao.get_user_by_id(session.user_id)

        if user is None:
            # Normaly NO WAY!
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error.",
            )

        new_access_token = session_dao.generate_access_token(user)
        response = JSONResponse({"access_token": new_access_token})
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            max_age=int(static.ACCESS_TOKEN_EXPIRE_TIME.total_seconds()),
            secure=settings.is_production,
            domain=settings.domain,
            samesite="strict",
            httponly=True,
        )

        return response
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired session_id."
    )