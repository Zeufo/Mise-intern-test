import typing
from datetime import date

from core.config import MAX_CAPACITY_PER_SLOT
from database import AsyncBookingCRUD, count_guests
from database.models import Booking
from fastapi import HTTPException
from schemas import BookingCreate, BookingOut
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import session


async def is_free_slots(data: BookingCreate, session: AsyncSession) -> bool:
    guests_count = await count_guests(data.booking_date, data.booking_time, session) or 0
    return guests_count + data.guests <= MAX_CAPACITY_PER_SLOT


async def create_booking_service(data: BookingCreate, session: AsyncSession) -> Booking:
    can_book = await is_free_slots(data, session)
    if not can_book:
        raise HTTPException(status_code=409, detail="Все места заняты")
    return await AsyncBookingCRUD.add_booking(session, data)


async def get_bookings_list_service(
    session: AsyncSession, target_id: date | None = None
) -> list[BookingOut]:
    result = await AsyncBookingCRUD.get_all_bookings(session, target_id)
    return result


async def get_booking_by_id_service(session: AsyncSession, booking_id: int) -> Booking:
    booking = await AsyncBookingCRUD.get_exact_booking(session, booking_id)

    if not booking:
        raise HTTPException(status_code=404, detail="Бронь не найдена")

    return booking


async def delete_booking_service(session: AsyncSession, booking_id: int) -> Booking:
    booking = await AsyncBookingCRUD.remove_booking(session, booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Бронь не найдена")
    else:
        return booking
