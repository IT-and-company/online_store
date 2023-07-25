from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'pk', 'phone')
    list_filter = ('username', 'phone')
    search_fields = ('username', 'phone')
    empty_value_display = '-пусто-'
