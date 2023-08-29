from distutils.util import strtobool

from django.db.models import F, Q, Count
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, generics, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from api.filters import CategoryTypeFilter, VariationProductFilter
from api.pagination import CustomPagination
from api.permissions import IsAdminOrReadOnly
from api.serializers import (BackCallSerializer, CartSerializer,
                             CategorySerializer, OrderSerializer,
                             ProductShortSerializer, SizeSerializer,
                             TagSerializer, TypeSerializer,
                             VariationProductSerializer, SignupSerializer,
                             TokenObtainPairWithoutPasswordSerializer,
                             UserSerializer, LoginSerializer)
from api.utils import (get_cart, send_confirmation_link, TokenGenerator,
                       send_confirmation_link_for_login)
from client.models import BackCall, Order
from products.models import (Category, CartProduct, Favorite, Size,
                             Tag, Type, VariationProduct)
from rest_framework.decorators import api_view

User = get_user_model()


class APILogin(APIView):
    """APIView-класс для проверки email и отправки ссылки-подтверждения
    пользователю."""
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_confirmation_link_for_login(request, serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


def confirm_login(
        request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    """Функция обрабатывающая ссылку-подтверждение для входа на сайт."""
    account_activation_token = TokenGenerator()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        return HttpResponse('Спасибо за подтверждение! Вы зашли на сайт!')
    return HttpResponse(
        'Ссылка для подтверждения входа на сайт недействительна!')


class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
    """Вьюсет для работы с моделью User, который может получить или
    обновить объект пользователя по его id."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegisterView(generics.CreateAPIView):
    """Generic-класс для создания объекта модели User и отправки
    ссылки-подтверждения на указанный email."""
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        response = super(UserRegisterView, self).create(
            request, *args, **kwargs)
        send_confirmation_link(request, response.data)
        return response


def activate(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    """Функция, которая обрабатывает ссылку-подтверждение для активации
    пользователя."""
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


class TokenObtainPairWithoutPasswordView(TokenViewBase):
    """View-класс, переопределяющий дефолтный сериализатор
    для получения токена."""
    serializer_class = TokenObtainPairWithoutPasswordSerializer


class BackCallViewSet(viewsets.ModelViewSet):
    queryset = BackCall.objects.all()
    serializer_class = BackCallSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def create(self, request):
        serializer = BackCallSerializer(data=request.data)
        if serializer.is_valid():
            backcall = serializer.save()
            subject = 'Новая заявка на обратный звонок'
            html_message = render_to_string(
                'email_templates/backcall.html',
                {'backcall': backcall})
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [
                settings.DEFAULT_TO_EMAIL]
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=from_email,
                recipient_list=to_email,
                html_message=html_message)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = [AllowAny]
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
    filter_backends = [DjangoFilterBackend, CategoryTypeFilter]
    filterset_class = VariationProductFilter

    @action(detail=False, methods=['get'])
    def hits_products(self, request):
        # Получает все товары в корзинах пользователей, считая количество каждого товара
        all_cart_products = CartProduct.objects.values('product').annotate(
            count=Count('product')).order_by('-count')
        top_products = all_cart_products[:10]

        top_product_ids = [item['product'] for item in top_products]
        remaining_count = 10 - len(top_product_ids)

        if remaining_count > 0:
            random_products = VariationProduct.objects.exclude(
                id__in=top_product_ids).order_by('?')[:remaining_count]
            top_product_ids += [product.id for product in random_products]

        top_products_list = VariationProduct.objects.filter(
            id__in=top_product_ids)
        serializer = ProductShortSerializer(top_products_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

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
            category_ids = selected_product.product.category.values_list(
                'id', flat=True)

            # Формируем Q-объект для поиска похожих товаров
            similar_filter = Q(
                size__in=selected_product.size.all(),
                product__category__id__in=category_ids,
                product__type=selected_product.product.type,
                price__lte=F('price') * 1.2
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


class CartAPI(APIView):
    """
    Эндпоинт для корзины.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Метод просмотра корзины.
        """
        cart = get_cart(request)

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
        cart = get_cart(request)

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
        cart = get_cart(request)

        product_id = request.query_params.get("product_id")
        product = get_object_or_404(VariationProduct, id=product_id)
        if product:
            cart.remove(product)
        request.data.update({'cart': cart})
        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
def clear_cart(request):
    cart = get_cart(request)
    cart.clear()
    return Response(status=status.HTTP_204_NO_CONTENT)

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
