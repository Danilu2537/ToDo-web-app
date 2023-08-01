from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from core.models import User
from core.serializers import (
    CreateUserSerializer,
    LoginSerializer,
    ProfileSerializer,
    UpdatePasswordSerializer,
)


class SignUpView(CreateAPIView):
    """Вью для регистрации пользователя"""

    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """Создание пользователя c помощью сериализатора CreateUserSerializer"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    """Вью для авторизации пользователя"""

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """Авторизация пользователя c помощью сериализатора LoginSerializer"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not (user := authenticate(**serializer.validated_data)):
            raise AuthenticationFailed('Invalid username/password')

        login(request=request, user=user)

        return Response(ProfileSerializer(user).data)


class ProfileView(RetrieveUpdateDestroyAPIView):
    """Вью для работы с профилем пользователя"""

    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> User:
        """Получение объекта пользователя"""
        return self.request.user

    def perform_destroy(self, instance: User) -> None:
        """Выход из аккаунта"""
        logout(self.request)


class UpdatePasswordView(GenericAPIView):
    """Вью для обновления пароля пользователя"""

    serializer_class = UpdatePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs) -> Response:
        """Обновление пароля пользователя c помощью сериализатора UpdatePasswordSerializer"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(serializer.data)
