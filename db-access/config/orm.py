from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

# Base class for defining ORM models.
class Base(DeclarativeBase):
    pass

# Load the database connection URL from environment variables.
DATABASE_URL = os.getenv("DATABASE_URL_SQLALCHEMY")

# Create the SQLAlchemy motor.
POOL_SIZE = int(os.getenv("POOL_SIZE"))
MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW"))
POOL_TIMEOUT = int(os.getenv("POOL_TIMEOUT"))
POOL_RECYCLE = int(os.getenv("POOL_RECYCLE"))

engine = create_engine(
    DATABASE_URL, 
    future=True,  # Enables SQLAlchemy's 2.0 style usage.
    pool_size=POOL_SIZE,   # Controls number of connections to maintain in the pool.
    max_overflow=MAX_OVERFLOW,  # Number of maximum connections allowed beyond the pool size.
    pool_timeout=POOL_TIMEOUT,  # Timeout before failing to acquire a connection.
    pool_recycle=POOL_RECYCLE  # Recycles connections after this many seconds.
)

# Create a session factory for managing database sessions.
session_local = sessionmaker(
    autocommit=False,  # Transactions are explicitly committed
    autoflush=False,  # Avoid automatic flushing of change
    bind=engine  # Bind the session to the created engine
)
