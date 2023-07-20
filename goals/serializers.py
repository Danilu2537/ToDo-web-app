from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied

from core.serializers import ProfileSerializer
from goals.choices import Status
from goals.models import Goal, GoalCategory, GoalComment


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания категории целей"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'


class GoalCategorySerializer(GoalCategoryCreateSerializer):
    """Сериализатор для получения категории целей"""

    user = ProfileSerializer(read_only=True)


class GoalCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания цели"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, value):
        """Проверка категории цели, проверяет, что категория не удалена и принадлежит текущему пользователю"""
        if value.is_deleted:
            raise NotFound('Категория не найдена')
        if value.user != self.context['request'].user:
            raise PermissionDenied('Нет доступа к этой категории')
        return value

    class Meta:
        model = Goal
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'


class GoalSerializer(serializers.ModelSerializer):
    """Сериализатор для получения цели"""

    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания комментария к цели"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_goal(self, value):
        """Проверка цели, проверяет, что цель не архивирована и принадлежит текущему пользователю"""
        if value.status == Status.archived:
            raise NotFound('Цель не найдена')
        if value.user != self.context['request'].user:
            raise PermissionDenied('Нет доступа к этой цели')
        return value

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'


class GoalCommentSerializer(serializers.ModelSerializer):
    """Сериализатор для получения комментария к цели"""

    user = ProfileSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user', 'goal')
        fields = '__all__'
