import abc
import typing

from core.config import DATABASE_URL
from loguru import logger
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base, Booking

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncLocalSession = async_sessionmaker(engine)


class AsyncDataBaseCRUD(abc.ABC):
    @staticmethod
    async def add_booking(*args, **kwargs) -> typing.Any:
        pass

    @staticmethod
    async def get_all_bookings(*args, **kwargs) -> typing.Any:
        pass

    @staticmethod
    async def get_exact_booking(*args, **kwargs) -> typing.Any:
        pass

    @staticmethod
    async def remove_booking(*args, **kwargs) -> typing.Any:
        pass


def DataBaseInit() -> None:
    try:
        logger.info("Creating tables...")
        Base.metadata.create_all(engine.sync_engine)
        logger.info("Tables created")

    except Exception as e:
        logger.critical("Cant create tables", e)


@typing.final
class AsyncBookingCRUD(AsyncDataBaseCRUD):
    @staticmethod
    async def add_booking(session: AsyncSession) -> typing.Any:
        query = insert(Booking).values()
        await session.execute(query)
        await session.commit()

    @staticmethod
    async def get_all_bookings(session: AsyncSession) -> typing.Any:
        query = select(Booking)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_exact_booking(session: AsyncSession) -> typing.Any:
        pass

    @staticmethod
    async def remove_booking(session: AsyncSession) -> typing.Any:
        pass
