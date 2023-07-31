from django.shortcuts import render
from .serializers import CategorySerializer, TypeSerializer
from products.models import (Category, Tag, Type)


class CategoryViewSet():
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet():
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
