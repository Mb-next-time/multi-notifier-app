from datetime import datetime, timezone

from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class NotificationSchedule(Base):
    __tablename__ = "notification_schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"))
    notification_id: Mapped[int] = mapped_column(ForeignKey("notification.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )
    repeat_settings: Mapped[dict] = mapped_column(JSON)
    name: Mapped[str] = mapped_column(String(255))
    fire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

