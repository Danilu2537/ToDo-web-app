from django.db import models

from goals.choices import Priority, Status


class BaseGoalsModel(models.Model):
    """Базовый класс для моделей приложения goals, содержит автоматические поля created и updated"""

    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        abstract = True


class GoalCategory(BaseGoalsModel):
    """Категория целей"""

    title = models.CharField(max_length=255, verbose_name='Название')
    user = models.ForeignKey('core.User', on_delete=models.PROTECT, verbose_name='Автор')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Goal(BaseGoalsModel):
    """Цель"""

    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.CharField(max_length=1000, null=True, verbose_name='Описание')
    due_date = models.DateTimeField(null=True, verbose_name='Дата выполнения')
    status = models.PositiveSmallIntegerField(
        choices=Status.choices, default=Status.to_do, verbose_name='Статус'
    )
    priority = models.PositiveSmallIntegerField(
        choices=Priority.choices, default=Priority.medium, verbose_name='Приоритет'
    )
    category = models.ForeignKey('GoalCategory', on_delete=models.PROTECT, verbose_name='Категория')
    user = models.ForeignKey('core.User', on_delete=models.PROTECT, verbose_name='Автор')

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    def __str__(self):
        """Строковое представление модели"""
        return self.title


class GoalComment(BaseGoalsModel):
    """Комментарий к цели"""

    user = models.ForeignKey('core.User', on_delete=models.PROTECT, verbose_name='Автор')
    goal = models.ForeignKey('Goal', on_delete=models.PROTECT, verbose_name='Цель')
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
