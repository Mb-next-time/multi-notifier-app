from datetime import datetime, timezone

from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from notifications.constants import NotificationStatus

from database import Base, default_datetime

class Notification(Base):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=default_datetime)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    status: Mapped[str] = mapped_column(String(32), default=NotificationStatus.ACTIVE.value)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=default_datetime,
        onupdate=default_datetime,
    )

    user: Mapped["User"] = relationship(back_populates="notifications")

    def __repr__(self) -> str:
        return f"Notification(id={self.id!r},title={self.title!r})"
