# from django.db import models
# from django.db.models import F, Sum
# # from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.exceptions import ValidationError
# from rest_framework.status import HTTP_200_OK
# from rest_framework.views import APIView

from products.models import (Basket, Category, Favorite, Size, Tag, Type,
                             VariationProduct)
from rest_framework import status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .utils import send_confirmation_link, TokenGenerator
from .filters import VariationProductFilter
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, OrderSerializer,
                          ProductShortSerializer, SizeSerializer,
                          TagSerializer, TypeSerializer,
                          VariationProductSerializer, SignupSerializer)


User = get_user_model()


# class APISignup(APIView):
#     def post(self, request):
#         serializer = SignupSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=HTTP_200_OK)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        response = super(UserRegisterView, self).create(
            request, *args, **kwargs)
        send_confirmation_link(request, response.data)
        return response


def activate(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    account_activation_token = TokenGenerator()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse(
            'Спасибо за подтверждение! Ваш аккаунт активирован!')
    return HttpResponse('Ссылка для активации недействительна!')


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
