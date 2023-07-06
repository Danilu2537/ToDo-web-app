import django_filters
from django.db import models

from goals.models import Goal


class GoalDateFilter(django_filters.FilterSet):
    class Meta:
        model = Goal
        fields = {
            'due_date': ('lte', 'gte'),
            'category': ('exact', 'in'),
            'status': ('exact', 'in'),
            'priority': ('exact', 'in'),
        }

    filter_overrides = {models.DateTimeField: {'filter_class': django_filters.IsoDateTimeFilter}}
