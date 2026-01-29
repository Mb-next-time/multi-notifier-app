from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from auth.dependencies import get_current_authenticated_user
from auth.models import User
from database import get_db
from notifications.service import NotificationService


def get_notification_service(
    database_session: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_authenticated_user)]
) -> NotificationService:
    return NotificationService(database_session, user)