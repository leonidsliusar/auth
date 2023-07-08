from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.dal import UserManager
from core.db.db_config import get_db
from core.models import UserInput, UserOutput
from v1.routers import reg


@reg.post('')
async def register(user: UserInput, db: AsyncSession = Depends(get_db)) -> UserOutput:
    manager = UserManager(db)
    user = await manager.create(user)
    return user
