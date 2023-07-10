from fastapi.security import OAuth2PasswordBearer
from core.db.db_config import get_db
from core.models import AuthUser, UserOutput
from core.services import UserManager
from core.settings import settings
from utils.hasher import check_hash
from datetime import timedelta, datetime
from fastapi import HTTPException, Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from jose import JWTError, jwt

from utils.http_exceptions import credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")
manager = UserManager()


async def authenticate(data: AuthUser, db: AsyncSession):
    user = await manager.retrieve_user_by_email(data.email, db)
    flag = check_hash(data.password, user.password)
    if not flag:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid password',
            headers={"WWW-Authenticate": "Bearer"}
        )


def create_token(data: dict, tlc: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + tlc
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict,
                         tlc: timedelta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_IN)) -> tuple[str, datetime]:
    to_encode = data.copy()
    expire = datetime.utcnow() + tlc
    to_encode.update({'exp': expire})
    encoded_jwt_refresh = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt_refresh, expire


def decode_token(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    return payload


async def get_user_from_token(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> UserOutput:
    try:
        payload = decode_token(token)
        email = payload.get('sub')
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    manager = UserManager()
    user_data = await manager.retrieve_user_by_email(email, db)
    if not user_data:
        raise credentials_exception
    user_data.password = None
    return user_data


async def get_user_from_refresh_token(refresh_token: str = Cookie(...), db: AsyncSession = Depends(get_db)) -> str:
    try:
        print(refresh_token)
        payload = decode_token(refresh_token)
        email = payload.get('sub')
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    manager = UserManager()
    user_data = await manager.retrieve_user_by_email(email, db)
    if not user_data:
        raise credentials_exception
    return user_data.email
