from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence

from notifications import schemas, models
from notifications.constants import NotificationStatus
from notifications.exceptions import NotificationNotFound
from notifications.schemas import FilterNotification
from auth.models import User


class NotificationService:

    def __init__(self, database_session: AsyncSession, user: User):
        self.database_session = database_session
        self.user = user

    async def _get_owned_notification(self, notification_id: int) -> models.Notification:
        notification = (await self.database_session.execute(
            select(models.Notification).where(
                models.Notification.id == notification_id,
                models.Notification.user_id == self.user.id,
                models.Notification.status != NotificationStatus.DELETED.value,
            )
        )).scalar_one_or_none()
        if not notification:
            raise NotificationNotFound
        return notification

    async def create(self, body_notification: schemas.BodyNotification) -> models.Notification:
        notification = models.Notification(user_id=self.user.id, **body_notification.model_dump())
        self.database_session.add(notification)
        await self.database_session.flush()
        return notification

    async def get_list(self, filter_notification: FilterNotification) -> Sequence[models.Notification]:
        page_limit = filter_notification.limit
        offset = (filter_notification.page - 1) * page_limit
        notifications = (await self.database_session.execute(
            select(models.Notification).where(
                models.Notification.user_id == self.user.id,
                models.Notification.status != NotificationStatus.DELETED.value,
            ).order_by(models.Notification.created_at.desc()).offset(offset).limit(page_limit)
        )).scalars().all()
        return notifications

    async def get(self, notification_id: int) -> models.Notification:
        return await self._get_owned_notification(notification_id)

    async def update(self, notification_id: int, body_notification: schemas.UpdateNotification) -> models.Notification:
        notification = await self._get_owned_notification(notification_id)
        for field, value in body_notification.model_dump(exclude_unset=True).items():
            setattr(notification, field, value)
        await self.database_session.flush()
        return notification

    async def delete(self, notification_id: int) -> None:
        notification = await self._get_owned_notification(notification_id)
        await self.database_session.delete(notification)
        await self.database_session.flush()
