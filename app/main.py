from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {
        "message": "🏋️‍♀️ Welcome to the Fitness Booking API!",
        "endpoints": {
            "GET /classes": "List all available classes",
            "POST /book": "Book a slot in a class",
            "GET /bookings?email=your_email": "View bookings by email"
        },
        "docs": "Visit /docs for interactive API documentation"
    }

@app.get("/classes", response_model=List[schemas.ClassOut])
def get_classes(db: Session = Depends(get_db)):
    return db.query(models.FitnessClass).all()


@app.post("/book", response_model=schemas.BookingOut)
def book_class(booking: schemas.BookingIn, db: Session = Depends(get_db)):
    fitness_class = db.query(models.FitnessClass).filter(models.FitnessClass.id == booking.class_id).first()
    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found")
    if fitness_class.available_slots <= 0:
        raise HTTPException(status_code=400, detail="No slots available")

    fitness_class.available_slots -= 1
    db_booking = models.Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


@app.get("/bookings", response_model=List[schemas.BookingOut])
def get_bookings(email: str = Query(...), db: Session = Depends(get_db)):
    return db.query(models.Booking).filter(models.Booking.client_email == email).all()
