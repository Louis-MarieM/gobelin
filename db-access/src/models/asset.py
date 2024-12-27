from config.orm import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(20), nullable=False)
    added_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    prices: Mapped[List["Price"]] = relationship(back_populates="asset")
