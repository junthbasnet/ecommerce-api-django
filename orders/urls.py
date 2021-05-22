from django.urls import path, include
from .routers import router
from .views import (
    ApplyPromoCodeGenericAPIView,
    CheckOutCreateAPIView,
    OrderListAPIView,
    OrderProductListAPIView,
    MarkOrderAsCompletedAPIView,
)

urlpatterns = [
    path('', include(router.urls)),
    path('apply-promo-code/', ApplyPromoCodeGenericAPIView.as_view(), name='apply_promo_code'),
    path('checkout/', CheckOutCreateAPIView.as_view(), name='checkout'),
    path('list/', OrderListAPIView.as_view(), name='user_orders'),
    path('products-list/', OrderProductListAPIView.as_view(), name='user_ordered_products'),
    path('mark-complete/', MarkOrderAsCompletedAPIView.as_view(), name='mark_order_as_completed'),
]