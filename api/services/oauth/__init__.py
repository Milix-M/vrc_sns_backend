"""OAuth login service."""

from fastapi import HTTPException


class NotVerifiedEmailError(HTTPException):
    """Raised when a user is not verified email."""