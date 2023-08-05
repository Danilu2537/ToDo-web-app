from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from goals.choices import Role
from goals.models import BoardParticipant


class BoardPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        _filters = {'user': request.user, 'board': obj}
        if request.method not in SAFE_METHODS:
            _filters['role'] = Role.owner

        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCategoryPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        _filters = {'user': request.user, 'board': obj.board}
        if request.method not in SAFE_METHODS:
            _filters['role__in'] = [Role.owner, Role.writer]

        return BoardParticipant.objects.filter(**_filters).exists()


class GoalPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        _filters = {'user': request.user, 'board': obj.category.board}
        if request.method not in SAFE_METHODS:
            _filters['role__in'] = [Role.owner, Role.writer]

        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCommentPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
