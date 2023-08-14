from django.db import models
from django.db.models import F, Sum
# from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from .filters import VariationProductFilter
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, TypeSerializer,
                          TagSerializer, SizeSerializer, ProductShortSerializer, VariationProductSerializer)
from products.models import (Category, Tag, Type, VariationProduct, Size, Favorite, Basket)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    pagination_class = None


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
    serializer_class = VariationProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = VariationProductFilter

    @staticmethod
    def create_obj(request, pk, model, serializer):
        product = get_object_or_404(VariationProduct, pk=pk)

        # Это какая-то нереальная хтонь, но оно работает.

        if request.user.is_authenticated:
            user = request.user
        else:
            user = None

        if user and model.objects.filter(product=product, user=user).exists():
            return Response(status.HTTP_400_BAD_REQUEST)

        model(product=product, user=user).save()
        serializer = serializer(get_object_or_404(VariationProduct, id=pk),
                                context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_obj(request, pk, model):
        product = get_object_or_404(VariationProduct, pk=pk)

        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        model.objects.filter(product=product, user=user).delete()

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
    def basket(self, request, pk):
        return VariationProductViewSet.create_obj(
            request, pk, Basket, ProductShortSerializer)

    @basket.mapping.delete
    def delete_basket(self, request, pk):
        return VariationProductViewSet.delete_obj(request, pk, Basket)

    # @action(methods=['get'], detail=False,
    #         permission_classes=[AllowAny])
    # def count_basket(self, request):
    #     if request.user.is_authenticated:
    #         user = request.user
    #     else:
    #         user = None

    # нехватает колличества продуктов

    #     count_sum = VariationProduct.objects.filter(
    #         product__basket__user=user).anotate(
    #         discounted_price=F('price') - F('price') * F('sale') / 100).agregate(
    #         'discounted_price', output_field=models.FloatField())
    #     return Response({
    #         'count_sum': count_sum['count_sum'] or 0
    #     })
