from django.urls import path, include
from .routers import router
from .views import (
    ApplyPromoCodeGenericAPIView,
    CheckOutCreateAPIView,
    PreOrderCheckOutCreateAPIView,
    OrderListAPIView,
    OrderProductListAPIView,
    MarkOrderAsCompletedAPIView,
    MarkOrderAsCancelledAPIView,
    PreOrderListAPIView,
)

urlpatterns = [
    path('', include(router.urls)),
    path('apply-promo-code/', ApplyPromoCodeGenericAPIView.as_view(), name='apply_promo_code'),
    path('checkout/', CheckOutCreateAPIView.as_view(), name='checkout'),
    path('pre-order-checkout/', PreOrderCheckOutCreateAPIView.as_view(), name='pre_order_checkout'),
    path('list/', OrderListAPIView.as_view(), name='user_orders'),
    path('pre-order/list/', PreOrderListAPIView.as_view(), name='user_pre_orders'),
    path('products-list/', OrderProductListAPIView.as_view(), name='user_ordered_products'),
    path('mark-complete/', MarkOrderAsCompletedAPIView.as_view(), name='mark_order_as_completed'),
    path('mark-cancel/', MarkOrderAsCancelledAPIView.as_view(), name='mark_order_as_cancelled'),
]