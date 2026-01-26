from datetime import datetime, timezone

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    ...

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    last_login: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    is_deleted: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f"User (id={self.id!r},username={self.username!r}>"
