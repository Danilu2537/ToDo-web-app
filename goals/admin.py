from django.contrib import admin

from goals.models import GoalCategory


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'update')
    list_display = ('id', 'title', 'user')
    fieldsets = ((None, {'fields': ('title', 'user', 'is_deleted')}), ('Даты', {'fields': ('created', 'update')}))
