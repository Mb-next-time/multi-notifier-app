import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.exc import DatabaseError

from notifications.constants import NotificationLiteral, RepeatInterval,NotificationSchemeFields
from tests.notifications.conftest import VALID_FORMAT_TIMESTAMP_Z_ZONE, VALID_FORMAT_TIMESTAMP_OFFSET_ZONE


@pytest.mark.parametrize(
    "json_body_notification", [
        {
            NotificationSchemeFields.TITLE.value: "title-1",
            NotificationSchemeFields.BODY.value: "body-1",
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.ONCE.value,
                NotificationLiteral.STEP.value: 0,
            },
            NotificationSchemeFields.STARTUP_AT.value: VALID_FORMAT_TIMESTAMP_Z_ZONE,
        },
        {
            NotificationSchemeFields.BODY.value: None,
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.HOURLY.value,
                NotificationLiteral.STEP.value: 5,
            },
            NotificationSchemeFields.STARTUP_AT.value: VALID_FORMAT_TIMESTAMP_Z_ZONE,
        },
        {
            NotificationSchemeFields.BODY.value: None,
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.MONTHLY.value,
                NotificationLiteral.STEP.value: 3,
            },
            NotificationSchemeFields.STARTUP_AT.value: VALID_FORMAT_TIMESTAMP_OFFSET_ZONE,
        },
    ]
)
def test_create(client_auth: TestClient, json_body_notification):
    response = client_auth.post(f"/{NotificationLiteral.URL.value}/", json=json_body_notification)
    assert response.status_code == status.HTTP_201_CREATED

# Invalid bodies for creating the notification
@pytest.mark.parametrize(
    "json_body_notification", [
        {
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                "invalid_key_how_often": RepeatInterval.ONCE.value,
                NotificationLiteral.STEP.value: 0,
            }
        },
        {
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.HOURLY.value,
                "invalid_key_step": 5,
            }
        },
        {
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: "unknown_value",
                NotificationLiteral.STEP.value: 3
            }
        },
        {
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.ONCE.value,
                NotificationLiteral.STEP.value: -2
            }
        },
        {
            NotificationSchemeFields.REPEAT_INTERVAL.value: {
                NotificationLiteral.HOW_OFTEN.value: RepeatInterval.ONCE.value,
                NotificationLiteral.STEP.value: "value_is_not_int"
            }
        },
        # empty body
        {
        },
    ]
)
def test_create_invalid_cases(client_auth: TestClient, json_body_notification):
    response = client_auth.post(f"/{NotificationLiteral.URL.value}/", json=json_body_notification)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_create_occurred_database_exception(client_factory_with_raised_exception, valid_json_body_notification, database_error):
    with client_factory_with_raised_exception("create", database_error) as client:
        with pytest.raises(DatabaseError):
            client.post(f"/{NotificationLiteral.URL.value}/", json=valid_json_body_notification)

def test_create_check_not_auth_user(client_not_auth, valid_json_body_notification):
    response = client_not_auth.post(f"/{NotificationLiteral.URL.value}/", json=valid_json_body_notification)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED