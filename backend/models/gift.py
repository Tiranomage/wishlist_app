from sqlalchemy import String, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from db import Base


class Gift(Base):
	__tablename__ = "gifts"

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	wishlist_id: Mapped[int] = mapped_column(ForeignKey("wishlists.id", ondelete="CASCADE"), index=True, nullable=False)
	name: Mapped[str] = mapped_column(String(100), nullable=False)
	price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
	image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
	purchase_link: Mapped[str | None] = mapped_column(Text, nullable=True)
	status: Mapped[str] = mapped_column(String(32), default="Свободен", nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

	wishlist: Mapped["Wishlist"] = relationship(back_populates="gifts")


