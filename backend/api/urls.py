from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (BackCallSerializer, CategoryViewSet, TagViewSet,
                    TypeViewSet, OrderViewSet, SizeViewSet,
                    VariationProductViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('type', TypeViewSet)
router.register('tags', TagViewSet)
router.register('size', SizeViewSet)
router.register('product', VariationProductViewSet)
# router.register('order', OrderViewSet)
# router.register('call', BackCallSerializer)

urlpatterns = [
    path('', include(router.urls)),
]
