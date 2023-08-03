from django.db import models


class TgUser(models.Model):
    chat_id = models.PositiveBigIntegerField(
        primary_key=True, editable=False, unique=True, verbose_name='ID чата'
    )
    username = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Имя пользователя'
    )
    user = models.OneToOneField(
        'core.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Пользователь',
    )
    verification_code = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='Код подтверждения'
    )

    @property
    def is_verified(self):
        return bool(self.user)

    @staticmethod
    def _generate_verification_code() -> str:
        import random

        return ''.join(random.choices('0123456789', k=4))

    def update_verification_code(self) -> None:
        self.verification_code = self._generate_verification_code()
        self.save(update_fields=['verification_code'])

    def __str__(self):
        return f'{self.__class__.__name__} ({self.chat_id})'
