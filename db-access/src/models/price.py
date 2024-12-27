from config.orm import Base
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("assets.id", ondelete="RESTRICT"), nullable=False)
    asset: Mapped["Asset"] = relationship(back_populates="prices")
    market_id: Mapped[int] = mapped_column(Integer, ForeignKey("markets.id", ondelete="RESTRICT"), nullable=False)
    market: Mapped["Market"] = relationship(back_populates="prices")
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    interval: Mapped[str] = mapped_column(String(5), nullable=False)
    open_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    close_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    high_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    low_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    volume: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False)
