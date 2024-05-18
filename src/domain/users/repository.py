from typing import AsyncGenerator

from src.infrastructure.database import BaseRepository, UsersTable

from .models import User, UserUncommited

all = ("UsersRepository",)


class UsersRepository(BaseRepository[UsersTable]):
    schema_class = UsersTable

    async def all(self) -> AsyncGenerator[User, None]:
        async for instance in self._all():
            yield User.from_orm(instance)

    async def get_slice(self, offset: int, limit: int) -> AsyncGenerator[User, None]:
        async for instance in self._get_slice(offset=offset, limit=limit):
            yield User.from_orm(instance)

    async def get(self, id_: int) -> User:
        instance = await self._get(key="id", value=id_)
        return User.from_orm(instance)

    async def get_by_username(self, username: str) -> User:
        try:
            instance = await self._get(key="username", value=username)
            return User.from_orm(instance)
        except Exception as e:
            # Handle the not found exception here
            return None

    async def create(self, schema: UserUncommited) -> User:
        try:
            user = await self.get_by_username(username=schema.username)
            if user is not None:
                raise Exception("User already exists")
            instance: UsersTable = await self._save(schema.dict())
            return User.from_orm(instance)
        except Exception as e:
            raise e
