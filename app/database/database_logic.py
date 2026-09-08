import abc
import typing
from datetime import date, time

from core.config import DATABASE_URL
from loguru import logger
from schemas import BookingCreate
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base, Booking

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncLocalSession = async_sessionmaker(engine, expire_on_commit=False)


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


async def database_init() -> None:
    try:
        logger.info("Creating tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            #
            logger.info("Tables created")
            await conn.commit()
            await conn.close()

    except Exception as e:
        logger.critical(f"Cant create tables: {e}")


@typing.final
class AsyncBookingCRUD(AsyncDataBaseCRUD):
    @staticmethod
    async def add_booking(session: AsyncSession, data: BookingCreate) -> Booking:
        booking = Booking(**data.model_dump())
        session.add(booking)
        await session.commit()
        await session.refresh(booking)
        return booking

    @staticmethod
    async def get_all_bookings(session: AsyncSession, date: date | None = None) -> typing.Any:
        query = select(Booking)
        if date:
            query = query.where(Booking.booking_date == date)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_exact_booking(session: AsyncSession, booking_id: int) -> Booking | None:
        query = select(Booking).where(Booking.id == booking_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def remove_booking(session: AsyncSession, booking_id: int) -> typing.Any:
        query = (
            update(Booking)
            .where(Booking.id == booking_id)
            .values(status="cancelled")
            .returning(Booking)
        )

        result = await session.execute(query)
        await session.commit()
        return result.scalar_one_or_none()


async def count_guests(date: date, time: time, session: AsyncSession) -> int | None:
    query = select(func.sum(Booking.guests)).where(
        Booking.booking_date == date, Booking.booking_time == time, Booking.status == "active"
    )
    result = await session.execute(query)
    return result.scalar()
