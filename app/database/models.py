from datetime import date, datetime, time

from sqlalchemy import Date, DateTime, Integer, String, Time, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# DeclarativeBase in Alchemy 2.0+ is abc class, so we cant use it directly
class Base(DeclarativeBase):
    pass


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    booking_date: Mapped[date] = mapped_column(Date, nullable=False)
    booking_time: Mapped[time] = mapped_column(Time, nullable=False)
    guests: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
