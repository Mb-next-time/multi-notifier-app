from datetime import datetime, timezone

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import UniqueConstraint

from database import Base

class Channel(Base):
    __tablename__ = "channel"

    id: Mapped[int] = mapped_column(primary_key=True)
    # way of send notification ('email', 'sms' and etc)
    provider: Mapped[str] = mapped_column(String(255))
    # concrete email, phone number
    destination: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    is_verified: Mapped[bool] = mapped_column(default=False)

    __table_args__ = (
        UniqueConstraint('provider', 'destination', 'user_id', name='uq_channel_provider_destination_user_id'),
    )

    def __repr__(self) -> str:
        return f"Channel(id={self.id!r},provider={self.provider!r})"
