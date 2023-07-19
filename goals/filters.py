import django_filters
from django.db import models
from django_filters.rest_framework import FilterSet

from goals.models import Goal


class GoalDateFilter(FilterSet):
    class Meta:
        model = Goal
        fields = {
            'due_date': ('lte', 'gte'),
            'category': ('exact', 'in'),
            'status': ('exact', 'in'),
            'priority': ('exact', 'in'),
        }

    filter_overrides = {models.DateTimeField: {'filter_class': django_filters.IsoDateTimeFilter}}
