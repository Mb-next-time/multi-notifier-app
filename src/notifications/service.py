import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update

from notifications import schemas, models
from notifications.constants import NotificationLiteral


class NotificationService:

    def __init__(self, database: Session):
        self.database = database

    def create(self, body_notification: schemas.BodyNotification) -> schemas.Notification:
        notification = models.Notification(**body_notification.model_dump(mode="json"))
        self.database.add(notification)
        self.database.commit()

        return schemas.Notification(
            id=notification.id,
            title=notification.title,
            body=notification.body,
            repeat_interval=notification.repeat_interval
        )

    def get_list(self):
        statement = select(models.Notification)
        notifications = self.database.scalars(statement).all()
        return notifications

    def get_by_id(self, notification_id: int) -> models.Notification:
        statement = select(models.Notification).where(models.Notification.id == notification_id)
        notification = self.database.execute(statement).scalars().first()
        if not notification:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return notification

    def update(self, notification_id: int, body_notification: schemas.BodyNotification) -> schemas.Notification:
        statement = update(models.Notification).values(
            title=body_notification.title,
            body=body_notification.body,
            repeat_interval=body_notification.repeat_interval.model_dump_json()
        ).where(models.Notification.id == notification_id)
        self.database.execute(statement)
        self.database.commit()
        notification = self.get_by_id(notification_id)
        repeat_interval_json = json.JSONDecoder().decode(notification.repeat_interval)

        return schemas.Notification(
            id=notification.id,
            title=notification.title,
            body=notification.body,
            repeat_interval=schemas.RepeatInterval(
                how_often=repeat_interval_json[NotificationLiteral.HOW_OFTEN.value],
                step=repeat_interval_json[NotificationLiteral.STEP.value]
            )
        )

    def delete(self, notification_id: int) -> None:
        statement = delete(models.Notification).where(models.Notification.id == notification_id)
        self.database.execute(statement)
        self.database.commit()