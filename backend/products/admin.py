from django.contrib import admin

from .models import (Category, Type)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
