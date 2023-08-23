# from django.db import models
# from django.db.models import F, Sum
# # from django.http import HttpResponse
from distutils.util import strtobool

from django.conf import settings  # noqa
from django.core.mail import send_mail  # noqa
from django.shortcuts import get_object_or_404  # noqa
from django.template.loader import render_to_string  # noqa
from django.utils.html import strip_tags  # noqa
from django_filters.rest_framework import DjangoFilterBackend  # noqa
from rest_framework import status, viewsets  # noqa
from rest_framework.decorators import action  # noqa
from rest_framework.permissions import AllowAny  # noqa
from rest_framework.response import Response  # noqa
from rest_framework.views import APIView  # noqa

from api.filters import VariationProductFilter  # noqa
from api.pagination import CustomPagination  # noqa
from api.permissions import IsAdminOrReadOnly  # noqa
from api.serializers import VariationProductSerializer  # noqa
from api.serializers import (CartSerializer, CategorySerializer,  # noqa
                             OrderSerializer, ProductShortSerializer,
                             SizeSerializer, TagSerializer, TypeSerializer)
from client.models import Order  # noqa
from products.cart import Cart  # noqa
from products.models import (CartProduct, Category, Favorite, Size,  # noqa
                             Tag, Type, UserCart, VariationProduct)

  # noqa


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
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
    #         return Response(data=serializer.data,
    #               status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors,
    #               status=status.HTTP_400_BAD_REQUEST)


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

    # @action(detail=True, methods=['post'],
    #         permission_classes=[AllowAny])
    # def basket(self, request, pk):
    #     return VariationProductViewSet.create_obj(
    #         request, pk, Basket, ProductShortSerializer)

    # @basket.mapping.delete
    # def delete_basket(self, request, pk):
    #     return VariationProductViewSet.delete_obj(request, pk, Basket)


class CartAPI(APIView):
    """
    Эндпоинт для корзины.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Метод просмотра корзины.
        """
        if request.user.is_authenticated:
            user = request.user
            cart = Cart(user_id=user.id)
        else:
            cart = Cart(request=request)
        print(cart.__dict__)

        serialized_cart = list(CartSerializer(
            cart,
            many=True,
            context={'request': request}
        ).data)

        total_price = cart.get_total_price()
        total_quantity = len(cart)
        serialized_cart.append({'total_price': total_price})
        serialized_cart.append({'total_quantity': total_quantity})
        return Response({'cart': serialized_cart}, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        """
        Метод добавления товара в корзину.
        """
        if request.user.is_authenticated:
            user = request.user
            cart = Cart(user_id=user.id)
        else:
            cart = Cart(request=request)

        product_id = request.query_params.get("product_id")
        product = get_object_or_404(VariationProduct, id=product_id)
        if product:
            cart.add(
                product=product,
                quantity=int(request.query_params.get('quantity', 1)),
                update_quantity=strtobool(
                    request.query_params.get('update_quantity')
                )
            )
        request.data.update({'cart': cart})
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        """
        Метод удаления продуктов из корзины.
        """
        if request.user.is_authenticated:
            user = request.user
            cart = Cart(user_id=user.id)
        else:
            cart = Cart(request=request)
        product_id = request.query_params.get("product_id")
        product = get_object_or_404(VariationProduct, id=product_id)
        if product:
            cart.remove(product)
        request.data.update({'cart': cart})
        return Response(status=status.HTTP_202_ACCEPTED)

    # @action(methods=['get'], detail=False,
    #         permission_classes=[AllowAny])
    # def count_basket(self, request):
    #     if request.user.is_authenticated:
    #         user = request.user
    #     else:
    #         user = None

    # не хватает колличества продуктов

    #     count_sum = VariationProduct.objects.filter(
    #         product__basket__user=user).anotate(
    #         discounted_price=(F('price') - F('price') * F('sale') / 100
    #               ) * F('quantity')).agregate(
    #         'discounted_price', output_field=models.FloatField())
    #     return Response({
    #         'count_sum': count_sum['count_sum'] or 0
    #     })
    # Product.objects.filter(featured=True).annotate(offer=(
    #       (F('totalprice') - F('saleprice')) / F('totalprice')) * 100)

# class PurchaseView(APIView):
#     def post(self, request, *args, **kwargs):
#         product_id = request.data.get('product_id')
#
#         try:
#             product = VariationProduct.objects.get(pk=product_id)
#         except VariationProduct.DoesNotExist:
#             return Response(
#               {'error': 'Product not found'},
#                   status=status.HTTP_404_NOT_FOUND)
#
#         with transaction.atomic():
#             # Создаем запись о покупке
#
#             # Увеличиваем количество покупок товара
#             product.purchases_count += 1
#             product.save()
#
#         return Response({'message': 'Purchase successful'},
#               status=status.HTTP_201_CREATED)
