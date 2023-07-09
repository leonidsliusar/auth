from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.dal import UserManager
from core.db.db_config import get_db
from core.models import UserInput, UserOutput
from v1.routers import reg
from uuid import UUID


@reg.post('')
async def register(user: UserInput, db: AsyncSession = Depends(get_db)) -> UserOutput:
    manager = UserManager(db)
    user = await manager.create(user)
    return user


@reg.get('/{user_id}')
async def register(user_id: UUID, db: AsyncSession = Depends(get_db)) -> UserOutput:
    manager = UserManager(db)
    user = await manager.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User does\'t exists')
    return user


@reg.put('/reset')
async def reset_password(user: UserInput, db: AsyncSession = Depends(get_db)) -> UserOutput:
    manager = UserManager(db)
    """HERE IS NEED ADD SOME LOGIC TO VERIFY CHANGING BY EMAIL"""
    user = await manager.update_password(user)
    if not user:
        raise HTTPException(status_code=404, detail='User does\'t exists')
    return user
