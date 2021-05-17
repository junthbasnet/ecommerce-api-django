from django.urls import path, include
from .routers import router
from .views import (
    CompareSimilarProductsListAPIView,
    SimilarProductsListAPIView,
)

app_name = 'products'

urlpatterns = [
    path('compare/', CompareSimilarProductsListAPIView.as_view(), name='compare_similar_products'),
    path('similar/', SimilarProductsListAPIView.as_view(), name='similar_products'),
    path('', include(router.urls)),
]
