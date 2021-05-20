from django.urls import path, include
from .routers import router
from .views import (
    ApplyPromoCodeGenericAPIView,
    CheckOutCreateAPIView,
    UserOrderListAPIView,
)

urlpatterns = [
    path('', include(router.urls)),
    path('apply-promo-code/', ApplyPromoCodeGenericAPIView.as_view(), name='apply_promo_code'),
    path('checkout/', CheckOutCreateAPIView.as_view(), name='checkout'),
    path('user-list/', UserOrderListAPIView.as_view(), name='user_orders')
]