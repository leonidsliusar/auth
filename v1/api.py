from email.utils import formatdate

from fastapi import Depends, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from core.auth_backend.authenticate import authenticate, create_token, create_refresh_token, decode_token, \
    get_user_from_token, get_user_from_refresh_token
from core.services import UserManager
from core.db.db_config import get_db
from core.models import UserInput, UserOutput, AuthUser
from utils.dependencies import is_in_changes, has_verify
from utils.http_exceptions import user_doesnt_exist, bad_code, bad_token
from v1.routers import reg, auth
from uuid import UUID
from fastapi import Response

manager = UserManager()


@reg.post('')
async def register(user: UserInput, db: AsyncSession = Depends(get_db)) -> UserOutput:
    user = await manager.create_user(user, db)
    return user


@reg.get('/{user_id}')
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> UserOutput:
    user = await manager.retrieve_user(str(user_id), db)
    if not user:
        raise user_doesnt_exist
    return user


@reg.post('/pass_unset')
async def reset_password(email: str, db: AsyncSession = Depends(get_db)) -> dict:
    user_data = await manager.unset_password(email, db)
    if not user_data:
        raise user_doesnt_exist
    return {'status': 'await validation'}


@reg.post('/verify_code')
async def verify_code(email: str, code: str, db: AsyncSession = Depends(get_db)) -> dict:
    verify_flag = await manager.verify(email, code, db)
    if not verify_flag:
        raise bad_code
    return {'status': 'success'}


@reg.post('/pass_set')
async def set_password(user: UserInput, db: AsyncSession = Depends(get_db), check_verify: None = Depends(has_verify),
                       in_changes: None = Depends(is_in_changes)) -> UserOutput:
    user = await manager.set_password(user, db)
    return user


@auth.post('/login/token')
async def authentication(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                         db: AsyncSession = Depends(get_db)) -> dict:
    data = {"email": form_data.username, "password": form_data.password}
    user = AuthUser(**data)
    await authenticate(user, db)
    access_token = create_token({"sub": form_data.username})
    refresh_token, expire = create_refresh_token({"sub": form_data.username})
    expires_str = formatdate(expire.timestamp(), usegmt=True)
    response.set_cookie(key='refresh_token', httponly=True, value=refresh_token, expires=expires_str, path='/auth')
    return {"access_token": access_token, "token_type": "bearer"}


@auth.post('/refresh')
async def refresh_token(email: str = Depends(get_user_from_refresh_token)) -> dict:
    access_token = create_token({"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}


@auth.post('/logout')
async def logout(response: Response) -> Response:
    response.delete_cookie(key='refresh_token', path='/auth')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
