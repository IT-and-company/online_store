from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, TypeSerializer, TagSerializer, SizeSerializer, VariationProductSerializer
from products.models import (Category, Tag, Type, VariationProduct, Size, Favorite, Basket)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class SizeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class VariationProductViewSet(viewsets.ModelViewSet):
    queryset = VariationProduct.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return RecipeViewSet.create_obj(
            request, pk, Favorite, RecipeShortSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return RecipeViewSet.delete_obj(request, pk, Favorite)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return RecipeViewSet.create_obj(
            request, pk, ShoppingCart, RecipeShortSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return RecipeViewSet.delete_obj(request, pk, Basket)

