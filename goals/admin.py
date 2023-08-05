from django.contrib import admin

from goals.models import Board, Goal, GoalCategory, GoalComment


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('id', 'title')
    search_fields = ('title',)
    fieldsets = (
        (None, {'fields': ('title', 'user', 'is_deleted')}),
        ('Даты', {'fields': ('created', 'updated')}),
    )


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('id', 'title', 'user')
    search_fields = ('title', 'user')
    fieldsets = (
        (None, {'fields': ('title', 'user', 'is_deleted')}),
        ('Даты', {'fields': ('created', 'updated')}),
    )


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('id', 'title', 'category', 'user')
    search_fields = ('title', 'description', 'category', 'user')
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'title',
                    'description',
                    'due_date',
                    'status',
                    'priority',
                    'category',
                    'user',
                )
            },
        ),
        ('Даты', {'fields': ('created', 'updated')}),
    )


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('id', 'text', 'goal', 'user')
    search_fields = ('goal', 'user', 'text')
    fieldsets = (
        (None, {'fields': ('goal', 'user', 'text')}),
        ('Даты', {'fields': ('created', 'updated')}),
    )
