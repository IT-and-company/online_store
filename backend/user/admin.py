from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'pk', 'phone')
    list_filter = ('email', 'phone')
    search_fields = ('email', 'phone')
    empty_value_display = '-пусто-'
