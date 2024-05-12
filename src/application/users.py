import bcrypt
from src.infrastructure.errors.base import BadRequestError
from src.domain.users.models import User, UserCreateRequestBody, UserUncommited
from src.domain.users.repository import UsersRepository
from src.infrastructure.database.transaction import transaction


@transaction
async def create(payload: UserCreateRequestBody) -> User:
    user = await UsersRepository().get_by_username(username=payload.username)
    if user:
      raise BadRequestError(message=f"{payload.username} already exists") 
    hashed_password = bcrypt.hashpw(payload.password.encode(), bcrypt.gensalt())
    payload.password = hashed_password
    user = await UsersRepository().create(UserUncommited(**payload.dict()))
    return user