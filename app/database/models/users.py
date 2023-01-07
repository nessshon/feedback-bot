from __future__ import annotations

from sqlalchemy import (Column, Integer, BigInteger, String, DateTime, Boolean,
                        select, update, func)

from ..base import Base
from ..sessionmaker import async_sessionmaker


class UserModel(Base):
    __tablename__ = "users"

    pk = Column(
        Integer,
        primary_key=True,
    )
    id = Column(
        BigInteger,
        unique=True,
        nullable=False
    )
    name = Column(
        String(length=64),
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        default=func.now()
    )
    message_thread_id = Column(
        Integer,
        unique=True,
        nullable=True
    )
    forum_topic_closed = Column(
        Boolean,
        default=False,
        nullable=False
    )

    @classmethod
    async def add(cls, **kwargs) -> None:
        async with async_sessionmaker() as session:
            session.add(cls(**kwargs))
            await session.commit()

    @classmethod
    async def update(cls, user_id: str | int, **kwargs) -> None:
        async with async_sessionmaker() as session:
            await session.execute(
                update(cls)
                .where(cls.id == user_id).values(**kwargs)
            )
            await session.commit()

    @classmethod
    async def is_exists(cls, user_id: str | str) -> bool:
        async with async_sessionmaker() as session:
            query = await session.execute(
                select(cls.id)
                .where(cls.id == user_id)
            )
            return query.scalar() is not None

    @classmethod
    async def is_forum_topic_closed(cls, message_thread_id: int) -> bool:
        async with async_sessionmaker() as session:
            query = await session.execute(
                select(cls.forum_topic_closed)
                .where(cls.message_thread_id == message_thread_id)
            )
            return query.scalar()

    @classmethod
    async def get_user_id(cls, message_thread_id: int) -> int:
        async with async_sessionmaker() as session:
            query = await session.execute(
                select(cls.id)
                .where(cls.message_thread_id == message_thread_id)
            )
            return query.scalar()

    @classmethod
    async def get_message_thread_id(cls, user_id: str | int) -> int:
        async with async_sessionmaker() as session:
            query = await session.execute(
                select(cls.message_thread_id)
                .where(cls.id == user_id)
            )
            return query.scalar()
