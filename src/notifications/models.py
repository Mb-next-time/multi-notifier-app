from datetime import datetime

from sqlalchemy import String, Text, DateTime, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from notifications.constants import NotificationLiteral, RepeatInterval


class Base(DeclarativeBase):
    ...

class Notification(Base):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), default=None, nullable=True)
    body: Mapped[str] = mapped_column(Text(), default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())
    is_active: Mapped[bool] = mapped_column(default=True)
    repeat_interval = mapped_column(JSON(), default={
        NotificationLiteral.HOW_OFTEN: RepeatInterval.ONCE,
        NotificationLiteral.STEP: 0
    })

    def __repr__(self) -> str:
        return f"Notification(id={self.id!r},title={self.title!r})"
