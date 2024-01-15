import urllib
from typing import Dict, List, Optional

import httpx

from api.static import static


class FaildRetrieveAccessTokenError(Exception):
    """Raised when failed to retrieve access token."""


async def get_token(
    code: str,
    client_id: Optional[str],
    client_secret: Optional[str],
    redirect_uri: str,
    grant_type: str = "authorization_code",
) -> str:
    """Function to get access token from Google API.

    This function is to get access token from Google API and return it.

    :param code: String will use to get access token.
    :param client_id: The client_id of the Google APP.
    :param client_secret: The client_secret of the Google APP.
    :param redirect_uri: The redirect uri.
    :param grant_type: The grant type.
    :returns: The access token
    :raises FaildRetrieveAccessTokenError: if can't retrieve access token
    """
    params = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": grant_type,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(static.GOOGLE_TOKEN_URL, data=params)
        token_data = response.json()

    if "access_token" not in token_data:
        raise FaildRetrieveAccessTokenError()

    return token_data["access_token"]


async def get_user_info(access_token: str) -> Dict[str, str]:
    """Get user info from Google API using access_token.

    This function returns user information

    :param access_token: The access token of google
    :returns: Returns the userinfo in dictionary.
    """
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(static.GOOGLE_USER_INFO_URL, headers=headers)
        user_info = response.json()

    return user_info


def auth_url(
    client_id: str,
    redirect_uri: str,
    scope: str | List[str] = ["openid", "profile", "email"].copy(),
    response_type: str = "code",
    **kwargs: str | List[str],
) -> str:
    """Generate authorization link for Google login.

    :param client_id: client_id of Google APP.
    :param redirect_uri: redirect_uri of Google APP
    :param scope: Scope of the Google API
    :param response_type: responce type of the Google API
    :param **kwargs: Custom parameters
    :returns: authorization_link for google login.
    """
    if not static.GOOGLE_AUTH_URL.endswith("?"):
        google_auth_url = f"{static.GOOGLE_AUTH_URL}?"

    params: Dict[str, str | List[str]] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": response_type,
        "scope": scope,
    }
    params.update(kwargs)
    for param, value in params.items():
        if isinstance(value, list):
            params[param] = urllib.parse.quote(" ".join(value))

    params = [f"{p}={v}" for p, v in params.items()]  # type: ignore
    parameters = "&".join(params)

    return google_auth_url + parameters