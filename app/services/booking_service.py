import typing
from datetime import date

from database import AsyncBookingCRUD
from schemas import BookingOut
from sqlalchemy.ext.asyncio import AsyncSession


async def is_free_slots(guests: int) -> bool:
    return True


async def create_booking(guests: int):
    can_book = await is_free_slots(guests)

    if can_book:
        pass
        # await AsyncBookingCRUD.add_booking()


async def get_bookings_list(
    session: AsyncSession, target_id: date | None = None
) -> list[BookingOut]:
    result = await AsyncBookingCRUD.get_all_bookings(session)
    return result
