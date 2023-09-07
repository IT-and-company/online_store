import datetime
from distutils.util import strtobool

from django.db.models import Count, Max, Q
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
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from api.filters import CategoryTypeFilter, VariationProductFilter
from api.pagination import CustomPagination
from api.permissions import IsAdminOrReadOnly
from api.serializers import (BackCallSerializer, CartSerializer,
                             CategorySerializer, OrderListSerializer,
                             OrderCreateSerializer, ProductFullSerializer,
                             ProductShortSerializer, SizeSerializer,
                             ColorTagSerializer, TypeSerializer,
                             VariationProductSerializer, SignupSerializer,
                             TokenObtainPairWithoutPasswordSerializer,
                             UserSerializer, LoginSerializer)
from api.utils import (TokenGenerator, get_cart, send_confirmation_link,
                       send_order)
from client.models import BackCall, Order, CartProduct, OrderCart, OrderProduct
from products.models import (Category,
                             ColorTag,
                             Favorite,
                             Product,
                             Size,
                             Type,
                             VariationProduct, )

User = get_user_model()


class LoginAPIView(APIView):
    """APIView-класс для проверки email и отправки ссылки-подтверждения
    пользователю."""

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_confirmation_link(
            request=request,
            user_data=serializer.data,
            title='Ссылка для подтверждения входа на сайт',
            template='email_templates/login.html'
        )
        return Response(status=status.HTTP_200_OK)


class UserRegisterView(generics.CreateAPIView):
    """Generic-класс для создания объекта модели User и отправки
    ссылки-подтверждения на указанный email."""
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        response = super(UserRegisterView, self).create(
            request, *args, **kwargs)
        send_confirmation_link(
            request=request,
            user_data=response.data,
            title='Ссылка для подтверждения аккаунта',
            template='email_templates/activate_email.html'
        )
        return response


class ActivateConfirmAPIView(APIView):
    """API-view класс, обрабатывающий ссылки-подтверждения для активации
    и входа на сайт."""

    def get(self, request: HttpRequest, uidb64: str,
            tokenbs64: str) -> HttpResponse:
        activation_token = TokenGenerator()
        serializer = UserSerializer
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            token = force_str(urlsafe_base64_decode(tokenbs64))
            user: User = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            token = None
        if (user is not None and token is not None
                and activation_token.check_token(user, token)):
            if not user.is_active:
                user.is_active = True
                user.save()
            serialized_data = serializer(user)
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(
            {'errors': 'Ссылка-подтверждение недействительна!'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
    """Вьюсет для работы с моделью User, который может получить или
    обновить объект пользователя по его id."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TokenObtainPairWithoutPasswordView(TokenViewBase):
    """View-класс, переопределяющий дефолтный сериализатор
    для получения токена."""
    serializer_class = TokenObtainPairWithoutPasswordSerializer


class BackCallViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с заявками на обратный звонок."""
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
    """Вьюсет для работы с заказами."""
    queryset = Order.objects.all()
    permission_classes = [AllowAny]
    pagination_class = None
    # Отображаем созданные заказы с корзиной и продуктами
    serializer_classes = {
        'list': OrderListSerializer,
        'retrieve': OrderListSerializer,
    }
    # При создании получаем корзину автоматически,
    # поэтому сериализуем только поля заказа
    default_serializer_class = OrderCreateSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action, self.default_serializer_class
        )

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            cart = get_cart(request)
            if len(cart) == 0:
                return Response(
                    {'detail': 'cart is empty'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            order_data = serializer.validated_data
            order = Order.objects.create(**order_data)
            order_cart_data = {'order': order}

            if request.user.is_authenticated:
                order_cart_data['user'] = request.user

            order_cart = OrderCart.objects.create(**order_cart_data)
            cart_items = []
            for item in cart:
                product_data = {
                    'product': item['variation'],
                    'quantity': item['quantity'],
                    'price': item['price'],
                }
                OrderProduct.objects.create(
                    cart=order_cart,
                    **product_data
                )
                product_data['total_price'] = item['total_price']
                cart_items.append(product_data)

            order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Отправляем сообщение с данными заказа на почту магазина
            emails = {
                'store_email': (settings.DEFAULT_TO_EMAIL,),
                'user_email': (order.email,)
            }
            for mail_data in [
                {
                    'subject': 'Новая заявка на заказ',
                    'to_email': emails['store_email'],
                    'message': ('Поступил новый заказ.<br>'
                                f'Дата и время заказа: {order_time}<br>')
                },
                {
                    'subject': 'Ваш заказ',
                    'to_email': emails['user_email'],
                    'message': ('Ваш заказ в магазине Мебельный бутик<br>'
                                'Наш менеджер вскоре с Вами свяжется<br>'
                                'Для уточнения деталей заказа<br>'
                                f'Дата и время заказа: {order_time}<br>')
                },
            ]:
                send_order(
                    subject=mail_data['subject'],
                    template='email_templates/store_order.html',
                    to_email=mail_data['to_email'],
                    order=order,
                    cart=cart,
                    cart_items=cart_items,
                    message=mail_data['message']
                )
            cart.clear()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UserOrderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вьюсет для отображения заказов текущего пользователя."""
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Order.objects.filter(cart__user__id=self.request.user.pk)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с категориями товаров."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с типами товаров."""
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с цветами товаров."""
    queryset = ColorTag.objects.all()
    serializer_class = ColorTagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class SizeViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с размерами товаров."""
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class ProductVariationsView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductFullSerializer
    lookup_field = 'pk'


class ProductAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductFullSerializer

    @action(detail=False, methods=['get'])
    def hits(self, request):
        all_cart_products = CartProduct.objects.values('product').annotate(
            count=Count('product')).order_by('-count')
        top_products = all_cart_products[:10]

        top_product_ids = [item['product'] for item in top_products]
        remaining_count = 10 - len(top_product_ids)

        if remaining_count > 0:
            random_products = VariationProduct.objects.exclude(
                id__in=top_product_ids).order_by('?')[:remaining_count]
            top_product_ids += [product.id for product in random_products]

        top_products_list = Product.objects.filter(
            variations__id__in=top_product_ids).distinct()
        serializer = ProductFullSerializer(top_products_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def latest(self, request):
        queryset = Product.objects.annotate(
            pub_date=Max('variations__pub_date')
        ).order_by('pub_date')
        serializer = ProductFullSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def similar(self, request):
        product_id = request.query_params.get('product_id')

        if product_id:
            # Получаем выбранную вариацию продукта
            selected_product = VariationProduct.objects.get(pk=product_id)
            category_ids = selected_product.product.category.values_list(
                'id', flat=True)

            # Формируем Q-объект для поиска похожих вариаций
            similar_filter = Q(
                product__category__id__in=category_ids,
                size__length__range=(
                    selected_product.size.length - 20,
                    selected_product.size.length + 20
                ),
                size__width__range=(
                    selected_product.size.width - 20,
                    selected_product.size.width + 20
                ),
                size__height__range=(
                    selected_product.size.height - 20,
                    selected_product.size.height + 20
                ),
                product__type=selected_product.product.type,
                price__range=(
                    selected_product.price * 0.8,
                    selected_product.price * 1.2
                )
            )

            # Применяем фильтр к запросу
            variations = VariationProduct.objects.prefetch_related(
                'product'
            ).filter(similar_filter).exclude(pk=selected_product.pk)
            queryset = [variation.product for variation in variations]
            serializer = ProductFullSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {'detail': 'Required query parameter product_id not found.'},
            status.HTTP_400_BAD_REQUEST
        )


class VariationProductViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с вариациями товаров."""
    queryset = VariationProduct.objects.all()
    serializer_class = VariationProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, CategoryTypeFilter]
    filterset_class = VariationProductFilter

    @staticmethod
    def create_obj(request, pk, model, serializer):
        product = get_object_or_404(VariationProduct, pk=pk)

        if model.objects.filter(product=product,
                                user=request.user).exists():
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


class CartAPI(APIView):
    """
    Эндпоинт корзины товаров текущего пользователя.
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
        return Response(
            {'cart': {
                'variations': serialized_cart,
                'total_price': total_price,
                'total_quantity': total_quantity
            }}, status=status.HTTP_200_OK
        )

    def post(self, request, **kwargs):
        """
        Метод добавления товара в корзину.
        """
        cart = get_cart(request)
        product_id = request.query_params.get("product_id")
        if not product_id:
            return Response(
                {
                    'detail': 'Required query parameter product_id not found.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            product = VariationProduct.objects.get(id=product_id)
        except VariationProduct.DoesNotExist:
            return Response(
                {
                    'detail': f'No variation with id {product_id} found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        cart.add(
            product=product,
            quantity=int(request.query_params.get('quantity', 1)),
            update_quantity=strtobool(
                request.query_params.get('update_quantity', 'False')
            )
        )
        try:
            request.data.update({'cart': cart})
        except AttributeError:
            request.data._mutable = True
            request.data.update({'cart': cart})
            request.data._mutable = False
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
        try:
            request.data.update({'cart': cart})
        except AttributeError:
            request.data._mutable = True
            request.data.update({'cart': cart})
            request.data._mutable = False
        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
def clear_cart(request):
    cart = get_cart(request)
    cart.clear()
    return Response(status=status.HTTP_204_NO_CONTENT)
