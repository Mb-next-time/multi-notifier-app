from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.exc import DatabaseError

from src.notifications.constants import NotificationLiteral


def test_get_list_is_success(client: TestClient):
    response = client.get(f"/{NotificationLiteral.URL.value}/")
    assert response.status_code == status.HTTP_200_OK

def test_get_list_occurred_exception(client_factory_with_raised_exception):
    client = client_factory_with_raised_exception("get_list", DatabaseError)
    response = client.get(f"/{NotificationLiteral.URL.value}/")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR