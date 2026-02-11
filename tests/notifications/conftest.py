from contextlib import contextmanager
from typing import Annotated
from unittest.mock import Mock

import pytest
from fastapi import Depends
from sqlalchemy.exc import DatabaseError

from auth.dependencies import get_current_authenticated_user
from auth.models import User
from notifications import schemas
from notifications.constants import NotificationSchemeField, NotificationStatus
from notifications.dependencies import get_notification_service
from notifications.schemas import FilterNotification
from notifications.models import Notification
from main import app
from tests import TestClientBuilder


class FakeNotificationService:

    async def get_list(self, filter_notification: FilterNotification):
        return [
            Notification(id=1, body="body-1", title="title-1", status=NotificationStatus.ACTIVE.value),
            Notification(id=2, body="body-2", title="title-2", status=NotificationStatus.INACTIVE.value),
            Notification(id=3, body="body-3", title="title-3", status=NotificationStatus.ACTIVE.value),
        ]

    async def create(self, body_notification: schemas.BodyNotification) -> Notification:
        return Notification(id=5, **body_notification.model_dump(), status=NotificationStatus.ACTIVE.value)

    async def get(self, notification_id: int) -> Notification:
        return Notification(id=notification_id, body="body", title="title", status=NotificationStatus.ACTIVE.value)

    async def update(self, notification_id: int, body_notification: schemas.UpdateNotification) -> Notification:
        notification = await self.get(notification_id)
        for field, value in body_notification.model_dump(exclude_unset=True).items():
            setattr(notification, field, value)
        return notification

    async def delete(self, notification_id: int) -> None:
        return

@pytest.fixture
def valid_json_body_notification():
    return {
        NotificationSchemeField.TITLE.value: "title-1",
        NotificationSchemeField.BODY.value: "body-1",
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
