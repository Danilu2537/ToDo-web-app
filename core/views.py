from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from core.models import User
from core.serializers import (
    CreateUserSerializer,
    LoginSerializer,
    ProfileSerializer,
    UpdatePasswordSerializer,
)


class SignUpView(CreateAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not (user := authenticate(**serializer.validated_data)):
            raise AuthenticationFailed('Invalid username/password')

        login(request=request, user=user)

        return Response(ProfileSerializer(user).data)


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user

    def perform_destroy(self, instance: User) -> None:
        logout(self.request)


class UpdatePasswordView(GenericAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(serializer.data)
