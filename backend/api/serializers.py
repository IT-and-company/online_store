from django.contrib.auth import get_user_model

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from client.models import BackCall, Order
from products.models import (OrderCart, OrderProduct, Category, Favorite, Image, Product, Size,
                             Specification, ColorTag, Type, VariationProduct)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(max_length=150, required=True)
#     phone = PhoneNumberField()
#
#     class Meta:
#         fields = ('name', 'phone',)
#         model = User
#
#     def validate(self, data):
#         if data.get('name') == 'me':
#             raise serializers.ValidationError(
#                 'Пользователь не может иметь такое имя')
#
#         if User.objects.filter(phone=data.get('phone')).exists():
#             raise serializers.ValidationError(
#                 'Пользователь с таким телефоном уже существует')
#
#         return data


class SignupSerializer(serializers.ModelSerializer):
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


class TokenObtainPairWithoutPasswordSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def validate(self, attrs):
        attrs.update({'password': ''})
        return super(
            TokenObtainPairWithoutPasswordSerializer, self).validate(attrs)


# class AuthSerializer(serializers.Serializer):
#     phone = serializers.CharField(max_length=15)
#     verification_code = serializers.CharField(max_length=4)
#
#     def validate(self, data):
#         phone = data.get('phone')
#         # verification_code = data.get('verification_code')
#
#         # Здесь должна быть логика отправки кода и проверки его правильности
#         # Пропустим это для примера
#         # ...
#
#         user = authenticate(request=self.context.get('request'),
#         phone=phone)
#
#         if not user:
#             raise serializers.ValidationError('Неверные учетные данные')
#
#         data['user'] = user
#         return data


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class BackCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackCall
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class ColorTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorTag
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('length',
                  'width',
                  'height')


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Image
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductBaseSerializer(serializers.ModelSerializer):
    color_tag = ColorTagSerializer(read_only=True)
    image = ImageSerializer(many=True, read_only=True)
    price = serializers.IntegerField()
    sale = serializers.IntegerField()
    is_discount = serializers.SerializerMethodField(
        method_name='get_is_discount')
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited')

    class Meta:
        model = VariationProduct
        fields = (
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
                                         recipe=obj).exists())

    def get_is_favorited(self, obj):
        return self.get_request(obj, Favorite)

    def get_is_discount(self, obj):
        return int(obj.price - (obj.price * obj.sale / 100))


class ProductShortSerializer(ProductBaseSerializer):
    product = serializers.CharField(source='product.name', read_only=True)

    class Meta(ProductBaseSerializer.Meta):
        fields = ProductBaseSerializer.Meta.fields + ('product',)


class VariationProductSerializer(ProductBaseSerializer):
    product = ProductSerializer(read_only=True)
    specification = SpecificationSerializer(read_only=True)

    class Meta(ProductBaseSerializer.Meta):
        fields = ProductBaseSerializer.Meta.fields + (
            'product', 'specification')


class CartSerializer(serializers.Serializer):
    product = ProductShortSerializer()
    quantity = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_quantity(self, obj):
        return obj['quantity']

    def get_price(self, obj):
        return obj['price']
