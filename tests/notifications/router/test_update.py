from typing import Any

import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.exc import DatabaseError

from notifications.exceptions import NotificationNotFound
from src.notifications.constants import NotificationLiteral, RepeatInterval, NotificationSchemeFields

service_method = "update"

@pytest.mark.parametrize(
    f"{NotificationLiteral.NOTIFICATION_ID.value}, body_notification", [
        (1, {
            NotificationSchemeFields.TITLE.value: "title-1",
            NotificationSchemeFields.BODY.value: "body-1",
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.ONCE.value,
                NotificationLiteral.STEP.value: 0,
            }
        }),
        (2, {
            NotificationSchemeFields.TITLE.value: None,
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.HOURLY.value,
                NotificationLiteral.STEP.value: 5,
            }
        }),
        (3, {
            NotificationSchemeFields.BODY.value: None,
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.MONTHLY.value,
                NotificationLiteral.STEP.value: 3,
            }
        }),
        (4, {
            NotificationSchemeFields.BODY.value: "edited-title",
        }),
    ]
)
def test_update(client_auth: TestClient, notification_id: int, body_notification: dict[str, Any]):
    response = client_auth.put(f"/{NotificationLiteral.URL.value}/{notification_id}", json=body_notification)
    assert response.status_code == status.HTTP_200_OK

# Invalid bodies for updating the notification
@pytest.mark.parametrize(
    f"{NotificationLiteral.NOTIFICATION_ID.value}, body_notification", [
        (1, {
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                "invalid_key_how_often": RepeatInterval.ONCE.value,
                NotificationLiteral.STEP.value: 0,
            }
        }),
        (2, {
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.HOURLY.value,
                "invalid_key_step": 5,
            }
        }),
        (3, {
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: "unknown_value",
                NotificationLiteral.STEP.value: 3
            }
        }),
        (4, {
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.ONCE.value,
                NotificationLiteral.STEP.value: -2
            }
        }),
        (5, {
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.ONCE.value,
                NotificationLiteral.STEP.value: "value_is_not_int"
            }
        }),
        (6, {
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.ONCE.value,
            }
        }),
        (7, {
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.STEP.value: 3
            }
        }),
    ]
)
def test_update_invalid_cases(client_auth: TestClient, notification_id: int, body_notification: dict[str, Any]):
    response = client_auth.put(f"/{NotificationLiteral.URL.value}/{notification_id}", json=body_notification)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_update_occurred_database_exception(client_factory_with_raised_exception, body_notification: dict[str, Any]):
    with client_factory_with_raised_exception(service_method, DatabaseError) as client:
        response = client.put(f"/{NotificationLiteral.URL.value}/1", json=body_notification)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

def test_update_not_found_notification_exception(client_factory_with_raised_exception, body_notification: dict[str, Any]):
    with client_factory_with_raised_exception(service_method, NotificationNotFound) as client:
        response = client.put(f"/{NotificationLiteral.URL.value}/1", json=body_notification)
        assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_check_not_auth_user(client_not_auth: TestClient, body_notification: dict[str, Any]):
    response = client_not_auth.put(f"/{NotificationLiteral.URL.value}/1", json=body_notification)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
