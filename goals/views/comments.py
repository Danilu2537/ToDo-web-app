from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalComment
from goals.permissions import GoalCommentPermission
from goals.serializers import (
    GoalCommentCreateSerializer,
    GoalCommentSerializer,
)


class GoalCommentCreateView(CreateAPIView):
    """Вью для создания комментария к цели"""

    permission_classes = [IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    """Вью для получения списка комментариев к цели"""

    permission_classes = [IsAuthenticated]
    serializer_class = GoalCommentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self):
        """Получение списка комментариев к цели для текущего пользователя"""
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class GoalCommentDetailView(RetrieveUpdateDestroyAPIView):
    """Вью для получения, обновления и удаления комментария к цели"""

    permission_classes = [GoalCommentPermission]
    serializer_class = GoalCommentSerializer

    def get_queryset(self):
        """Получение списка комментариев к цели для текущего пользователя"""
        return GoalComment.objects.select_related('user').filter(
            goal__category__board__participants__user=self.request.user
        )
