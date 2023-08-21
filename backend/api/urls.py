from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, SizeViewSet, TagViewSet, TypeViewSet,
                    VariationProductViewSet, APISignup)

app_name = 'api'

router = DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('type', TypeViewSet)
router.register('tags', TagViewSet)
router.register('size', SizeViewSet)
router.register('product', VariationProductViewSet)

url_auth = (
    path('auth/signup', APISignup.as_view(), name='signup'),
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(url_auth))
]
