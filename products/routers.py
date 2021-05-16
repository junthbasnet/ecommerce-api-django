from rest_framework.routers import DefaultRouter

from .views import (
    CategoryAPIViewSet,
    SubCategoryAPIViewSet,
    ProductAPIViewSet,
)

router = DefaultRouter()

router.register('categories', CategoryAPIViewSet)
router.register('sub-categories', SubCategoryAPIViewSet)
router.register('', ProductAPIViewSet)
