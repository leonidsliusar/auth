from abc import ABC, abstractmethod
from sqlalchemy import insert
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
        query = insert(User).values(user_to_inset.model_dump()).returning(User.id, User.email)
        returning_result = await self.db.execute(query)
        user_data = returning_result.mappings().fetchone()
        return UserOutput(**user_data)
