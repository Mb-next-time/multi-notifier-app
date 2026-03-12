from datetime import datetime, timezone

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, current_datetime_utc

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=current_datetime_utc)
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=current_datetime_utc)
    is_deleted: Mapped[bool] = mapped_column(default=False)

    notifications: Mapped[list["Notification"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User (id={self.id!r},username={self.username!r}>"
