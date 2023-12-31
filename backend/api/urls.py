from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (ActivateConfirmAPIView, BackCallViewSet, CartAPI,
                    CategoryViewSet, LoginAPIView, OrderViewSet,
                    ProductAPIView, SizeViewSet,
                    TagViewSet, TypeViewSet, UserOrderViewSet,
                    UserRegisterView, UserViewSet, VariationProductViewSet,
                    clear_cart)

app_name = 'api'

router = DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('type', TypeViewSet)
router.register('tags', TagViewSet)
router.register('size', SizeViewSet)
router.register('variation', VariationProductViewSet)
router.register('call', BackCallViewSet)
router.register('order', OrderViewSet)
router.register('users', UserViewSet)
router.register('user_orders', UserOrderViewSet, basename='Order')
router.register('product', ProductAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('confirm_login/<uidb64>/<tokenbs64>/',
         ActivateConfirmAPIView.as_view(), name='confirm_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterView.as_view(), name='registration'),
    path('activate/<uidb64>/<tokenbs64>/', ActivateConfirmAPIView.as_view(),
         name='activate'),
    path('cart/', CartAPI.as_view()),
    path('cart/clear/', clear_cart),
]
