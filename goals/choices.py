from django.db import models


class Status(models.IntegerChoices):
    """Класс для работы со статусом целей"""

    to_do = 1, 'К выполнению'
    in_progress = 2, 'В процессе'
    done = 3, 'Выполнено'
    archived = 4, 'Архив'


class Priority(models.IntegerChoices):
    """Класс для работы с приоритетом целей"""

    low = 1, 'Низкий'
    medium = 2, 'Средний'
    high = 3, 'Высокий'
    critical = 4, 'Критический'


class Role(models.IntegerChoices):
    """Класс для работы с ролями участников доски"""

    owner = 1, 'Владелец'
    writer = 2, 'Редактор'
    reader = 3, 'Читатель'
