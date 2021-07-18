from rest_framework.routers import DefaultRouter
from .views import (
    PromoCodeAPIViewSet,
    OrderListRetrieveAPIViewSet,
)

router = DefaultRouter()
router.register('promo-codes', PromoCodeAPIViewSet)
router.register('list', OrderListRetrieveAPIViewSet)
