from datetime import datetime

from sqlalchemy import DateTime, String, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, default_datetime

class NotificationDelivery(Base):
    __tablename__ = "notification_delivery"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel: Mapped[dict] = mapped_column(JSON)
    notification: Mapped[dict] = mapped_column(JSON)
    notification_schedule_id: Mapped[int] = mapped_column()
    delivered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=default_datetime)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=default_datetime)
    error_message: Mapped[str | None] = mapped_column(String(255))
    next_fire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(16))
    current_attempt: Mapped[int] = mapped_column(default=1)
    max_attempts: Mapped[int] = mapped_column(default=5)

    __table_args__ = (
        UniqueConstraint('notification_schedule_id', 'next_fire_at', name='uq_notification_delivery_notification_schedule_id_next_fire_at'),
    )