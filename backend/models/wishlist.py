from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from db import Base


class Wishlist(Base):
	__tablename__ = "wishlists"

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
	title: Mapped[str] = mapped_column(String(100), nullable=False)
	description: Mapped[str | None] = mapped_column(Text, nullable=True)
	is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
	share_token: Mapped[str | None] = mapped_column(String(5), nullable=True, unique=True, index=True)
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

	owner: Mapped["User"] = relationship(back_populates="wishlists")
	gifts: Mapped[list["Gift"]] = relationship(back_populates="wishlist", cascade="all, delete-orphan")


