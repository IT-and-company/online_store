from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (BackCallViewSet, CartAPI, CategoryViewSet, OrderViewSet,
                    SizeViewSet, TagViewSet, TypeViewSet,
                    VariationProductViewSet, UserRegisterView,
                    activate, clear_cart, TokenObtainPairWithoutPasswordView,
                    UserViewSet, APILogin, confirm_login)

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
    path('login/', APILogin.as_view(), name='login'),
    path('confirm_login/<uidb64>/<token>/', confirm_login,
         name='confirm_login'),
    path('token/', TokenObtainPairWithoutPasswordView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterView.as_view(), name='registration'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('cart/', CartAPI.as_view()),
    path('cart/clear/', clear_cart),
]
