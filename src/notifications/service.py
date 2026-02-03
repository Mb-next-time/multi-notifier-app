from sqlalchemy.orm import Session
from sqlalchemy import select, Sequence

from notifications import schemas, models
from notifications.exceptions import NotificationNotFound
from notifications.constants import DEFAULT_PAGE_LIMIT, DEFAULT_NUMBER_PAGE

from auth.models import User

class NotificationService:

    def __init__(self, database_session: Session, user: User):
        self.database_session = database_session
        self.user = user

    def _get_owned_notification(self, notification_id: int) -> models.Notification:
        notification = self.database_session.execute(
            select(models.Notification).where(
                models.Notification.id == notification_id,
                models.Notification.user_id == self.user.id,
                models.Notification.is_active == True,
            )
        ).scalar_one_or_none()
        if not notification:
            raise NotificationNotFound
        return notification

    def create(self, body_notification: schemas.BodyNotification) -> models.Notification:
        notification = models.Notification(user_id=self.user.id, **body_notification.model_dump())
        self.database_session.add(notification)
        self.database_session.flush()
        return notification

    def get_list(self, page: int = DEFAULT_NUMBER_PAGE, limit: int = DEFAULT_PAGE_LIMIT) -> Sequence[models.Notification]:
        offset = (page - 1) * limit
        notifications = self.database_session.execute(
            select(models.Notification).where(
                models.Notification.user_id == self.user.id,
                models.Notification.is_active == True,
            ).order_by(models.Notification.created_at.desc()).offset(offset).limit(limit)
        ).scalars().all()
        return notifications

    def get(self, notification_id: int) -> models.Notification:
        return self._get_owned_notification(notification_id)

    def update(self, notification_id: int, body_notification: schemas.UpdateNotification) -> models.Notification:
        notification = self._get_owned_notification(notification_id)
        for field, value in body_notification.model_dump(exclude_unset=True).items():
            setattr(notification, field, value)
        self.database_session.flush()
        return notification

    def delete(self, notification_id: int) -> None:
        notification = self._get_owned_notification(notification_id)
        self.database_session.delete(notification)
        self.database_session.flush()