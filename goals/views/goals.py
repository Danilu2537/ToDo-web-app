from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from goals.choices import Status
from goals.filters import GoalDateFilter
from goals.models import Goal
from goals.permissions import GoalPermission
from goals.serializers import GoalCreateSerializer, GoalListSerializer, GoalSerializer


class GoalCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [GoalPermission]
    queryset = Goal.objects.exclude(status=Status.archived)

    def perform_destroy(self, instance):
        instance.status = Status.archived
        instance.save()


class GoalListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalListSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ['title', 'description']
    ordering = ['title']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user,
            category__is_deleted=False,
        ).exclude(status=Status.archived)
