# Infrastructure layer — database connection.
#
# Replicate the same structure as user-service/app/database.py.
# The only difference: the default DATABASE_URL points to games.db.
#
# This file should provide:
# - engine         — SQLAlchemy engine built from DATABASE_URL
# - SessionLocal   — session factory bound to the engine
# - Base           — DeclarativeBase that all ORM models inherit from
# - get_db()       — FastAPI dependency: yields a session, closes it after the request
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./games.db")

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()