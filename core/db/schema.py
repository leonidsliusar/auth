from enum import Enum
from uuid import uuid4

from sqlalchemy import Enum as EnumField
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase, AsyncAttrs):
    ...


class BotType(Enum):
    BROADCAST = 'B'
    CHAT = 'C'
    ANALYTIC = 'A'


class User(Base):
    """
    bot_type - user have bought access to some bot
    is_changed - user is in process of changing password
    """
    __tablename__ = 'user'

    id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    bot_type: Mapped[BotType] = mapped_column(EnumField(BotType), nullable=True)
    verify_code: Mapped[str] = mapped_column(nullable=True)
    in_changes: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f'{self.id} {self.email} {self.bot_type}'
