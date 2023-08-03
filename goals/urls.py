from django.urls import path

from goals.views.boards import BoardCreateView, BoardListView, BoardView
from goals.views.categories import (
    GoalCategoryCreateView,
    GoalCategoryListView,
    GoalCategoryView,
)
from goals.views.comments import (
    GoalCommentCreateView,
    GoalCommentDetailView,
    GoalCommentListView,
)
from goals.views.goals import GoalCreateView, GoalListView, GoalView

app_name = 'goals'

urlpatterns = [
    # Эндпоинты для работы с досками
    path('board/create', BoardCreateView.as_view(), name='create-board'),
    path('board/list', BoardListView.as_view(), name='list-board'),
    path('board/<int:pk>', BoardView.as_view(), name='detail-board'),
    # Эндпоинты для работы с категориями целей
    path(
        'goal_category/create',
        GoalCategoryCreateView.as_view(),
        name='create-category',
    ),
    path(
        'goal_category/list',
        GoalCategoryListView.as_view(),
        name='list-category',
    ),
    path(
        'goal_category/<int:pk>',
        GoalCategoryView.as_view(),
        name='detail-category',
    ),
    # Эндпоинты для работы с целями
    path('goal/create', GoalCreateView.as_view(), name='create-goal'),
    path('goal/list', GoalListView.as_view(), name='list-goal'),
    path('goal/<int:pk>', GoalView.as_view(), name='detail-goal'),
    # Эндпоинты для работы с комментариями к целям
    path(
        'goal_comment/create',
        GoalCommentCreateView.as_view(),
        name='create-comment',
    ),
    path(
        'goal_comment/list', GoalCommentListView.as_view(), name='list-comment'
    ),
    path(
        'goal_comment/<int:pk>',
        GoalCommentDetailView.as_view(),
        name='detail-comment',
    ),
]
