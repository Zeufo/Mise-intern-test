from collections.abc import AsyncGenerator
from datetime import date

from database import AsyncLocalSession
from fastapi import APIRouter, Depends, Query
from schemas import BookingCreate, BookingOut
from services import get_bookings_list
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import session

router = APIRouter()


async def get_session() -> AsyncGenerator:
    async with AsyncLocalSession() as session:
        yield session


@router.get(
    "/bookings",
    response_model=list[BookingOut],
    summary="Получить все брони",
    description="Возвращаеет все номера брони",
)
async def get_bookings(
    booking_date: date | None = Query(default=None, description="фильтр по дате"),
    session: AsyncSession = Depends(get_session),
):
    result = await get_bookings_list(session, booking_date)
    return result


@router.post("/bookings")
async def create_booking(
    data: BookingCreate, session: AsyncSession = Depends(get_session), date=None
):
    pass


@router.get("/bookings/{booking_id}")
async def get_booking(booking_id):
    pass


@router.delete("/bookings/{booking_id}")
async def delete_booking(booking_id):
    pass
