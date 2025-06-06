from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base
from app.models import FitnessClass
from datetime import datetime, timedelta

client = TestClient(app)

# Setup DB before each test (manual approach)
def setup_module(module):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.add_all([
        FitnessClass(name="Yoga", date_time=datetime.now() + timedelta(days=1), instructor="Alice", available_slots=2),
        FitnessClass(name="Zumba", date_time=datetime.now() + timedelta(days=2), instructor="Bob", available_slots=1),
    ])
    db.commit()
    db.close()


def test_get_classes():
    response = client.get("/classes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2


def test_successful_booking():
    data = {
        "class_id": 1,
        "client_name": "Test User",
        "client_email": "test@example.com"
    }
    response = client.post("/book", json=data)
    assert response.status_code == 200
    assert response.json()["client_email"] == "test@example.com"


def test_overbooking():
    # Book once (should work)
    client.post("/book", json={
        "class_id": 2,
        "client_name": "First",
        "client_email": "first@example.com"
    })
    # Book again (should fail — slots were 1)
    response = client.post("/book", json={
        "class_id": 2,
        "client_name": "Second",
        "client_email": "second@example.com"
    })
    assert response.status_code == 400
    assert "No slots available" in response.text


def test_get_bookings_by_email():
    email = "fetchme@example.com"
    client.post("/book", json={
        "class_id": 1,
        "client_name": "Fetcher",
        "client_email": email
    })
    response = client.get("/bookings", params={"email": email})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["client_email"] == email


def test_booking_missing_fields():
    data = {
        "class_id": 1,
        "client_name": "Missing Email"
    }
    response = client.post("/book", json=data)
    assert response.status_code == 422


def test_booking_invalid_email():
    data = {
        "class_id": 1,
        "client_name": "Invalid Email",
        "client_email": "not-an-email"
    }
    response = client.post("/book", json=data)
    assert response.status_code == 422


def test_booking_invalid_class():
    data = {
        "class_id": 999,
        "client_name": "No Class",
        "client_email": "noclass@example.com"
    }
    response = client.post("/book", json=data)
    assert response.status_code == 404
