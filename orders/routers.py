from rest_framework.routers import DefaultRouter
from .views import (
    PromoCodeAPIViewSet,
)

router = DefaultRouter()
router.register('promo-codes', PromoCodeAPIViewSet)
