import re
from datetime import date, time, timedelta

from pydantic import BaseModel, Field, field_validator

PHONE_PATTERN = re.compile(r"^(\+7|8)\d{10}$")
NAME_PATTERN = re.compile(r"^[A-Za-zА-Яа-яЁё\s-]+$")


class BookingCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    phone: str = Field(min_length=10, max_length=15)
    booking_date: date
    booking_time: time
    guests: int = Field(ge=1, le=12)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not NAME_PATTERN.fullmatch(v):
            raise ValueError("Имя может содержать только буквы, пробелы и дефис")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not PHONE_PATTERN.fullmatch(v):
            raise ValueError("Телефон должен быть в формате +7XX... или 8XX...")
        return v

    @field_validator("booking_date")
    @classmethod
    def validate_date(cls, v: date) -> date:
        today = date.today()
        if v < today:
            raise ValueError("Дата бронирования не может быть раньше сегодняшнего дня")
        if v > today + timedelta(days=90):
            raise ValueError("Дата бронирования не может быть позже, чем через 90 дней")
        return v

    @field_validator("booking_time")
    @classmethod
    def validate_booking_time(cls, v: time) -> time:
        if v.minute != 0 or v.second != 0 or not (12 <= v.hour <= 22):
            raise ValueError(
                "Допустимы только слоты с 12:00 до 22:00 с шагом в 1 час (12:00, 13:00, ..., 22:00)"
            )
        return v


class BookingOut(BookingCreate):
    id: int
    status: str
