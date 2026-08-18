from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

# Using a local sqlite database for simplicity, but this should be configurable
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./prost.db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
