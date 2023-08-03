from django.db import models

from goals.choices import Priority, Role, Status


class BaseGoalsModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления'
    )

    class Meta:
        abstract = True


class Board(BaseGoalsModel):
    title = models.CharField(max_length=255, verbose_name='Название')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    def __str__(self):
        return self.title


class BoardParticipant(BaseGoalsModel):
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)
    board = models.ForeignKey(
        Board,
        verbose_name='Доска',
        on_delete=models.PROTECT,
        related_name='participants',
    )
    user = models.ForeignKey(
        'core.User',
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        related_name='participants',
    )
    role = models.PositiveSmallIntegerField(
        verbose_name='Роль', choices=Role.choices, default=Role.owner
    )

    editable_roles = Role.choices[1:]

    class Meta:
        unique_together = ('board', 'user')
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return self.title


class GoalCategory(BaseGoalsModel):
    board = models.ForeignKey(
        Board,
        on_delete=models.PROTECT,
        related_name='categories',
        verbose_name='Доска',
    )
    title = models.CharField(max_length=255, verbose_name='Название')
    user = models.ForeignKey(
        'core.User', on_delete=models.PROTECT, verbose_name='Автор'
    )
    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Goal(BaseGoalsModel):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name='Описание'
    )
    due_date = models.DateTimeField(null=True, verbose_name='Дата выполнения')
    status = models.PositiveSmallIntegerField(
        choices=Status.choices, default=Status.to_do, verbose_name='Статус'
    )
    priority = models.PositiveSmallIntegerField(
        choices=Priority.choices,
        default=Priority.medium,
        verbose_name='Приоритет',
    )
    category = models.ForeignKey(
        'GoalCategory', on_delete=models.PROTECT, verbose_name='Категория'
    )
    user = models.ForeignKey(
        'core.User', on_delete=models.PROTECT, verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    def __str__(self):
        return self.title


class GoalComment(BaseGoalsModel):
    user = models.ForeignKey(
        'core.User', on_delete=models.PROTECT, verbose_name='Автор'
    )
    goal = models.ForeignKey(
        'Goal', on_delete=models.PROTECT, verbose_name='Цель'
    )
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
