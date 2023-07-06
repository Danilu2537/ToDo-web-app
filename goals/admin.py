from django.contrib import admin

from goals.models import Goal, GoalCategory


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'update')
    list_display = ('id', 'title', 'user')
    search_fields = ('title', 'user')
    fieldsets = (
        (None, {'fields': ('title', 'user', 'is_deleted')}),
        ('Даты', {'fields': ('created', 'update')}),
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
