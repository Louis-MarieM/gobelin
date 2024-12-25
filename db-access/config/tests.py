import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, sessionmaker
from sqlalchemy import Integer, String, ForeignKey
from src.daos.base_dao import BaseDAO

class Base(DeclarativeBase):
    pass

# Fictional model
class TestModel(Base):
    __test__ = False  # To warn the PytestCollectionWarning
    __tablename__ = "test_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

# SQLite RAM configuration
@pytest.fixture
def db_session():
    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
