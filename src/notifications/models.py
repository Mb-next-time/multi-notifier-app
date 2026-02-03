from datetime import datetime, timezone

from sqlalchemy import String, Text, JSON, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from notifications.constants import NotificationLiteral, RepeatInterval
from database import Base

class Notification(Base):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str | None] = mapped_column(String(255), default=None)
    body: Mapped[str | None] = mapped_column(Text(), default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    is_active: Mapped[bool] = mapped_column(default=True)
    repeat_interval = mapped_column(JSON(), default={
        NotificationLiteral.HOW_OFTEN: RepeatInterval.ONCE,
        NotificationLiteral.STEP: 0
    })
    startup_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="notifications")

    def __repr__(self) -> str:
        return f"Notification(id={self.id!r},title={self.title!r})"
