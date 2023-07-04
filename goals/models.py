from django.db import models


class GoalCategory(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(max_length=255, verbose_name='Название')
    user = models.ForeignKey('core.User', on_delete=models.PROTECT, verbose_name='Автор')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
