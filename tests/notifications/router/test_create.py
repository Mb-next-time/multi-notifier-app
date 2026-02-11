import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.exc import DatabaseError

from notifications.constants import NotificationLiteral,NotificationSchemeField
from constants import API_URL_V1

API_URL = API_URL_V1

def test_create(client_auth: TestClient, valid_json_body_notification):
    response = client_auth.post(f"{API_URL}/{NotificationLiteral.URL.value}/", json=valid_json_body_notification)
    assert response.status_code == status.HTTP_201_CREATED

# Invalid bodies for creating the notification
@pytest.mark.parametrize(
    "json_body_notification", [
        {
            NotificationSchemeField.TITLE.value: "title-1",
            # empty field body
        },
        {
            # empty field title
            NotificationSchemeField.BODY.value: "body-1",
        },
        # empty request body
        {
        },
    ]
)
def test_create_invalid_cases(client_auth: TestClient, json_body_notification):
    response = client_auth.post(f"{API_URL}/{NotificationLiteral.URL.value}/", json=json_body_notification)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_create_occurred_database_exception(client_factory_with_raised_exception, valid_json_body_notification, database_error):
    with client_factory_with_raised_exception("create", database_error) as client:
        with pytest.raises(DatabaseError):
            client.post(f"{API_URL}/{NotificationLiteral.URL.value}/", json=valid_json_body_notification)

def test_create_check_not_auth_user(client_not_auth, valid_json_body_notification):
    response = client_not_auth.post(f"{API_URL}/{NotificationLiteral.URL.value}/", json=valid_json_body_notification)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED