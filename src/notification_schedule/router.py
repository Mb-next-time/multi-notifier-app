from typing import Annotated

from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_authenticated_user
from auth.models import User
from notification_schedule.constants import NotificationScheduleLiteral
from notification_schedule.models import NotificationSchedule
from notification_schedule.schemas import ResponseNotificationSchedule, BodyNotificationSchedule
from notifications.dependencies import get_notification_service
from notifications.models import Notification
from notifications.service import NotificationService
from channels.models import Channel
from database import get_database_session


notification_schedule_router = APIRouter(prefix=f"/{NotificationScheduleLiteral.URL.value}", tags=[NotificationScheduleLiteral.TAGS])

@notification_schedule_router.get(
    path="/",
    response_model=list[ResponseNotificationSchedule]
)
async def list_notification_schedules(
    database_session: Annotated[AsyncSession,Depends(get_database_session)],
    user: Annotated[User, Depends(get_current_authenticated_user)]
):
    notification_schedules = (await database_session.execute(
        select(NotificationSchedule).join(
            Notification, Notification.id == NotificationSchedule.notification_id).where(Notification.user_id == user.id))).scalars().all()
    return notification_schedules

@notification_schedule_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseNotificationSchedule
)
async def create_notification_schedules(
    body_notification_schedule: BodyNotificationSchedule,
    database_session: Annotated[AsyncSession, Depends(get_database_session)],
    user: Annotated[User, Depends(get_current_authenticated_user)],
    notification_service: Annotated[NotificationService, Depends(get_notification_service)]
):
    # check ownership of the notification
    await notification_service.get(body_notification_schedule.notification_id)
    channel = (await database_session.execute(select(Channel).where(
        Channel.id == body_notification_schedule.channel_id,
        Channel.user_id == user.id,
    ))).scalar_one_or_none()

    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Channel with id {body_notification_schedule.channel_id} not found"
        )

    new_notification_schedule = NotificationSchedule(**body_notification_schedule.model_dump())
    database_session.add(new_notification_schedule)
    await database_session.flush()

    return new_notification_schedule
