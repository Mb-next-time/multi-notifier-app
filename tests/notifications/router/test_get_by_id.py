import pytest

from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.exc import DatabaseError

from notifications.exceptions import NotificationNotFound
from src.notifications.constants import NotificationLiteral

service_method = "get_by_id"


def test_get_by_id_occurred_not_found_notification_exception(client_factory_with_raised_exception):
    with client_factory_with_raised_exception(service_method, NotificationNotFound) as client:
        response = client.get(f"/{NotificationLiteral.URL.value}/1")
        assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_by_id_occurred_database_exception(client_factory_with_raised_exception):
    with client_factory_with_raised_exception(service_method, DatabaseError) as client:
        response = client.get(f"/{NotificationLiteral.URL.value}/1")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

@pytest.mark.parametrize(
    NotificationLiteral.NOTIFICATION_ID.value, [1,2,3]
)
def test_get_by_id(client_auth: TestClient, notification_id: int):
    response = client_auth.get(f"/{NotificationLiteral.URL.value}/{notification_id}")
    assert response.json().get("id") == notification_id

@pytest.mark.parametrize(
    NotificationLiteral.NOTIFICATION_ID.value, [0, "str_value", -4, {}, []]
)
def test_get_by_id_invalid_cases(client_auth: TestClient, notification_id: int):
    response = client_auth.get(f"/{NotificationLiteral.URL.value}/{notification_id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_get_by_id_check_not_auth_user(client_not_auth):
    response = client_not_auth.get(f"/{NotificationLiteral.URL.value}/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
