from django.db import models

from goals.choices import Priority, Status


class GoalCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    user = models.ForeignKey('core.User', on_delete=models.PROTECT, verbose_name='Автор')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Goal(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.CharField(max_length=1000, null=True, verbose_name='Описание')
    due_date = models.DateTimeField(null=True, verbose_name='Дата выполнения')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')
    status = models.PositiveSmallIntegerField(
        choices=Status.choices, default=Status.to_do, verbose_name='Статус'
    )
    priority = models.PositiveSmallIntegerField(
        choices=Priority.choices, default=Priority.medium, verbose_name='Приоритет'
    )
    category = models.ForeignKey('GoalCategory', on_delete=models.PROTECT, verbose_name='Категория')
    user = models.ForeignKey('core.User', on_delete=models.PROTECT, verbose_name='Автор')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
