from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  sessionmaker, declarative_base

# Create a Database
SQLALCHEMY_DATABASE_URL = "sqlite:///database/sql.db"

db = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)
Base = declarative_base()
