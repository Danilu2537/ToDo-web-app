import factory.django
import pytest
from django.urls import reverse
from rest_framework import status

from core.models import User


@pytest.mark.django_db()
class TestSignUpView:
    url = reverse('core:signup')

    def test_no_data(self, client):
        response = client.post(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'username': ['Обязательное поле.'],
            'password': ['Обязательное поле.'],
            'password_repeat': ['Обязательное поле.'],
        }

    def test_weak_password(self, client):
        data = {'username': 'test', 'password': '1', 'password_repeat': '1'}
        response = client.post(self.url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'password': [
                'Введённый пароль слишком короткий. '
                'Он должен содержать как минимум 8 символов.',
                'Введённый пароль слишком широко распространён.',
                'Введённый пароль состоит только из цифр.',
            ]
        }

    def test_signup(self, client):
        password = factory.Faker('password', length=8)
        data = {
            'username': 'test',
            'email': 'test@ya.ru',
            'last_name': 'test',
            'first_name': 'test',
            'password': password,
            'password_repeat': password,
        }
        response = client.post(self.url, data=data)
        user = User.objects.get(username='test')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            'id': user.id,
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@ya.ru',
        }


@pytest.mark.django_db()
class TestLoginView:
    url = reverse('core:login')

    def test_no_data(self, client):
        response = client.post(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'username': ['Обязательное поле.'],
            'password': ['Обязательное поле.'],
        }

    def test_login(self, client):
        password = factory.Faker('password', length=8)
        data = {'username': 'test', 'password': password, 'password_repeat': password}
        response = client.post(reverse('core:signup'), data=data)
        user_id = response.json()['id']
        del data['password_repeat']
        response = client.post(self.url, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'email': '',
            'first_name': '',
            'id': user_id,
            'last_name': '',
            'username': 'test',
        }
