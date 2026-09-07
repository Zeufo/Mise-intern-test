import abc
import typing

from core.config import DATABASE_URL
from loguru import logger
from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import query

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


def database_init() -> None:
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
    async def get_all_bookings(session: AsyncSession, date: str | None = None) -> typing.Any:
        query = select(Booking)
        if date:
            query = query.where(Booking.booking_date == date)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_exact_booking(session: AsyncSession) -> typing.Any:
        pass

    @staticmethod
    async def remove_booking(session: AsyncSession) -> typing.Any:
        pass


async def count_guests() -> int | None:
    query = select(func.sum(Booking.guests)).where(
        Booking.booking_date == Booking.status == "active"
    )
    async with AsyncLocalSession() as session:
        pass
