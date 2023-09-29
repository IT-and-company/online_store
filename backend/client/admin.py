from django.contrib import admin

from .models import (BackCall,
                     CartProduct,
                     Order,
                     OrderCart,
                     OrderProduct,
                     UserCart,)


class OrderCartInline(admin.StackedInline):
    model = OrderCart
    extra = 0
    min_num = 1
    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderCartInline,)
    list_display = (
        'pk',
        'name',
        'phone',
        'email',
        'address',
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


@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user')
    search_fields = (
        'user__username',
    )


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'cart', 'product', 'quantity')
    search_fields = (
        'product__name',
    )


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    min_num = 1


@admin.register(OrderCart)
class OrderCartAdmin(admin.ModelAdmin):
    inlines = (OrderProductInline,)
    list_display = ('pk', 'order')
    search_fields = (
        'order__email',
        'order__address',
    )


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'cart', 'product', 'quantity')
    search_fields = (
        'product__name',
    )
