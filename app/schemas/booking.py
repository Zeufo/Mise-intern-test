from datetime import date, time

from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    phone: str = Field(min_length=10, max_length=15)
    booking_date: date
    booking_time: time
    guests: int = Field(ge=1, le=12)


class BookingOut(BookingCreate):
    id: int
    status: str
