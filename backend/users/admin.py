from django.contrib import admin

from users.models import User, Follow
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
    list_filter = ("email", "username")

    @admin.action(description="Заблокировать выбранных пользователей")
    def block_user(modeladmin, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Разблокировать выбранных пользователей")
    def unblock_user(modeladmin, request, queryset):
        queryset.update(is_active=True)

    UserAdmin.actions += (block_user, unblock_user, )


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
