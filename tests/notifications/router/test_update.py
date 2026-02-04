import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.exc import DatabaseError

from notifications.exceptions import NotificationNotFound
from notifications.constants import NotificationLiteral, RepeatInterval, NotificationSchemeFields
from tests.notifications.conftest import (
    VALID_FORMAT_TIMESTAMP_OFFSET_ZONE,
    VALID_FORMAT_TIMESTAMP_Z_ZONE,
    INVALID_FORMAT_TIMESTAMP,
)

service_method = "update"

@pytest.mark.parametrize(
    f"{NotificationLiteral.NOTIFICATION_ID.value}, json_body_notification", [
        (1, {
            NotificationSchemeFields.TITLE.value: "title-1",
            NotificationSchemeFields.BODY.value: "body-1",
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.ONCE.value,
                NotificationLiteral.STEP.value: 0,
            },
            NotificationSchemeFields.STARTUP_AT.value: VALID_FORMAT_TIMESTAMP_OFFSET_ZONE,
        }),
        (2, {
            NotificationSchemeFields.TITLE.value: None,
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.HOURLY.value,
                NotificationLiteral.STEP.value: 5,
            },
            NotificationSchemeFields.STARTUP_AT.value: VALID_FORMAT_TIMESTAMP_Z_ZONE,
        }),
        (3, {
            NotificationSchemeFields.BODY.value: None,
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.MONTHLY.value,
                NotificationLiteral.STEP.value: 3,
            },
            NotificationSchemeFields.STARTUP_AT.value: VALID_FORMAT_TIMESTAMP_Z_ZONE,
        }),
        (4, {
            NotificationSchemeFields.BODY.value: "edited-title",
            NotificationSchemeFields.STARTUP_AT.value: VALID_FORMAT_TIMESTAMP_Z_ZONE,
        }),
    ]
)
def test_update(client_auth: TestClient, notification_id: int, json_body_notification):
    response = client_auth.put(f"/{NotificationLiteral.URL.value}/{notification_id}", json=json_body_notification)
    assert response.status_code == status.HTTP_200_OK

# Invalid bodies for updating the notification
@pytest.mark.parametrize(
    f"{NotificationLiteral.NOTIFICATION_ID.value}, json_body_notification", [
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
        (8, {
            NotificationSchemeFields.BODY.value: "edited-title",
            NotificationSchemeFields.STARTUP_AT.value: INVALID_FORMAT_TIMESTAMP,
        }),
    ]
)
def test_update_invalid_cases(client_auth: TestClient, notification_id: int, json_body_notification):
    response = client_auth.put(f"/{NotificationLiteral.URL.value}/{notification_id}", json=json_body_notification)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_update_occurred_database_exception(client_factory_with_raised_exception, valid_json_body_notification, database_error):
    with pytest.raises(DatabaseError):
        with client_factory_with_raised_exception(service_method, database_error) as client:
            client.put(f"/{NotificationLiteral.URL.value}/1", json=valid_json_body_notification)

def test_update_not_found_notification_exception(client_factory_with_raised_exception, valid_json_body_notification):
    with client_factory_with_raised_exception(service_method, NotificationNotFound) as client:
        response = client.put(f"/{NotificationLiteral.URL.value}/1", json=valid_json_body_notification)
        assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_check_not_auth_user(client_not_auth: TestClient, valid_json_body_notification):
    response = client_not_auth.put(f"/{NotificationLiteral.URL.value}/1", json=valid_json_body_notification)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
