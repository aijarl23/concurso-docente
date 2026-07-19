from django.contrib import admin
from .models import UserAccess


@admin.register(UserAccess)
class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'access_type', 'status', 'granted_at', 'expires_at')
    list_filter = ('access_type', 'status', 'module')
    search_fields = ('user__username', 'user__email', 'module__title')
