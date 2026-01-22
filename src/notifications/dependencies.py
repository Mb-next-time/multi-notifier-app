from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from notifications.services import NotificationService


def get_notification_service(database: Annotated[Session, Depends(get_db)],) -> NotificationService:
    return NotificationService(database)