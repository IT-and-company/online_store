from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, TypeSerializer, TagSerializer, SizeSerializer, ProductShortSerializer,
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
    # filter_backends = [DjangoFilterBackend]
    # # filterset_class = здесь должен быть фильтр

    @staticmethod
    def create_obj(request, pk, model, serializer):
        product = get_object_or_404(VariationProduct, pk=pk)
        if model.objects.filter(product=product, user=request.user).exists():
            return Response(status.HTTP_400_BAD_REQUEST)
        model(product=product, user=request.user).save()
        serializer = serializer(get_object_or_404(VariationProduct, id=pk),
                                context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_obj(request, pk, model):
        get_object_or_404(model, product=pk, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    @action(detail=True, methods=['post'],
            permission_classes=[AllowAny])
    def favorite(self, request, pk):
        return VariationProductViewSet.create_obj(
            request, pk, Favorite, ProductShortSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return VariationProductViewSet.delete_obj(request, pk, Favorite)

    @action(detail=True, methods=['post'],
            permission_classes=[AllowAny])
    def shopping_cart(self, request, pk):
        return VariationProductViewSet.create_obj(
            request, pk, Basket, ProductShortSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return VariationProductViewSet.delete_obj(request, pk, Basket)
