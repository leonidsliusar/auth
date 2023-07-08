from typing import AsyncGenerator
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from core.settings import settings

engine = create_async_engine(settings.DB, echo=True)
async_session = async_sessionmaker(engine=engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator:
    session = async_session()
    try:
        yield session
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail='User already exists')
    finally:
        await session.close()
