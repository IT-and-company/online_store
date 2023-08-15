from django.contrib import admin
from .models import Order, BackCall


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'phone',
        'email',
        'address'
    )
    list_filter = ('name', 'phone', 'address')
    search_fields = ('name', 'phone')
    empty_value_display = '-пусто-'


@admin.register(BackCall)
class BackCall(admin.ModelAdmin):
    list_display = (
        'name',
        'phone'
    )
