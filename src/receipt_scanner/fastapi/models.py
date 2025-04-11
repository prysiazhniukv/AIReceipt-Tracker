from receipt_scanner.fastapi.database import Base
from sqlalchemy import String, DateTime, func, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from typing import List

class ReceiptItem(Base):
    __tablename__ = "receipt_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    receipt_id: Mapped[int] = mapped_column(ForeignKey("receipts.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String)
    quantity: Mapped[int]
    unit_price: Mapped[float] = mapped_column(Numeric)



class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(primary_key=True)
    photo_url: Mapped[str] = mapped_column(String)
    time_stamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    store_name: Mapped[str] = mapped_column(String(30), nullable=True)
    items: Mapped[List["ReceiptItem"]] = relationship(
        backref="receipt",
        cascade="all, delete-orphan"
    )
    total_price: Mapped[float] = mapped_column(Numeric, nullable=True)



