import pytest
from rest_framework.test import APIClient

from core.models import User

pytest_plugins = 'tests.factories'


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture()
@pytest.mark.django_db
def auth_client(client):
    client.user = User.objects.create_user(username='test', password='test')
    client.login(username='test', password='test')
    return client
