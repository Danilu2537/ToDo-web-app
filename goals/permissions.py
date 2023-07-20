from rest_framework.permissions import IsAuthenticated


class GoalCategoryPermission(IsAuthenticated):
    """Проверка на владельца категории целей"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class GoalPermission(IsAuthenticated):
    """Проверка на владельца цели"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class GoalCommentPermission(IsAuthenticated):
    """Проверка на владельца комментария к цели"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
