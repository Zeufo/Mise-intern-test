from collections.abc import AsyncGenerator
from datetime import date

from database import AsyncLocalSession
from fastapi import APIRouter, Depends, Query, status
from schemas import BookingCreate, BookingOut
from services import (
    create_booking_service,
    delete_booking_service,
    get_booking_by_id_service,
    get_bookings_list_service,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


async def get_session() -> AsyncGenerator:
    async with AsyncLocalSession() as session:
        yield session


@router.get(
    "/bookings",
    response_model=list[BookingOut],
    summary="Получить все брони",
)
async def get_bookings(
    booking_date: date | None = Query(default=None, description="фильтр по дате"),
    session: AsyncSession = Depends(get_session),
):
    return await get_bookings_list_service(session, booking_date)


@router.post(
    "/bookings",
    response_model=BookingOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать бронь",
)
async def create_booking(data: BookingCreate, session: AsyncSession = Depends(get_session)):
    return await create_booking_service(data, session)


@router.get("/bookings/{booking_id}", response_model=BookingOut, summary="Получить бронь по id")
async def get_booking(booking_id: int, session: AsyncSession = Depends(get_session)):
    return await get_booking_by_id_service(session, booking_id)


@router.delete("/bookings/{booking_id}", response_model=BookingOut, summary="Отменить бронь")
async def delete_booking(booking_id: int, session: AsyncSession = Depends(get_session)):
    return await delete_booking_service(session, booking_id)
