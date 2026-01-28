from unittest.mock import Mock

from starlette.testclient import TestClient

from auth.dependencies import get_current_authenticated_user
from auth.models import User
from src.main import app


class TestClientBuilder:

    def add_auth(self):
        app.dependency_overrides[get_current_authenticated_user] = lambda: User(id=1)
        return self

    def build(self):
        return TestClient(app)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clear()

    def _clear(self):
        app.dependency_overrides.clear()
        return self
