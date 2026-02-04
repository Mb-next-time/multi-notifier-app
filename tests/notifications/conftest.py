from datetime import datetime, timezone, timedelta
from contextlib import contextmanager
from typing import Annotated
from unittest.mock import Mock

import pytest
from fastapi import Depends
from sqlalchemy.exc import DatabaseError, DBAPIError

from auth.dependencies import get_current_authenticated_user
from auth.models import User
from notifications import schemas
from notifications.constants import NotificationLiteral, RepeatInterval, NotificationSchemeFields
from notifications.dependencies import get_notification_service
from notifications.schemas import FilterNotification
from notifications.models import Notification
from main import app
from tests import TestClientBuilder

datetime_in_future = datetime.now(tz=timezone.utc) + timedelta(minutes=60)
VALID_FORMAT_TIMESTAMP_OFFSET_ZONE: str = datetime_in_future.isoformat()
VALID_FORMAT_TIMESTAMP_Z_ZONE: str = VALID_FORMAT_TIMESTAMP_OFFSET_ZONE.replace("+00:00", "Z")
INVALID_FORMAT_TIMESTAMP = "2026-01-29T13:AD:00Z"

class FakeNotificationService:

    def get_list(self, filter_notification: FilterNotification):
        return [
            Notification(id=1, repeat_interval={
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.ONCE.value,
                NotificationLiteral.STEP.value: 0,
            }, startup_at=datetime_in_future),
            Notification(id=2, repeat_interval={
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.HOURLY.value,
                NotificationLiteral.STEP.value: 2,
            }, startup_at=datetime_in_future),
            Notification(id=3, repeat_interval={
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.MONTHLY.value,
                NotificationLiteral.STEP.value: 1,
            }, startup_at=datetime_in_future),
        ]

    def create(self, body_notification: schemas.BodyNotification) -> Notification:
        return Notification(id=5, **body_notification.model_dump())

    def get(self, notification_id: int) -> Notification:
        return Notification(id=notification_id, repeat_interval={
            NotificationLiteral.HOW_OFTEN.value: RepeatInterval.ONCE.value,
            NotificationLiteral.STEP.value: 0,
        }, startup_at=datetime_in_future)

    def update(self, notification_id: int, body_notification: schemas.UpdateNotification) -> Notification:
        notification = self.get(notification_id)
        for field, value in body_notification.model_dump(exclude_unset=True).items():
            setattr(notification, field, value)
        return notification

    def delete(self, notification_id: int) -> None:
        return

@pytest.fixture
def valid_json_body_notification():
    return {
        NotificationSchemeFields.TITLE.value: "title-1",
        NotificationSchemeFields.BODY.value: "body-1",
        NotificationSchemeFields.REPEAT_INTERVAL.value: {
            NotificationLiteral.HOW_OFTEN.value: RepeatInterval.ONCE.value,
            NotificationLiteral.STEP.value: 0,
        },
        NotificationSchemeFields.STARTUP_AT.value: VALID_FORMAT_TIMESTAMP_Z_ZONE,
    }

def get_fake_notification_service(
    user: Annotated[User, Depends(get_current_authenticated_user)]
) -> FakeNotificationService:
    return FakeNotificationService()

class TestClientNotificationsBuilder(TestClientBuilder):

    def add_exception(self, method: str, exception: Exception):
        mock = Mock()
        setattr(mock, method, Mock(side_effect=exception))
        app.dependency_overrides[get_notification_service] = lambda: mock
        return self

    def add_fake_notification_service(self):
        app.dependency_overrides[get_notification_service] = get_fake_notification_service
        return self

@pytest.fixture()
def client_auth():
    with TestClientNotificationsBuilder() as test_client_notifications_builder:
        yield test_client_notifications_builder.add_fake_notification_service().add_auth().build()

@pytest.fixture()
def client_not_auth():
    with TestClientNotificationsBuilder() as test_client_notifications_builder:
        yield test_client_notifications_builder.add_fake_notification_service().build()

@pytest.fixture()
def client_factory_with_raised_exception():
    @contextmanager
    def _create(method: str, exception: Exception):
        with TestClientNotificationsBuilder() as test_client_notifications_builder:
            yield test_client_notifications_builder.add_exception(method, exception).add_auth().build()
    return _create

@pytest.fixture()
def database_error():
    str_exc = "Some error with database"
    return DatabaseError(str_exc, None, BaseException(str_exc))
