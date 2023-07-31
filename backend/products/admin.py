from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (Category, Tag, Type, Size, Specification, Product, VariationProduct, Favorite, Basket, Image)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('length', 'width', 'height')
    search_fields = ('length', 'width', 'height')


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('article_number',
                    'materials', 'type', 'manufacturer')
    search_fields = ('article_number', 'manufacturer')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image',)
    fields = ('image',)


class VariationProductInline(admin.TabularInline):
    model = VariationProduct
    extra = 0
    min_num = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (VariationProductInline,)
    list_display = ('name', 'text')
    fields = ('name', 'text', 'category', 'type')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    readonly_fields = ('is_favorited',)

    @admin.display(description='Количество избраного')
    def is_favorited(self, obj):
        return obj.favorite.count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'product')
    search_fields = (
        'user__username',
        'user__phone',
        'product__name'
    )


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'product')
    search_fields = (
        'user__username',
        'user__phone',
        'product__name'
    )


admin.site.unregister(Group)
