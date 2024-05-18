from typing import Union
from datetime import datetime, timedelta, timezone
import bcrypt
from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext

from src.domain.users.repository import UsersRepository


router = APIRouter(prefix="/auth", tags=["Auth"])


class AuthRequestBody(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserInDB(User):
    hashed_password: str


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token")
async def auth_openapi(body: AuthRequestBody):
    user = await UsersRepository().get_by_username(username=body.username)
    if not user or not bcrypt.checkpw(
            body.password.encode(),
            user.password.encode()):
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password")

    token = create_access_token(
        data={
            "sub": body.username},
        expires_delta=timedelta(
            days=ACCESS_TOKEN_EXPIRE_DAYS))
    return {"access_token": token, "token_type": "bearer"}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def create_access_token(
        data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
