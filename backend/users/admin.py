from django.contrib import admin

from .models import CustomUser, Follow


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Админка ингридиентов."""
    list_display = (
        'email',
        'username',
        'first_name',
        'first_name',
        'password'
    )
    search_fields = ('username',)
    list_filter = ('username', 'email')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Админка подписок."""
    list_display = (
        'user',
        'following',
    )
