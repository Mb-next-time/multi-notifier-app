from contextlib import contextmanager
from unittest.mock import Mock

import pytest

from auth.dependencies import get_auth_service
from src.main import app
from tests import TestClientBuilder

class TestClientAuthBuilder(TestClientBuilder):

    def add_exception(self, method: str, exception: Exception):
        mock = Mock()
        setattr(mock, method, Mock(side_effect=exception))
        app.dependency_overrides[get_auth_service] = lambda: mock
        return self

@pytest.fixture()
def valid_credentials():
    return {"username": "test", "password": "test1234"}

@pytest.fixture()
def invalid_credentials():
    return {"username": "test1", "password": "test"}

@pytest.fixture
def client_not_auth():
    with TestClientAuthBuilder() as test_client_auth_builder:
        yield test_client_auth_builder.build()

@pytest.fixture()
def client_factory_with_raised_exception():
    @contextmanager
    def _create(method: str, exception: Exception):
        with TestClientAuthBuilder() as test_client_auth_builder:
            yield test_client_auth_builder.add_exception(method, exception).build()
    return _create