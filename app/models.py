from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class FitnessClass(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date_time = Column(DateTime)
    instructor = Column(String)
    available_slots = Column(Integer)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer)
    client_name = Column(String)
    client_email = Column(String)
