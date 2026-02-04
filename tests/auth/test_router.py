import pytest
from fastapi import status

from auth.exceptions import AuthIsFailed, AuthDuplication
from auth.constants import AuthLiterals

method_login_user = "login_user"
login_endpoint = "login"

def test_login_auth_is_failed_exception(client_factory_with_raised_exception, valid_credentials):
    with client_factory_with_raised_exception(method_login_user, AuthIsFailed) as client:
        response = client.post(f"{AuthLiterals.URL.value}/{login_endpoint}", json=valid_credentials)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_login_occurred_exception(client_factory_with_raised_exception, valid_credentials):

    with client_factory_with_raised_exception(method_login_user, Exception) as client:
        with pytest.raises(Exception):
            client.post(f"{AuthLiterals.URL.value}/{login_endpoint}", json=valid_credentials)

def test_login_validation_credentials(client_not_auth, invalid_credentials):
    response = client_not_auth.post(f"{AuthLiterals.URL.value}/{login_endpoint}", json=invalid_credentials)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

method_register_user = "register_user"
register_endpoint = "register"

def test_register_integrity_error_exception(client_factory_with_raised_exception, valid_credentials):
    with client_factory_with_raised_exception(method_register_user, AuthDuplication) as client:
        response = client.post(f"{AuthLiterals.URL.value}/{register_endpoint}", json=valid_credentials)
        assert response.status_code == status.HTTP_409_CONFLICT

def test_register_occurred_exception(client_factory_with_raised_exception, valid_credentials):

    with client_factory_with_raised_exception(method_register_user, Exception) as client:
        with pytest.raises(Exception):
            client.post(f"{AuthLiterals.URL.value}/{login_endpoint}", json=valid_credentials)

def test_register_validation_credentials(client_not_auth, invalid_credentials):
    response = client_not_auth.post(f"{AuthLiterals.URL.value}/{register_endpoint}", json=invalid_credentials)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
