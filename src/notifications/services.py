from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy import select, Sequence, ScalarResult

from notifications import schemas, models


class NotificationService:

    def __init__(self, database: Session):
        self.database = database

    def create(self, body_notification: schemas.BodyNotification) -> models.Notification:
        notification = models.Notification(**body_notification.model_dump())
        self.database.add(notification)
        self.database.commit()
        return notification

    def get_list(self) -> Sequence[models.Notification]:
        notifications = self.database.execute(select(models.Notification)).scalars().all()
        return notifications

    def get_by_id(self, notification_id: int) -> models.Notification:
        notification = self.database.execute(select(models.Notification).filter_by(id=notification_id)).scalar_one_or_none()
        if not notification:
            raise NoResultFound
        return notification

    def update(self, notification_id: int, body_notification: schemas.UpdateNotification) -> models.Notification:
        notification = self.database.execute(select(models.Notification).filter_by(id=notification_id)).scalar_one_or_none()
        if not notification:
            raise NoResultFound
        for field, value in body_notification.model_dump(exclude_unset=True).items():
            setattr(notification, field, value)
        self.database.commit()
        return notification

    def delete(self, notification_id: int) -> None:
        notification = self.database.execute(select(models.Notification).filter_by(id=notification_id)).scalar_one_or_none()
        if not notification:
            raise NoResultFound
        self.database.delete(notification)
        self.database.commit()