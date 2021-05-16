from rest_framework.routers import DefaultRouter

from .views import (
    CategoryAPIViewSet,
)

router = DefaultRouter()

router.register('categories', CategoryAPIViewSet)
