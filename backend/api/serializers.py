from django.shortcuts import get_object_or_404
from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from users.models import User
from users.tokens import account_activation_token


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
