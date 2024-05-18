from fastapi import APIRouter
from fastapi.params import Depends
from loguru import logger

from src.application.authentication import get_current_user
from src.domain.users.repository import UsersRepository
from src.domain.users.models import User, UserCreateRequestBody, UserPublic

from src.infrastructure.models import Response, ResponseMulti
from src.application import users

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=201)
async def user_create(schema: UserCreateRequestBody) -> Response[UserPublic]:
    """Create a new user."""
    user: User = await users.create(schema)
    return Response[UserPublic](result=user)


# Get slice with pagination
@router.get("", status_code=200)
async def users_list(offset: int = 0, limit: int = 10) -> ResponseMulti[UserPublic]:
    try:
        users_public = [
            UserPublic.from_orm(user)
            async for user in UsersRepository().get_slice(offset, limit)
        ]
        return ResponseMulti[UserPublic](result=users_public)
    except Exception as e:
        logger.exception(e)


@router.get("/{me}", status_code=200)
async def user_me(user: User = Depends(
        get_current_user)) -> Response[UserPublic]:
    return Response[UserPublic](result=user)
