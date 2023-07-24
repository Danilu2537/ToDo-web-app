import django_filters
from django.db import models
from django_filters.rest_framework import FilterSet

from goals.models import Goal, GoalCategory


class GoalCategoryFilter(FilterSet):
    """Фильтр для работы с категориями целей, фильтрует категории по доскам"""

    class Meta:
        model = GoalCategory
        fields = {'board': ('exact',)}


class GoalDateFilter(FilterSet):
    """Фильтр для работы с целью, работает с полями due_date, category, status, priority"""

    class Meta:
        model = Goal
        fields = {
            'due_date': ('lte', 'gte'),
            'category': ('exact', 'in'),
            'status': ('exact', 'in'),
            'priority': ('exact', 'in'),
        }

    filter_overrides = {models.DateTimeField: {'filter_class': django_filters.IsoDateTimeFilter}}
