from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from core.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ('last_login', 'date_joined')
    list_display = ('id', 'username')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            'Персональная информация',
            {'fields': ('first_name', 'last_name', 'email')},
        ),
        ('Доступы', {'fields': ('is_active', 'is_staff')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.unregister(Group)
