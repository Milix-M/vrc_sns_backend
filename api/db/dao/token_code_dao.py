import secrets
from typing import Optional

from fastapi import Depends
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from api.db.dependencies import get_db_session
from api.db.models.token_code_model import TokenCode

class SealAlreadyExpiredError(Exception):
    """ "Error when tried to expire token_code was expired."""

class SealNotFoundError(Exception):
    """Error when not found token_code in database."""

class TokenCodeDAO:
    """Class for accessing token_code table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session
    async def generate_seal(self, nbytes: Optional[int] = 64) -> str:
        """
        This function generates a unique seal for the token code.
        The seal is a URL-safe string of random bytes.
        If the seal already exists and is not expired, a new seal is generated.
        """
        seal = secrets.token_urlsafe(nbytes)

        if await self.is_seal_exist_in_not_expired(seal):
            return await self.generate_seal()

        return seal

    async def create_code(self, user_id: int) -> str:
        seal = await self.generate_seal()
        self.session.add(
            TokenCode(user_id=user_id, seal=seal),
        )

        return seal

    async def get_code(self, token_code_id: int) -> Optional[TokenCode]:
        code = await self.session.get(TokenCode, token_code_id)
        return code

    async def get_code_from_seal(self, seal: str) -> Optional[TokenCode]:
        """
        This function retrieves a token code from the given seal.
        The token code must not be used and the seal must match.
        """
        query = select(TokenCode)
        query = query.filter(
            and_(TokenCode.seal == seal, TokenCode.is_used == False),
        )
        rows = await self.session.execute(query)

        return rows.scalar_one_or_none()

    async def expire_code(self, token_code_id: int) -> None:
        """
        This function expires a token code with the given token code id.
        If the token code is not found, a SealNotFoundError is raised.
        If the token code is already expired, a SealAlreadyExpiredError is raised.
        """
        token_code: Optional[TokenCode] = await self.get_code(token_code_id)
        if token_code is not None:
            if not token_code.is_valid():
                token_code.is_used = True
            elif token_code.is_used:
                raise SealAlreadyExpiredError()
        else:
            raise SealNotFoundError()

    async def is_seal_exist(self, seal: str) -> bool:
        """
        This function checks if the specified seal exists in the database.
        """
        query = select(TokenCode)
        query = query.filter(TokenCode.seal == seal)
        row = await self.session.execute(query)

        return row.scalar_one_or_none() is not None

    async def is_seal_exist_in_not_expired(self, seal: str) -> bool:
        """
        This function checks if the specified seal exists in the database and is not expired.
        """
        query = select(TokenCode)
        query = query.filter(
            and_(TokenCode.seal == seal, TokenCode.is_valid() == false())
        )
        row = await self.session.execute(query)

        return row.scalar_one_or_none() is not None