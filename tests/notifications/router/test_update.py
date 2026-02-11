import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.exc import DatabaseError

from notifications.exceptions import NotificationNotFound
from notifications.constants import NotificationLiteral, NotificationSchemeField, NotificationStatus
from constants import API_URL_V1

service_method = "update"
API_URL = API_URL_V1

@pytest.mark.parametrize(
    f"{NotificationLiteral.NOTIFICATION_ID.value}, json_body_notification", [
        (1, {
            NotificationSchemeField.TITLE.value: "title-1",
        }),
        (2, {
            NotificationSchemeField.BODY.value: "body-1",
        }),
        (3, {
            NotificationSchemeField.STATUS.value: NotificationStatus.ACTIVE.value
        }),
        (4, {
            NotificationSchemeField.STATUS.value: NotificationStatus.INACTIVE.value
        }),
        (4, {
            NotificationSchemeField.STATUS.value: NotificationStatus.DELETED.value
        }),
    ]
)
def test_update(client_auth: TestClient, notification_id: int, json_body_notification):
    response = client_auth.put(f"{API_URL}/{NotificationLiteral.URL.value}/{notification_id}", json=json_body_notification)
    assert response.status_code == status.HTTP_200_OK

# Invalid bodies for updating the notification
@pytest.mark.parametrize(
    f"{NotificationLiteral.NOTIFICATION_ID.value}, json_body_notification", [
        (1, {
            NotificationSchemeField.STATUS.value: "not_allowed_status_value"
        }),
    ]
)
def test_update_invalid_cases(client_auth: TestClient, notification_id: int, json_body_notification):
    response = client_auth.put(f"{API_URL}/{NotificationLiteral.URL.value}/{notification_id}", json=json_body_notification)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_update_occurred_database_exception(client_factory_with_raised_exception, valid_json_body_notification, database_error):
    with pytest.raises(DatabaseError):
        with client_factory_with_raised_exception(service_method, database_error) as client:
            client.put(f"{API_URL}/{NotificationLiteral.URL.value}/1", json=valid_json_body_notification)

def test_update_not_found_notification_exception(client_factory_with_raised_exception, valid_json_body_notification):
    with client_factory_with_raised_exception(service_method, NotificationNotFound) as client:
        response = client.put(f"{API_URL}/{NotificationLiteral.URL.value}/1", json=valid_json_body_notification)
        assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_check_not_auth_user(client_not_auth: TestClient, valid_json_body_notification):
    response = client_not_auth.put(f"{API_URL}/{NotificationLiteral.URL.value}/1", json=valid_json_body_notification)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
