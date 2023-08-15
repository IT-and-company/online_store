from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, TypeViewSet, SizeViewSet, TagViewSet, VariationProductViewSet

app_name = 'api'

router = DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('type', TypeViewSet)
router.register('tags', TagViewSet)
router.register('size', SizeViewSet)
router.register('product', VariationProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
