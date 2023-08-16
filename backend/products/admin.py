import json

from django.contrib import admin
from django.contrib.auth.models import Group
from django import forms

from .models import (Basket, Category, Favorite, Image, Product, ProductModel,
                      Size, Specification, Tag, Type, VariationProduct)


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

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
        'type',
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
                    'materials', 'model', 'manufacturer')
    search_fields = ('article_number', 'manufacturer')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image',)
    fields = ('image',)


class VariationProductInline(admin.TabularInline):
    model = VariationProduct
    extra = 0
    min_num = 1


def get_data():
    data = {}
    for type in Type.objects.all():
        data[str(type.id)]={}
    for model in ProductModel.objects.all():
        data[str(model.type.id)][str(model.id)] = {
                'id': str(model.id),
                'type_id': str(model.type.id),
                'name': str(model.name)
        }
    return json.dumps(data)

class ProductAdminForm(forms.ModelForm):
    data = get_data()
    type = forms.ModelChoiceField(
        queryset=Type.objects.all(), 
        widget=forms.Select(
            attrs={
                'onchange': f'model_type = this.options[this.selectedIndex].value; var data = {data};'
                '(function(){ var select = document.getElementById("id_model");'
                ' select.options.length=0; select.options[select.options.length] = new Option("----","");'
                ' for(let [key, value] of Object.entries(data[model_type.toString()]))'
                ' { select.options[select.options.length] = new Option(value.name,value.id);} })()'
                }
        )
    )
    model = forms.ModelChoiceField(
        queryset=ProductModel.objects.all()
    )
    class Meta:
        model = Product
        fields='__all__'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        get_data()
    inlines = (VariationProductInline,)
    list_display = ('name', 'text')
    fields = ('name', 'text', 'category', 'type', 'model')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    readonly_fields = ('is_favorited',)
    form = ProductAdminForm

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
    list_display = ('pk', 'user', 'product', 'quantity')
    search_fields = (
        'user__username',
        'user__phone',
        'product__name'
    )


admin.site.unregister(Group)
