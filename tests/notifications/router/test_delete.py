import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.exc import DatabaseError

from notifications.exceptions import NotificationNotFound
from src.notifications.constants import NotificationLiteral

service_method = "delete"


def test_delete_occurred_not_found_notification_exception(client_factory_with_raised_exception):
    client = client_factory_with_raised_exception(service_method, NotificationNotFound)
    response = client.delete(f"/{NotificationLiteral.URL.value}/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_occurred_database_exception(client_factory_with_raised_exception):
    client = client_factory_with_raised_exception(service_method, DatabaseError)
    response = client.delete(f"/{NotificationLiteral.URL.value}/1")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

@pytest.mark.parametrize(
    NotificationLiteral.NOTIFICATION_ID.value, [1,2,3]
)
def test_delete(client: TestClient, notification_id: int):
    response = client.delete(f"/{NotificationLiteral.URL.value}/{notification_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.parametrize(
    NotificationLiteral.NOTIFICATION_ID.value, [0, "str_value", -4, {}, []]
)
def test_delete_invalid_cases(client: TestClient, notification_id: int):
    response = client.get(f"/{NotificationLiteral.URL.value}/{notification_id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT