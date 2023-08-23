from django_filters.rest_framework import FilterSet, filters
from products.models import (Category, ProductModel, Size,
                             Tag, Type, VariationProduct)
from rest_framework.filters import BaseFilterBackend


class VariationProductFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug',
                                             to_field_name='slug',
                                             queryset=Tag.objects.all())
    size = filters.ModelMultipleChoiceFilter(field_name='size',
                                             queryset=Size.objects.all())
    model = filters.ModelMultipleChoiceFilter(
        field_name='model', queryset=ProductModel.objects.all())
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    is_favorited = filters.BooleanFilter(
        method='get_favorited')
    is_in_basket = filters.BooleanFilter(
        method='get_is_in_basket')

    class Meta:
        model = VariationProduct
        fields = ['tags', 'is_favorited', 'is_in_basket', 'size', 'model',
                  'min_price', 'max_price']

    def get_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorite__user=user)
        return queryset

    def get_is_in_basket(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(basket__user=user)
        return queryset


class CategoryTypeFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        categories = request.query_params.getlist('categories')
        types = request.query_params.getlist('types')

        if categories:
            queryset = queryset.filter(product__category__slug__in=categories)

        if types:
            queryset = queryset.filter(product__type__slug__in=types)

        return queryset
