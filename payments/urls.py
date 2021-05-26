from django.urls import path, include

from .routers import router
from .views import (
    IMEPayTokenCreateAPI,
    CreatePaymentAPI
)

app_name = 'payment'

urlpatterns = [
    path('', include(router.urls)),
    path('imepay-token-create/', IMEPayTokenCreateAPI.as_view()),
    path('create/', CreatePaymentAPI.as_view()),
]
