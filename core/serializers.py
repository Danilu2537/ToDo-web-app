from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from core.fields import PasswordField
from core.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""

    password = PasswordField()
    password_repeat = PasswordField(validate=False)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_repeat',
        )

    def validate(self, attrs: dict) -> dict:
        """Проверка паролей"""
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data: dict) -> User:
        """Создание пользователя с учетом хеширования пароля"""
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    """Сериализатор для авторизации"""

    username = serializers.CharField(required=True)
    password = PasswordField(validate=False)


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UpdatePasswordSerializer(serializers.Serializer):
    """Сериализатор для обновления пароля"""

    old_password = PasswordField(validate=False)
    new_password = PasswordField()

    def validate_old_password(self, attrs: dict) -> dict:
        """Проверка старого пароля"""
        if not self.context['request'].user.check_password(attrs['old_password']):
            raise serializers.ValidationError('Invalid password')
        return attrs
