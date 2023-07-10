from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.db_config import get_db
from core.models import UserInput
from core.services import UserManager
from utils.http_exceptions import not_entered_code, user_not_in_changes


async def has_verify(user: UserInput, db: AsyncSession = Depends(get_db)) -> None:
    user_data = await UserManager().retrieve_user_by_email(user.email, db)
    if user_data.verify_code:
        raise not_entered_code


async def is_in_changes(user: UserInput, db: AsyncSession = Depends(get_db)) -> None:
    user_data = await UserManager().retrieve_user_by_email(user.email, db)
    if not user_data.in_changes:
        raise user_not_in_changes
