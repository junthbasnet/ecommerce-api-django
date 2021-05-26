from django.urls import path, include
from .routers import router
from .views import (
    ApplyPromoCodeGenericAPIView,
    CheckOutCreateAPIView,
    OrderListAPIView,
    OrderProductListAPIView,
    MarkOrderAsCompletedAPIView,
    MarkOrderAsCancelledAPIView,
    PreOrderCheckOutCreateAPIView,
    PreOrderListAPIView,
    MarkPreOrderAsCompletedAPIView,
    MarkPreOrderAsCancelledAPIView,
)

urlpatterns = [
    path('', include(router.urls)),
    path('apply-promo-code/', ApplyPromoCodeGenericAPIView.as_view(), name='apply_promo_code'),
    path('products-list/', OrderProductListAPIView.as_view(), name='user_ordered_products'),
    path('checkout/', CheckOutCreateAPIView.as_view(), name='checkout'),
    path('pre-order-checkout/', PreOrderCheckOutCreateAPIView.as_view(), name='pre_order_checkout'),
    path('list/', OrderListAPIView.as_view(), name='user_orders'),
    path('pre-order/list/', PreOrderListAPIView.as_view(), name='user_pre_orders'),
    path('mark-complete/', MarkOrderAsCompletedAPIView.as_view(), name='mark_order_as_completed'),
    path('mark-cancel/', MarkOrderAsCancelledAPIView.as_view(), name='mark_order_as_cancelled'),
    path('mark-pre-order-complete/', MarkPreOrderAsCompletedAPIView.as_view(), name='mark_pre_order_as_completed'),
    path('mark-pre-order-cancel/', MarkPreOrderAsCancelledAPIView.as_view(), name='mark_pre_order_as_cancelled'),
]