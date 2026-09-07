from datetime import date, timedelta

import pytest
from core.config import MAX_CAPACITY_PER_SLOT

pytestmark = pytest.mark.asyncio

TOMORROW = (date.today() + timedelta(days=1)).isoformat()


def make_payload(**overrides):
    payload = {
        "name": "Иван Иванов",
        "phone": "+79991234567",
        "booking_date": TOMORROW,
        "booking_time": "18:00:00",
        "guests": 2,
    }
    payload.update(overrides)
    return payload


# ---------- CREATE ----------


async def test_create_booking_success(client):
    response = await client.post("/bookings", json=make_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "active"
    assert data["name"] == "Иван Иванов"
    assert "id" in data


async def test_create_booking_invalid_phone(client):
    response = await client.post("/bookings", json=make_payload(phone="123456"))
    assert response.status_code == 422


async def test_create_booking_invalid_name(client):
    response = await client.post("/bookings", json=make_payload(name="Ivan123"))
    assert response.status_code == 422


async def test_create_booking_date_in_past(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    response = await client.post("/bookings", json=make_payload(booking_date=yesterday))
    assert response.status_code == 422


async def test_create_booking_date_too_far(client):
    far_date = (date.today() + timedelta(days=91)).isoformat()
    response = await client.post("/bookings", json=make_payload(booking_date=far_date))
    assert response.status_code == 422


async def test_create_booking_invalid_time_slot(client):
    response = await client.post("/bookings", json=make_payload(booking_time="18:30:00"))
    assert response.status_code == 422


async def test_create_booking_invalid_guests_count(client):
    response = await client.post("/bookings", json=make_payload(guests=13))
    assert response.status_code == 422


async def test_create_booking_slot_full_returns_409(client):
    for _ in range(MAX_CAPACITY_PER_SLOT):
        response = await client.post(
            "/bookings", json=make_payload(guests=1, booking_time="19:00:00")
        )
        assert response.status_code == 201

    response = await client.post("/bookings", json=make_payload(guests=1, booking_time="19:00:00"))
    assert response.status_code == 409


# ---------- LIST ----------


async def test_get_bookings_list(client):
    await client.post("/bookings", json=make_payload())
    await client.post("/bookings", json=make_payload(booking_time="20:00:00"))

    response = await client.get("/bookings")

    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_bookings_filtered_by_date(client):
    other_date = (date.today() + timedelta(days=2)).isoformat()
    await client.post("/bookings", json=make_payload())
    await client.post("/bookings", json=make_payload(booking_date=other_date))

    response = await client.get("/bookings", params={"booking_date": TOMORROW})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["booking_date"] == TOMORROW


# ---------- GET BY ID ----------


async def test_get_booking_by_id_success(client):
    create_resp = await client.post("/bookings", json=make_payload())
    booking_id = create_resp.json()["id"]

    response = await client.get(f"/bookings/{booking_id}")

    assert response.status_code == 200
    assert response.json()["id"] == booking_id


async def test_get_booking_by_id_not_found(client):
    response = await client.get("/bookings/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Бронь не найдена"


# ---------- DELETE ----------


async def test_delete_booking_success(client):
    create_resp = await client.post("/bookings", json=make_payload())
    booking_id = create_resp.json()["id"]

    response = await client.delete(f"/bookings/{booking_id}")

    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"


async def test_delete_booking_not_found(client):
    response = await client.delete("/bookings/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Бронь не найдена"
