from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import insert, select, update, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.schema import User
from utils.regex_checker import RegexIn


class BaseManager(ABC):
    __slots__ = 'db'

    def __init__(self, db: AsyncSession):
        self.db = db

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    async def retrieve(self, *args, **kwargs):
        pass

    @abstractmethod
    async def update(self, *args, **kwargs):
        pass


class StorageManager(BaseManager):

    async def create(self, user_data: dict) -> dict:
        query = insert(User).values(user_data).returning(User.id, User.email, User.bot_type)
        returning_result = await self.db.execute(query)
        user_data = returning_result.fetchone()._asdict()
        return user_data

    async def retrieve(self, user_param: str) -> Optional[dict]:
        match RegexIn(user_param):
            case r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b':
                query = select(User).where(User.email == user_param)
            case _:
                query = select(User).where(User.id == user_param)
        returning_result = await self.db.execute(query)
        user_data = returning_result.scalar()
        if user_data:
            user_data = user_data.__dict__
            user_data.pop('_sa_instance_state')
            return user_data

    async def update(self, user_email: str, user_password: Optional[str] = None,
                     verify_code: Optional[str] = None) -> Optional[dict]:
        if user_password:
            query = update(User).where(User.email == user_email).values(
                password=user_password, in_changes=False).returning(User.id, User.email, User.bot_type)
        else:
            query = update(User).where(User.email == user_email).values(
                verify_code=verify_code, in_changes=True).returning(User.id, User.email)
        returning_result = await self.db.execute(query)
        try:
            user_data = returning_result.fetchone()._asdict()
        except AttributeError:
            user_data = None
        return user_data

    async def unset_verify_status(self, email: str) -> None:
        query = update(User).where(User.email == email).values(verify_code=None)
        await self.db.execute(query)
