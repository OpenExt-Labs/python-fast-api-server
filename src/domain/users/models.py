from pydantic import Field
from src.infrastructure.models import InternalModel, PublicModel

__all__ = ("UserUncommited", "User", "UserCreateRequestBody", "UserPublic")


class _UserInternal(InternalModel):
    username: str
    password: str 
    email: str


# Internal models
# ------------------------------------------------------
class UserUncommited(_UserInternal):
    """This schema is used for creating instance in the database."""
    pass


class User(_UserInternal):
    """Existed product representation."""
    id: int


# Public models
class _UserPublic(PublicModel):
    username: str = Field(description="User name")
    email: str = Field(description="User email")

class UserPublic(_UserPublic):
    """User public model."""
    id: int = Field(description="User id")

class UserCreateRequestBody(_UserPublic):
    """Product create request body."""
    password: str = Field(description="User password")
