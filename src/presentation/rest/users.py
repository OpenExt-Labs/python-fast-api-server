from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from loguru import logger

from src.application.authentication import get_current_user
from src.infrastructure.database.transaction import transaction
from src.domain.users.repository import UsersRepository
from src.domain.users.models import User, UserCreateRequestBody, UserPublic, UserUncommited

from src.infrastructure.models import Response, ResponseMulti
import bcrypt

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=201)
@transaction
async def user_create(schema: UserCreateRequestBody) -> Response[UserPublic]:
  try:
    """Create a new user."""
    user = await UsersRepository().get_by_username(username=schema.username)
    if user is not None:
      return JSONResponse(status_code=400, content={"message": "User already exists"}) 
    else:
      hashed_password = bcrypt.hashpw(schema.password.encode(), bcrypt.gensalt())
      schema.password = hashed_password
      user = await UsersRepository().create(UserUncommited(**schema.dict()))
      return Response[UserPublic](result=user)
  except Exception as e:
    logger.exception(e)

@router.get("", status_code=200)
async def users_list() -> ResponseMulti[UserPublic]:
  try:
    """Get all users."""
    users_public = [
        UserPublic.from_orm(user)
        async for user in UsersRepository().all()
    ]
    return ResponseMulti[UserPublic](result=users_public)
  except Exception as e:
    logger.exception(e)

@router.get("/{me}", status_code=200)
async def user_me(user: User = Depends(get_current_user)) -> Response[UserPublic]:
  try:
    """Get the current user."""
    return Response[UserPublic](result=user)
  except Exception as e:
    logger.exception(e)