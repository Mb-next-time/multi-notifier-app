from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from notifications import schemas
from notifications.constants import NotificationLiteral, RepeatInterval, NotificationSchemeFields
from notifications.dependencies import get_notification_service
from src.main import app
from notifications.models import Notification


class FakeNotificationService:

    def get_list(self):
        return [
            Notification(id=1, repeat_interval={
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.ONCE.value,
                NotificationLiteral.STEP.value: 0,
            }),
            Notification(id=2, repeat_interval={
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.HOURLY.value,
                NotificationLiteral.STEP.value: 2,
            }),
            Notification(id=3, repeat_interval={
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.MONTHLY.value,
                NotificationLiteral.STEP.value: 1,
            })
        ]

    def create(self, body_notification: schemas.BodyNotification) -> Notification:
        return Notification(id=5, **body_notification.model_dump())

    def get_by_id(self, notification_id: int) -> Notification:
        return Notification(id=notification_id, repeat_interval={
            NotificationLiteral.HOW_OFTEN.value: RepeatInterval.ONCE.value,
            NotificationLiteral.STEP.value: 0,
        })

    def update(self, notification_id: int, body_notification: schemas.UpdateNotification) -> Notification:
        notification = self.get_by_id(notification_id)
        for field, value in body_notification.model_dump(exclude_unset=True).items():
            setattr(notification, field, value)
        return notification

    def delete(self, notification_id: int) -> None:
        return

@pytest.fixture
def body_notification():
    return {
        NotificationSchemeFields.TITLE.value: "title-1",
        NotificationSchemeFields.BODY.value: "body-1",
        NotificationSchemeFields.REPEAT_INTERVAL.value: {
            NotificationLiteral.HOW_OFTEN.value: RepeatInterval.ONCE.value,
            NotificationLiteral.STEP.value: 0,
        }
    }

@pytest.fixture
def client():
    app.dependency_overrides[get_notification_service] = lambda: FakeNotificationService()
    return TestClient(app)

@pytest.fixture
def client_factory_with_raised_exception():
    def _create(method: str, exception: Exception):
        mock = Mock()
        setattr(mock, method, Mock(side_effect=exception))
        app.dependency_overrides[get_notification_service] = lambda: mock
        return TestClient(app)
    return _create
