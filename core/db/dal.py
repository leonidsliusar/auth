from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.schema import User
from core.models import UserInput, UserOutput
from utils.hasher import hash_pass


class BaseManager(ABC):
    __slots__ = 'db'

    def __init__(self, db: AsyncSession):
        self.db = db

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get(self, *args, **kwargs):
        pass


class UserManager(BaseManager):

    async def create(self, user: UserInput) -> UserOutput:
        user_to_inset = user.model_copy()
        user_to_inset.password = hash_pass(user.password)
        query = insert(User).values(user_to_inset.model_dump()).returning(User.id, User.email, User.is_active)
        returning_result = await self.db.execute(query)
        user_data = returning_result.mappings().fetchone()
        return UserOutput(**user_data)

    async def get(self, user_id: str) -> Optional[UserOutput]:
        query = select(User.id, User.email, User.is_active).where(User.id == user_id)
        returning_result = await self.db.execute(query)
        user_data = returning_result.mappings().fetchone()
        if user_data:
            user = UserOutput(**user_data)
            return user

    async def update_password(self, user: UserInput) -> Optional[UserOutput]:
        new_password = user.password
        new_password_hashed = hash_pass(new_password)
        query = update(User).where(User.email == user.email).values(password=new_password_hashed).returning(
            User.id, User.email, User.is_active)
        returning_result = await self.db.execute(query)
        user_data = returning_result.mappings().fetchone()
        if user_data:
            user = UserOutput(**user_data)
            return user
