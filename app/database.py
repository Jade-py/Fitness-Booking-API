from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create, connect to and instantiate an SqlLite Database Instance
SQLALCHEMY_DATABASE_URL = "sqlite:///./classes.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine) # Creates a new database engine that is bound to the SqlLite engine
Base = declarative_base()
