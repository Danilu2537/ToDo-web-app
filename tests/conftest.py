import pytest
from rest_framework.test import APIClient

pytest_plugins = 'tests.factories'


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture()
@pytest.mark.django_db
def auth_client(client, user):
    client.user = user
    client.force_login(client.user)
    return client
