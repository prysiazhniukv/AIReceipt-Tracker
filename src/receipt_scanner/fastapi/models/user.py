from sqlalchemy import Boolean, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from receipt_scanner.fastapi.database import Base
from receipt import Receipt

class User(Base):
    __tablename__ = "users"

    id:   Mapped[int]     = mapped_column(primary_key=True)
    email:        Mapped[str]     = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_pass:  Mapped[str]     = mapped_column(String, nullable=False)
    is_active:    Mapped[bool]    = mapped_column(Boolean, default=True, nullable=False)
    created_at:   Mapped[DateTime] = mapped_column(DateTime(timezone=True),
                                                   server_default=func.now())

    # one‐to‐many → receipts “owned” by this user
    receipts: Mapped[list["Receipt"]] = relationship(
        "Receipt", back_populates="owner", cascade="all, delete-orphan"
    )

