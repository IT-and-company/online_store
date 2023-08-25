from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (BackCallViewSet, CartAPI, CategoryViewSet, OrderViewSet,
                    SizeViewSet, TagViewSet, TypeViewSet,
                    VariationProductViewSet, UserRegisterView,
                    activate, TokenObtainPairWithoutPasswordView, UserViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('type', TypeViewSet)
router.register('tags', TagViewSet)
router.register('size', SizeViewSet)
router.register('product', VariationProductViewSet)
router.register('call', BackCallViewSet)
router.register('order', OrderViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairWithoutPasswordView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterView.as_view(), name='registration'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('cart/', CartAPI.as_view()),
]
