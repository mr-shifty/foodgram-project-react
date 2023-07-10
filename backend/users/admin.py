from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Follow


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username', 'email',
        'first_name', 'last_name', 'id',
    )
    list_filter = ('email', 'first_name')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
