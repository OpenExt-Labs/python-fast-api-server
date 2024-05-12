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
    tokenUrl="/auth/openapi",
    scheme_name=settings.authentication.scheme,
)


async def get_current_user(token: str = Depends(oauth2_oauth)) -> User:
    try:
        print(f"token {token}")
        payload = jwt.decode(
            token,
            settings.authentication.access_token.secret_key,
            algorithms=[settings.authentication.algorithm],
        )
        print(f"payload {payload}")
        token_payload = TokenPayload(**payload)

        if datetime.fromtimestamp(token_payload.exp) < datetime.now():
            raise AuthenticationError
    except (JWTError, ValidationError):
        logger.exception(JWTError)
        raise AuthenticationError

    user = await UsersRepository().get_by_username(username=token_payload.sub)

    return user
