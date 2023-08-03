from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    readonly_fields = ('chat_id', 'username', 'user', 'verification_code')
    list_display = (
        'chat_id',
        'username',
        'user',
        'verification_code',
        'is_verified',
    )
    search_fields = ('chat_id', 'username')
    fieldsets = (
        (
            None,
            {'fields': ('chat_id', 'username', 'user', 'verification_code')},
        ),
    )

    def tg_user(self, obj: TgUser) -> str | None:
        if user := obj.user:
            return format_html(
                f'<a href="{reverse("admin:core_user_change", args=(user.id,))}">{user}</a>'
            )
