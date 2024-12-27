from config.orm import Base
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, sessionmaker
from sqlalchemy import Integer, String, ForeignKey
import sqlite3
from src.daos.base_dao import BaseDAO

class TestModel(Base):
    """
    Fictional model.
    """
    __test__ = False  # To warn the PytestCollectionWarning.
    __tablename__ = "test_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

@pytest.fixture
def db_session():
    """
    SQLite RAM configuration.
    """
    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Activates foreign key constraints for SQLite.
    """
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()