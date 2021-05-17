from django.urls import path, include
from .routers import router
from .views import (
    CompareSimilarProductsListAPIView,
)

app_name = 'products'

urlpatterns = [
    path('compare/', CompareSimilarProductsListAPIView.as_view(), name='compare_similar_products'),
    path('', include(router.urls)),
]
