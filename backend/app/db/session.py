from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Using SQLite for easier local development
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# For SQLite, we need connect_args={"check_same_thread": False}
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
