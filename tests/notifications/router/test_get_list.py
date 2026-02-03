from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.exc import DatabaseError

from notifications.constants import NotificationLiteral


def test_get_list_is_success(client_auth: TestClient):
    response = client_auth.get(f"/{NotificationLiteral.URL.value}/")
    assert response.status_code == status.HTTP_200_OK

def test_get_list_occurred_exception(client_factory_with_raised_exception):
    with client_factory_with_raised_exception("get_list", DatabaseError) as client:
        response = client.get(f"/{NotificationLiteral.URL.value}/")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

def test_get_list_check_not_auth_user(client_not_auth):
    response = client_not_auth.get(f"/{NotificationLiteral.URL.value}/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
