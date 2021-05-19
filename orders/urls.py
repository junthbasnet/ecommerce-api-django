from django.urls import path, include
from .routers import router
from .views import (
    ApplyPromoCodeGenericAPIView,
)

urlpatterns = [
    path('', include(router.urls)),
    path('apply-promo-code/', ApplyPromoCodeGenericAPIView.as_view(), name='apply_promo_code')
]