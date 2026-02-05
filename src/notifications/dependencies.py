from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_authenticated_user
from auth.models import User
from database import get_database_session
from notifications.service import NotificationService


async def get_notification_service(
    database_session: Annotated[AsyncSession, Depends(get_database_session)],
    user: Annotated[User, Depends(get_current_authenticated_user)]
) -> NotificationService:
    return NotificationService(database_session, user)