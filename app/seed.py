from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import FitnessClass

db = SessionLocal() # Create an instance of database

# Input sample data /Seed the classes table
classes = [
    FitnessClass(name="Yoga", date_time=datetime.now() + timedelta(days=1), instructor="Alice", available_slots=5),
    FitnessClass(name="Zumba", date_time=datetime.now() + timedelta(days=2), instructor="Bob", available_slots=8),
    FitnessClass(name="HIIT", date_time=datetime.now() + timedelta(days=3), instructor="Charlie", available_slots=10)
]

db.add_all(classes)
db.commit()
db.close()
