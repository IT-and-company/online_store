# from django.db import models
# from django.db.models import F, Sum
# # from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from products.models import (Basket, Category, Favorite, Size, Tag, Type,
                             VariationProduct)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import VariationProductFilter
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, OrderSerializer,
                          ProductShortSerializer, SizeSerializer,
                          TagSerializer, TypeSerializer,
                          VariationProductSerializer)


class OrderViewSet(viewsets.ViewSet):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    # def send_email(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         data = serializer.validated_data
    #         # Отправляем форму на почту
    #         send_mail(
    #             'Sent email from {}'.format(data.get('name')),
    #             'Here is the message. {}'.format(data.get('text')),
    #             data.get('email'),
    #             ['to@example.com'],
    #             fail_silently=False,
    #         )
    #         return Response(
    #         data=serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(
    #     serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    @action(detail=False, methods=['get'])
    def latest_products(self, request):
        queryset = VariationProduct.objects.all().order_by('-pub_date')
        serializer = ProductShortSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def similar_products(self, request):
        product_id = request.query_params.get('product_id')

        if product_id:
            # Получаем выбранный продукт
            selected_product = VariationProduct.objects.get(pk=product_id)

            # Формируем Q-объект для поиска похожих товаров
            similar_filter = Q(
                size=selected_product.size,
                type=selected_product.type,
                price__lte=selected_product.price * 1.2,
                category=selected_product.category
            )

            # Применяем фильтр к запросу
            queryset = VariationProduct.objects.filter(similar_filter).exclude(
                pk=selected_product.pk)

            serializer = ProductShortSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status.HTTP_400_BAD_REQUEST)

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
    #         discounted_price=(F('price') - F(
    #         'price') * F('sale') / 100) * F('quantity')).agregate(
    #         'discounted_price', output_field=models.FloatField())
    #     return Response({
    #         'count_sum': count_sum['count_sum'] or 0
    #     })
    # Product.objects.filter(featured=True).annotate(
    # offer=((F('totalprice') - F('saleprice')) / F('totalprice')) * 100)

# class PurchaseView(APIView):
#     def post(self, request, *args, **kwargs):
#         product_id = request.data.get('product_id')
#
#         try:
#             product = VariationProduct.objects.get(pk=product_id)
#         except VariationProduct.DoesNotExist:
#             return Response({
#             'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         with transaction.atomic():
#             # Создаем запись о покупке
#
#             # Увеличиваем количество покупок товара
#             product.purchases_count += 1
#             product.save()
#
#         return Response({'message': 'Purchase successful'},
#         status=status.HTTP_201_CREATED)
