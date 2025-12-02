from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from db import Base


class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=False)
	password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

	wishlists: Mapped[list["Wishlist"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


