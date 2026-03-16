from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, current_datetime_utc
from notification_schedule.constants import NotificationScheduleStatus

class NotificationSchedule(Base):
    __tablename__ = "notification_schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"))
    notification_id: Mapped[int] = mapped_column(ForeignKey("notification.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=current_datetime_utc)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=current_datetime_utc,
        onupdate=current_datetime_utc
    )
    repeat_settings: Mapped[dict] = mapped_column(JSON)
    name: Mapped[str] = mapped_column(String(255))
    next_fire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(16), default=NotificationScheduleStatus.RUNNING.value)
