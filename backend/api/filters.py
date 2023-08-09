from django_filters.rest_framework import FilterSet, filters
from products.models import Tag, Size, Specification, VariationProduct


class VariationProductFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug',
                                             to_field_name='slug',
                                             queryset=Tag.objects.all())
    size = filters.ModelMultipleChoiceFilter(field_name='size',
                                             queryset=Size.objects.all())
    model = filters.ModelMultipleChoiceFilter(
        field_name='model',
        queryset=Specification.objects.all())
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = VariationProduct
        fields = ['tags', 'size', 'model', 'min_price', 'max_price']


