import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base
from app.models import FitnessClass
from datetime import datetime, timedelta

# Reset DB before each test (if needed)
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    db.add_all([
        FitnessClass(name="Yoga", date_time=datetime.now() + timedelta(days=1), instructor="Alice", available_slots=2),
        FitnessClass(name="Zumba", date_time=datetime.now() + timedelta(days=2), instructor="Bob", available_slots=1),
    ])
    db.commit()
    db.close()


@pytest.mark.anyio
async def test_get_classes():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/classes")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.anyio
async def test_successful_booking():
    booking_data = {
        "class_id": 1,
        "client_name": "Test User",
        "client_email": "test@example.com"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/book", json=booking_data)
    assert response.status_code == 200
    assert response.json()["client_email"] == "test@example.com"


@pytest.mark.anyio
async def test_overbooking_fails():
    booking_data = {
        "class_id": 2,
        "client_name": "First",
        "client_email": "first@example.com"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First booking should succeed
        await ac.post("/book", json=booking_data)
        # Second booking should fail (slots = 1)
        response = await ac.post("/book", json=booking_data)
    assert response.status_code == 400
    assert "No slots available" in response.text


@pytest.mark.anyio
async def test_get_bookings_by_email():
    booking_data = {
        "class_id": 1,
        "client_name": "Someone",
        "client_email": "booker@example.com"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/book", json=booking_data)
        response = await ac.get("/bookings", params={"email": "booker@example.com"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["client_email"] == "booker@example.com"
