from rest_framework.routers import DefaultRouter

# from .views import UserPayment
from .views import (
    PaymentEnvironmentVariableAPIViewSet,
)

router = DefaultRouter()

router.register('env-variables', PaymentEnvironmentVariableAPIViewSet)
