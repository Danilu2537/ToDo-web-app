from django.db import transaction
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from goals.choices import Status
from goals.models import Board, BoardParticipant, Goal
from goals.permissions import BoardPermission
from goals.serializers import BoardSerializer, BoardWithParticipantsSerializer


class BoardCreateView(CreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        with transaction.atomic():
            board = serializer.save()
            BoardParticipant.objects.create(board=board, user=self.request.user)


class BoardListView(ListAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user).exclude(
            is_deleted=True
        )


class BoardView(RetrieveUpdateDestroyAPIView):
    serializer_class = BoardWithParticipantsSerializer
    permission_classes = [BoardPermission]

    def get_queryset(self):
        return Board.objects.prefetch_related('participants__user').exclude(
            is_deleted=True
        )

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Status.archived)
