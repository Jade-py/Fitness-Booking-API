from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# Creating schemas for serialization and validation of stored data
class ClassOut(BaseModel):
    id: int
    name: str
    date_time: datetime
    instructor: str
    available_slots: int
    model_config = ConfigDict(from_attributes=True)

class BookingIn(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

class BookingOut(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr
    model_config = ConfigDict(from_attributes=True)
