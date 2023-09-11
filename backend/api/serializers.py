from django.contrib.auth import get_user_model

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from client.models import BackCall, Order, OrderCart, OrderProduct
from products.models import (Category, Favorite, Picture, Product, Size,
                             Specification, ColorTag, Type, VariationProduct)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с объектами модели User."""
    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    """Сериализатор для проверки и обработки email при входе на сайт."""
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError(
                f'Email "{value}" не зарегистрирован или не активирован'
            )
        return value


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для создания нового объекта модели User."""
    class Meta:
        model = User
        fields = ('first_name', 'email')

    def create(self, validated_data):
        try:
            user, _ = User.objects.get_or_create(**validated_data)
        except Exception as error:
            raise ValidationError(
                f'Ошибка создания нового пользователя: {error}')
        user.is_active = False
        user.save()
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                f'Email "{value}" уже используется'
            )
        return value


class OrderProductSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с объектами модели OrderProduct."""

    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderCartSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с объектами модели OrderCart."""
    products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = OrderCart
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    """Сериализатор для работы со списком заказов."""
    cart = OrderCartSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заказа."""
    class Meta:
        model = Order
        fields = '__all__'


class BackCallSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с заявками на обратный звонок."""
    class Meta:
        model = BackCall
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для работы с категориями товаров."""
    class Meta:
        model = Category
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с типами товаров."""
    class Meta:
        model = Type
        fields = '__all__'


class ColorTagSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с цветами товаров."""
    class Meta:
        model = ColorTag
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с размерами товаров."""
    class Meta:
        model = Size
        fields = ('length',
                  'width',
                  'height')


class SpecificationSerializer(serializers.ModelSerializer):
    """Сериализатор для работы со спецификацией товаров."""
    class Meta:
        model = Specification
        fields = '__all__'


class PictureSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с изображениями товаров."""
    image = Base64ImageField()

    class Meta:
        model = Picture
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с товарами."""
    class Meta:
        model = Product
        fields = '__all__'


class ProductBaseSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения продукта со всеми характеристиками
    и дополнительными полями."""
    color_tag = ColorTagSerializer(read_only=True)
    image = PictureSerializer(many=True, read_only=True)
    price = serializers.IntegerField()
    sale = serializers.IntegerField()
    is_discount = serializers.SerializerMethodField(
        method_name='get_is_discount')
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited')

    class Meta:
        model = VariationProduct
        depth = 2
        fields = (
            'id',
            'image',
            'price',
            'sale',
            'size',
            'color_tag',
            'is_discount',
            'is_favorited',
        )

    def get_request(self, obj, model):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and model.objects.filter(user=request.user,
                                         product=obj).exists())

    def get_is_favorited(self, obj):
        return self.get_request(obj, Favorite)

    def get_is_discount(self, obj):
        return int(obj.price - (obj.price * obj.sale / 100))


class ProductShortSerializer(ProductBaseSerializer):
    """Сериализатор наследующийся от базового сериализатор товаров,
    который добавляет к каждому объекту товара поле product."""
    product = serializers.CharField(source='product.name', read_only=True)

    class Meta(ProductBaseSerializer.Meta):
        fields = ProductBaseSerializer.Meta.fields + ('product',)


class VariationProductSerializer(ProductBaseSerializer):
    """Сериализатор для работы с разными вариантами каждого товара."""
    product = ProductSerializer(read_only=True)
    specification = SpecificationSerializer(read_only=True)

    class Meta(ProductBaseSerializer.Meta):
        fields = ProductBaseSerializer.Meta.fields + (
            'product', 'specification')


class ProductFullSerializer(serializers.ModelSerializer):
    variations = ProductBaseSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.Serializer):
    """Сериализатор для работы с корзиной."""
    variation = VariationProductSerializer()
    quantity = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_quantity(self, obj):
        return obj['quantity']

    def get_price(self, obj):
        return obj['price']
