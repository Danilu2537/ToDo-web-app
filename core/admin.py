from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from core.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {"fields": ("first_name", "last_name", "email")}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff'
            ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.unregister(Group)
