from django.urls import path, include
from .routers import router
from .views import (
    CompareSimilarProductsListAPIView,
    SimilarProductsListAPIView,
    ProductBoughtTogetherAPIView,
    RecommendedProductsAPIView,
)

app_name = 'products'

urlpatterns = [
    path('compare/', CompareSimilarProductsListAPIView.as_view(), name='compare_similar_products'),
    path('similar/', SimilarProductsListAPIView.as_view(), name='similar_products'),
    path('bought-together/', ProductBoughtTogetherAPIView.as_view(), name='bought_together_products'),
    path('recommended/', RecommendedProductsAPIView.as_view(), name='recommended_products'),
    path('', include(router.urls)),
]

