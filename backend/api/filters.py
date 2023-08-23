from django_filters.rest_framework import FilterSet, filters

from products.models import ProductModel, Size, Tag, Type, VariationProduct


class VariationProductFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug',
                                             to_field_name='slug',
                                             queryset=Tag.objects.all())
    size = filters.ModelMultipleChoiceFilter(field_name='size',
                                             queryset=Size.objects.all())
    type = filters.ModelMultipleChoiceFilter(
        field_name='type', queryset=Type.objects.all())
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
