from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy motor creation
engine = create_engine(DATABASE_URL, pool_size=5, pool_size=10, pool_timeout=30, pool_recycle=3600)

# Session factory creation
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
