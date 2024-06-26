from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from src.config import settings
from src.domain.authentication import TokenPayload
from src.domain.users import User, UsersRepository
from src.infrastructure.errors import AuthenticationError

from loguru import logger

__all__ = ("get_current_user",)

oauth2_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={"read": "Read", "write": "Write"},
)


async def get_current_user(token: str = Depends(oauth2_oauth)) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.authentication.access_token.secret_key,
            algorithms=[settings.authentication.algorithm],
        )
        token_payload = TokenPayload(**payload)
        if datetime.fromtimestamp(token_payload.exp) < datetime.now():
            raise AuthenticationError
    except (JWTError, ValidationError):
        logger.exception(JWTError)
        raise AuthenticationError

    user = await UsersRepository().get_by_username(username=token_payload.sub)
    if user is None:
        raise AuthenticationError

    return user
