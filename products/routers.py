from rest_framework.routers import DefaultRouter

from .views import (
    CategoryAPIViewSet,
    SubCategoryAPIViewSet,
)

router = DefaultRouter()

router.register('categories', CategoryAPIViewSet)
router.register('sub-categories', SubCategoryAPIViewSet)
