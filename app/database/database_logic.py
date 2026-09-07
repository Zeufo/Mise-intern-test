import abc
import typing

from config import DATABASE_URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

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


class AsyncBookingCRUD(AsyncDataBaseCRUD):
    @staticmethod
    async def add_booking(session: AsyncSession) -> typing.Any:
        pass

    @staticmethod
    async def get_all_bookings(session: AsyncSession) -> typing.Any:
        pass

    @staticmethod
    async def get_exact_booking(session: AsyncSession) -> typing.Any:
        pass

    @staticmethod
    async def remove_booking(session: AsyncSession) -> typing.Any:
        pass
