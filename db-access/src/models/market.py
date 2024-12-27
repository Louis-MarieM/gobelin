from config.orm import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import  DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

class Market(Base):
    __tablename__ = "markets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    region: Mapped[str] = mapped_column(String(40), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    source: Mapped[str] = mapped_column(String(40), nullable=True)
    added_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    prices: Mapped[List["Price"]] = relationship(back_populates="market")
