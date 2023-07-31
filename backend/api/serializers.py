from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from products.models import (Category, Tag, Type, Size, Specification, Product, VariationProduct, Favorite, Basket, Image)

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    phone = PhoneNumberField()

    class Meta:
        fields = (
            'username', 'phone')
        model = User

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Пользователь не может иметь такое имя')

        if User.objects.filter(phone=data.get('phone')).exists():
            raise serializers.ValidationError(
                'Пользователь с таким телефоном уже существует')

        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует')
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
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


class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationProduct
        fields = (
            'id',
            'product',
            'image',
            'price',
            'sale',
            'size',
            'tags'
        )


class VariationProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(source='product', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    image = ImageSerializer(many=True, read_only=True)
    specification = SpecificationSerializer(read_only=True)
    price = serializers.IntegerField()
    sale = serializers.IntegerField()
    is_discount = serializers.SerializerMethodField(
        method_name='get_is_discount')
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited')
    is_in_basket = serializers.SerializerMethodField(
        method_name='get_is_in_basket')

    class Meta:
        model = VariationProduct
        fields = (
            'id',
            'product',
            'image',
            'price',
            'sale',
            'size',
            'tags',
            'specification'
        )

    @staticmethod
    def get_is_discount(obj):
        return obj.price - (obj.price * obj.sale / 100)

    def get_request(self, obj, model):
        return (self.context.get('request')
                and model.objects.filter(product=obj).exists())

    def get_is_in_basket(self, obj):
        return self.get_request(obj, Basket)

    def get_is_favorited(self, obj):
        return self.get_request(obj, Favorite)
