from django_filters.rest_framework import FilterSet, filters
from products.models import (ProductModel, Size, ColorTag,
                             VariationProduct, Product, Category,
                             Type)


class VariationProductFilter(FilterSet):
    """Класс фильтрации для обработки полей модели VariationProduct."""
    color_tag = filters.ModelMultipleChoiceFilter(
        field_name='color_tag__slug',
        to_field_name='slug',
        queryset=ColorTag.objects.all()
    )
    size = filters.ModelMultipleChoiceFilter(field_name='size',
                                             queryset=Size.objects.all())
    model = filters.ModelMultipleChoiceFilter(
        field_name='product__model', queryset=ProductModel.objects.all())
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    is_favorited = filters.BooleanFilter(
        method='get_favorited')

    class Meta:
        model = VariationProduct
        fields = ['color_tag', 'is_favorited', 'size', 'model',
                  'min_price', 'max_price']

    def get_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorite__user=user)
        return queryset


class CategoryTypeFilter(FilterSet):
    """Класс фильтрации, который сортирует продукты по типу и категории."""
    category = filters.ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all()
    )
    type = filters.ModelMultipleChoiceFilter(
        field_name='type',
        queryset=Type.objects.all()
    )
    min_price = filters.NumberFilter(
        field_name="variations__price", lookup_expr='gte')
    max_price = filters.NumberFilter(
        field_name="variations__price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'type']
