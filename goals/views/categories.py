from django.db import transaction
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from goals.choices import Status
from goals.models import GoalCategory
from goals.permissions import GoalCategoryPermission
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    """Вью для создания категории целей"""

    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """Вью для получения списка категорий целей"""

    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategorySerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        """Получение списка категорий целей для текущего пользователя"""
        return GoalCategory.objects.select_related('user').filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """Вью для получения, обновления и удаления категории целей"""

    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermission]

    def get_queryset(self):
        """Получение категории целей для текущего пользователя"""
        return GoalCategory.objects.select_related('user').exclude(is_deleted=True)

    def perform_destroy(self, instance):
        """Удаление категории целей и всех ее целей"""
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.goal_set.update(status=Status.archived)
