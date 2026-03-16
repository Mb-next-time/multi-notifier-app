import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.exc import DatabaseError

from notifications.exceptions import NotificationNotFound
from notifications.constants import NotificationLiteral, NotificationSchemeField
from constants import API_URL_V1

service_method = "update"
API_URL = API_URL_V1

@pytest.mark.parametrize(
    f"{NotificationLiteral.NOTIFICATION_ID.value}, json_body_notification", [
        (1, {
            NotificationSchemeField.BODY.value: "body-1",
        })
    ]
)
def test_update(client_auth: TestClient, notification_id: int, json_body_notification):
    response = client_auth.put(f"{API_URL}/{NotificationLiteral.URL.value}/{notification_id}", json=json_body_notification)
    assert response.status_code == status.HTTP_200_OK

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
